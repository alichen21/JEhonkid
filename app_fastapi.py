"""
FastAPI Web应用 - 后端 API
支持文件上传和后台异步处理
为 Next.js 前端提供 RESTful API 服务
"""

import os
import base64
import tempfile
import threading
from io import BytesIO
from pathlib import Path
from typing import Optional, Dict, List
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException, Response, Body
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from picture_to_text import PictureToText, HEIC_SUPPORT
from text_processor import TextProcessor
from text_to_speech import TextToSpeech
from task_manager import task_manager, TaskStatus
from PIL import Image
import glob
import time

app = FastAPI(title="JKid API", version="1.0.0")

# CORS 配置 - 允许 Next.js 前端访问
# 开发环境：允许所有本地源
# 生产环境：部署后前后端在同一域名，CORS 不是必需的，但保留以兼容开发模式
allowed_origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://127.0.0.1:3001",
    "http://localhost:3001",
    "http://127.0.0.1:3002",
    "http://localhost:3002",
    "http://127.0.0.1:5000",
    "http://localhost:5000",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

# 生产环境域名（从环境变量读取，如果有的话）
production_domain = os.getenv("PRODUCTION_DOMAIN")
if production_domain:
    allowed_origins.append(f"https://{production_domain}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# 添加全局CORS响应头（作为备用）
@app.middleware("http")
async def add_cors_header(request, call_next):
    response = await call_next(request)
    origin = request.headers.get("origin")
    if origin and ("localhost" in origin or "127.0.0.1" in origin):
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

# 配置
UPLOAD_FOLDER = 'Picture books'
USER_UPLOAD_FOLDER = 'static/uploads'
AUDIO_FOLDER = 'static/audio'
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'heic', 'heif', 'gif', 'bmp'}

# 确保目录存在
os.makedirs(USER_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)
os.makedirs('static', exist_ok=True)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 前端构建目录路径
FRONTEND_BUILD_DIR = Path("frontend/out")


# Pydantic 模型
class TTSRequest(BaseModel):
    text: str
    voice_name: Optional[str] = "ja-JP-Neural2-B"
    model: Optional[str] = None
    speaking_rate: Optional[float] = 0.75


class TTSAudioRequest(BaseModel):
    text: str
    speaking_rate: Optional[float] = 0.75

# 初始化OCR和文本处理器（使用 try-except 允许应用在没有环境变量时启动）
ocr = None
text_processor = None
try:
    ocr = PictureToText()
    print("✅ OCR 模块已初始化")
except Exception as e:
    print(f"⚠️  OCR 模块初始化失败: {str(e)}")
    print("   提示：需要设置 GOOGLE_CLOUD_API_KEY 环境变量")

try:
    text_processor = TextProcessor()
    print("✅ 文本处理模块已初始化")
except Exception as e:
    print(f"⚠️  文本处理模块初始化失败: {str(e)}")
    print("   提示：需要设置 SUPER_MIND_API_KEY 或 AI_BUILDER_TOKEN 环境变量")

# 初始化TTS（如果可用）
tts = None
try:
    tts = TextToSpeech()
    print("✅ Text-to-Speech 模块已初始化")
except Exception as e:
    print(f"⚠️  Text-to-Speech 模块初始化失败: {str(e)}")
    print("   提示：需要设置 GOOGLE_CLOUD_API_KEY 环境变量")


def allowed_file(filename: str) -> bool:
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def secure_filename(filename: str) -> str:
    """生成安全的文件名（移除特殊字符，防止路径遍历）"""
    import re
    # 移除路径分隔符
    filename = os.path.basename(filename)
    # 只保留字母、数字、点、下划线、连字符
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    return filename


def process_image_task(task_id: str, image_path: str):
    """
    后台线程处理图片任务
    执行 OCR -> 文本处理 -> TTS 生成流程
    """
    try:
        # 更新状态：开始处理
        task_manager.update_task_status(task_id, TaskStatus.PROCESSING)
        
        # Step 1: OCR识别
        if ocr is None:
            task_manager.update_task_status(
                task_id,
                TaskStatus.FAILED,
                error="OCR 模块未初始化，请检查 GOOGLE_CLOUD_API_KEY 环境变量"
            )
            return
        
        task_manager.update_task_status(
            task_id, 
            TaskStatus.PROCESSING,
            progress={'ocr': 'processing'}
        )
        
        ocr_result = ocr.extract_text(image_path, detection_type="DOCUMENT_TEXT_DETECTION")
        
        if 'error' in ocr_result:
            task_manager.update_task_status(
                task_id,
                TaskStatus.FAILED,
                error=f"OCR识别失败: {ocr_result['error']}"
            )
            return
        
        task_manager.update_task_status(
            task_id,
            TaskStatus.OCR_COMPLETED,
            progress={'ocr': 'completed'}
        )
        
        # Step 2: 文本处理
        processed_text = None
        if ocr_result.get('full_text'):
            if text_processor is None:
                print(f"[任务 {task_id}] 文本处理模块未初始化，跳过文本处理步骤")
                processed_text = {
                    'cleaned_text': ocr_result.get('full_text', ''),
                    'translation': '文本处理模块未初始化'
                }
            else:
                task_manager.update_task_status(
                    task_id,
                    TaskStatus.TEXT_PROCESSING,
                    progress={'text_processing': 'processing'}
                )
                
                print(f"[任务 {task_id}] 开始文本处理...")
                text_processing_start = time.time()
                processed_text = text_processor.process_ocr_text(ocr_result.get('full_text', ''))
                text_processing_duration = time.time() - text_processing_start
                print(f"[任务 {task_id}] 文本处理完成，耗时: {text_processing_duration:.2f} 秒")
            
            if processed_text.get('error'):
                task_manager.update_task_status(
                    task_id,
                    TaskStatus.FAILED,
                    error=f"文本处理失败: {processed_text['error']}"
                )
                return
            
            task_manager.update_task_status(
                task_id,
                TaskStatus.TEXT_PROCESSING,
                progress={'text_processing': 'completed'}
            )
        
        # Step 3: TTS生成（如果TTS可用且有文本）
        audio_urls = {}
        if tts and processed_text:
            task_manager.update_task_status(
                task_id,
                TaskStatus.TTS_GENERATING,
                progress={'tts': 'processing'}
            )
            
            # 为每个分段生成音频
            segments = processed_text.get('segments', [])
            if segments:
                for idx, segment in enumerate(segments):
                    if segment.strip():
                        tts_result = tts.synthesize_japanese(
                            text=segment,
                            voice_name="ja-JP-Neural2-B",
                            speaking_rate=0.75,
                            output_format="mp3"
                        )
                        
                        if 'error' not in tts_result:
                            # 保存音频文件
                            audio_filename = f"{task_id}_segment_{idx}.mp3"
                            audio_path = os.path.join(AUDIO_FOLDER, audio_filename)
                            
                            with open(audio_path, 'wb') as f:
                                f.write(tts_result['audio_content'])
                            
                            audio_urls[f'segment_{idx}'] = f'/static/audio/{audio_filename}'
            
            # 为完整正文生成音频
            main_text = processed_text.get('main_text', '') or processed_text.get('japanese_text', '')
            if main_text.strip():
                tts_result = tts.synthesize_japanese(
                    text=main_text,
                    voice_name="ja-JP-Neural2-B",
                    speaking_rate=0.75,
                    output_format="mp3"
                )
                
                if 'error' not in tts_result:
                    audio_filename = f"{task_id}_main.mp3"
                    audio_path = os.path.join(AUDIO_FOLDER, audio_filename)
                    
                    with open(audio_path, 'wb') as f:
                        f.write(tts_result['audio_content'])
                    
                    audio_urls['main'] = f'/static/audio/{audio_filename}'
            
            # 为指导语生成音频（如果有）
            instruction = processed_text.get('instruction', '')
            if instruction.strip():
                tts_result = tts.synthesize_japanese(
                    text=instruction,
                    voice_name="ja-JP-Neural2-B",
                    speaking_rate=0.75,
                    output_format="mp3"
                )
                
                if 'error' not in tts_result:
                    audio_filename = f"{task_id}_instruction.mp3"
                    audio_path = os.path.join(AUDIO_FOLDER, audio_filename)
                    
                    with open(audio_path, 'wb') as f:
                        f.write(tts_result['audio_content'])
                    
                    audio_urls['instruction'] = f'/static/audio/{audio_filename}'
            
            task_manager.update_task_status(
                task_id,
                TaskStatus.TTS_GENERATING,
                progress={'tts': 'completed'}
            )
        
        # 组装最终结果
        result = {
            'ocr': {
                'full_text': ocr_result.get('full_text', ''),
                'text_blocks': ocr_result.get('text_blocks', []),
                'language': ocr_result.get('language', [])
            },
            'processed_text': processed_text,
            'audio_urls': audio_urls
        }
        
        # 更新任务为完成状态
        task_manager.update_task_status(
            task_id,
            TaskStatus.COMPLETED,
            result=result
        )
        
    except Exception as e:
        # 处理异常
        task_manager.update_task_status(
            task_id,
            TaskStatus.FAILED,
            error=f"处理失败: {str(e)}"
        )


@app.get("/")
def root():
    """根路径 - 如果有前端构建文件，返回前端页面；否则返回 API 信息"""
    # 检查是否有前端构建文件
    index_path = Path("frontend/out/index.html")
    if index_path.exists():
        return FileResponse(index_path)
    
    # 否则返回 API 信息
    return {
        "message": "JKid API",
        "version": "1.0.0",
        "endpoints": {
            "upload": "/api/upload",
            "task": "/api/task/{task_id}",
            "tts": "/api/tts",
            "tts_audio": "/api/tts/audio",
            "ocr": "/api/ocr/{filename}",
            "images": "/images/{filename}"
        }
    }


@app.get("/api/ocr/{filename:path}")
def api_ocr(filename: str):
    """API端点 - 获取单个图片的OCR结果"""
    if ocr is None:
        raise HTTPException(
            status_code=503, 
            detail="OCR 模块未初始化，请检查 GOOGLE_CLOUD_API_KEY 环境变量"
        )
    
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    try:
        result = ocr.extract_text(image_path, detection_type="DOCUMENT_TEXT_DETECTION")
        return {
            'success': True,
            'filename': filename,
            'full_text': result.get('full_text', ''),
            'text_blocks': result.get('text_blocks', []),
            'language': result.get('language', [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/images/{filename:path}")
def serve_image(filename: str):
    """提供图片文件，自动转换 HEIC 格式为 JPG"""
    # 先尝试从用户上传目录查找
    image_path = os.path.join(USER_UPLOAD_FOLDER, filename)
    upload_folder = USER_UPLOAD_FOLDER
    
    if not os.path.exists(image_path):
        # 如果不存在，从原始目录查找
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        upload_folder = UPLOAD_FOLDER
    
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    # 检查是否为 HEIC 格式
    file_ext = os.path.splitext(filename)[1].lower()
    
    if file_ext in ['.heic', '.heif']:
        # 转换为 JPG 格式返回
        try:
            if not HEIC_SUPPORT:
                raise HTTPException(status_code=500, detail="HEIC 格式不支持，请安装 pillow-heif")
            
            img = Image.open(image_path)
            
            # 转换为 RGB 模式
            if img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = rgb_img
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 创建临时字节流
            img_io = BytesIO()
            img.save(img_io, 'JPEG', quality=95)
            img_io.seek(0)
            
            return Response(
                content=img_io.getvalue(),
                media_type='image/jpeg',
                headers={
                    'Content-Disposition': f'inline; filename={os.path.splitext(filename)[0]}.jpg'
                }
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'HEIC 转换失败: {str(e)}')
    else:
        # 其他格式直接返回
        return FileResponse(image_path)


@app.post("/api/tts")
def api_tts(data: TTSRequest):
    """API端点 - 将日语文本转换为音频（返回 base64）"""
    if not tts:
        raise HTTPException(
            status_code=503,
            detail='Text-to-Speech 服务未初始化。请检查 GOOGLE_CLOUD_API_KEY 环境变量。'
        )
    
    try:
        if not data.text:
            raise HTTPException(status_code=400, detail='文本内容为空')
        
        # 调用TTS API
        result = tts.synthesize_japanese(
            text=data.text,
            voice_name=data.voice_name or "ja-JP-Neural2-B",
            speaking_rate=data.speaking_rate or 0.75,
            output_format="mp3",
            model=data.model
        )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result['error'])
        
        # 返回音频数据（base64编码）
        audio_base64 = base64.b64encode(result['audio_content']).decode('utf-8')
        
        return {
            'success': True,
            'audio_data': audio_base64,
            'audio_format': result['audio_format'],
            'voice_name': result['voice_name'],
            'model': result.get('model', 'default')
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'处理失败: {str(e)}')


@app.post("/api/tts/audio")
def api_tts_audio(data: TTSAudioRequest):
    """API端点 - 直接返回音频文件（用于HTML5 audio标签）"""
    if not tts:
        raise HTTPException(
            status_code=503,
            detail="TTS服务未初始化"
        )
    
    try:
        if not data.text:
            raise HTTPException(status_code=400, detail="文本内容为空")
        
        # 调用TTS API
        result = tts.synthesize_japanese(
            text=data.text,
            voice_name="ja-JP-Neural2-B",
            speaking_rate=data.speaking_rate or 0.75,
            output_format="mp3"
        )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result['error'])
        
        # 返回音频文件
        return Response(
            content=result['audio_content'],
            media_type='audio/mpeg',
            headers={
                'Content-Disposition': 'inline; filename=speech.mp3'
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


@app.options("/api/upload")
async def options_upload():
    """处理CORS预检请求"""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

@app.post("/api/upload")
async def api_upload(file: UploadFile = File(...)):
    """API端点 - 上传图片文件"""
    # 如果没有文件名，生成一个默认文件名
    if not file.filename:
        # 检查Content-Type来确定文件类型
        content_type = file.content_type or 'image/jpeg'
        if 'jpeg' in content_type or 'jpg' in content_type:
            ext = '.jpg'
        elif 'png' in content_type:
            ext = '.png'
        else:
            ext = '.jpg'  # 默认使用jpg
        filename = f"upload_{int(time.time())}{ext}"
    else:
        filename = file.filename
    
    # 验证文件扩展名
    if not allowed_file(filename):
        raise HTTPException(
            status_code=400,
            detail=f'不支持的文件格式。支持的格式: {", ".join(ALLOWED_EXTENSIONS)}'
        )
    
    try:
        # 读取文件内容
        contents = await file.read()
        
        # 检查文件大小
        if len(contents) > MAX_CONTENT_LENGTH:
            raise HTTPException(status_code=400, detail="文件大小超过限制（10MB）")
        
        # 生成安全的文件名
        filename = secure_filename(filename)
        # 添加时间戳避免文件名冲突
        timestamp = int(time.time())
        name, ext = os.path.splitext(filename)
        if not ext:  # 如果没有扩展名，根据Content-Type添加
            content_type = file.content_type or 'image/jpeg'
            if 'jpeg' in content_type or 'jpg' in content_type:
                ext = '.jpg'
            elif 'png' in content_type:
                ext = '.png'
            else:
                ext = '.jpg'
        filename = f"{name}_{timestamp}{ext}"
        
        filepath = os.path.join(USER_UPLOAD_FOLDER, filename)
        
        # 保存文件
        with open(filepath, 'wb') as f:
            f.write(contents)
        
        # 创建任务
        task_id = task_manager.create_task(filename, filepath)
        
        # 启动后台线程处理任务
        thread = threading.Thread(target=process_image_task, args=(task_id, filepath))
        thread.daemon = True
        thread.start()
        
        response_data = {
            'success': True,
            'task_id': task_id,
            'filename': filename,
            'message': '文件上传成功，正在处理...'
        }
        
        # 添加CORS响应头
        return JSONResponse(
            content=response_data,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'上传失败: {str(e)}')


@app.get("/api/task/{task_id}")
def api_get_task(task_id: str):
    """API端点 - 查询任务状态"""
    task = task_manager.get_task(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    # 构建响应
    response = {
        'success': True,
        'task_id': task['task_id'],
        'filename': task['filename'],
        'status': task['status'],
        'progress': task['progress'],
        'created_at': task['created_at'],
        'updated_at': task['updated_at']
    }
    
    # 如果任务完成，包含结果
    if task['status'] == TaskStatus.COMPLETED.value and task['result']:
        response['result'] = task['result']
    
    # 如果任务失败，包含错误信息
    if task['status'] == TaskStatus.FAILED.value and task['error']:
        response['error'] = task['error']
    
    return response


# 挂载前端静态文件（必须在所有 API 路由之后）
if FRONTEND_BUILD_DIR.exists():
    # 挂载 Next.js 的 _next 静态资源
    next_static_dir = FRONTEND_BUILD_DIR / "_next"
    if next_static_dir.exists():
        app.mount("/_next", StaticFiles(directory=str(next_static_dir)), name="nextjs")
    
    # 服务前端页面（catch-all 路由，必须在最后）
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """服务前端页面 - 支持客户端路由"""
        # API 和静态资源路径不处理（应该已经被其他路由处理）
        if full_path.startswith("api/") or full_path.startswith("images/") or full_path.startswith("static/") or full_path.startswith("_next/"):
            raise HTTPException(status_code=404, detail="Not found")
        
        # 检查文件是否存在
        file_path = FRONTEND_BUILD_DIR / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        
        # 对于客户端路由（如 /upload），返回 index.html
        index_path = FRONTEND_BUILD_DIR / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
        
        raise HTTPException(status_code=404, detail="File not found")


if __name__ == '__main__':
    import uvicorn
    
    # 从环境变量读取端口，如果没有则使用默认值 8000
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")  # 生产环境使用 0.0.0.0
    
    print("=" * 60)
    print("启动 FastAPI 后端服务")
    print("=" * 60)
    print(f"API 地址: http://{host}:{port}")
    print(f"API 文档: http://{host}:{port}/docs")
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    
    uvicorn.run(app, host=host, port=port, log_level="info")

