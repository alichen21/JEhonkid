"""
Picture to Text 功能模块
使用 Google Cloud Vision API 进行日语OCR识别
"""

import os
import base64
import json
import tempfile
from typing import Dict, List, Optional
from dotenv import load_dotenv
import requests
from PIL import Image

# 尝试导入 pillow-heif 以支持 HEIC 格式
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    HEIC_SUPPORT = True
except ImportError:
    HEIC_SUPPORT = False
    print("⚠️  pillow-heif 未安装，HEIC 格式可能无法处理。安装命令: pip install pillow-heif")

# 加载环境变量
load_dotenv()

class PictureToText:
    """图片转文字类，使用Google Cloud Vision API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化
        
        Args:
            api_key: Google Cloud API Key，如果不提供则从环境变量读取
        """
        self.api_key = api_key or os.getenv('GOOGLE_CLOUD_API_KEY')
        if not self.api_key:
            raise ValueError("Google Cloud API Key未设置，请检查.env文件")
        
        # Google Cloud Vision API REST端点
        self.api_url = f"https://vision.googleapis.com/v1/images:annotate?key={self.api_key}"
    
    def _convert_heic_to_jpg(self, image_path: str) -> str:
        """
        将 HEIC 格式图片转换为 JPG 格式
        
        Args:
            image_path: HEIC 图片文件路径
            
        Returns:
            转换后的临时 JPG 文件路径
        """
        if not HEIC_SUPPORT:
            raise ValueError("HEIC 格式不支持，请安装 pillow-heif: pip install pillow-heif")
        
        try:
            img = Image.open(image_path)
            # 创建临时文件
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
            temp_path = temp_file.name
            temp_file.close()
            
            # 转换为 RGB 模式（HEIC 可能是 RGBA）
            if img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = rgb_img
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 保存为 JPG
            img.save(temp_path, 'JPEG', quality=95)
            return temp_path
        except Exception as e:
            raise Exception(f"HEIC 转换失败: {str(e)}")
    
    def _encode_image(self, image_path: str) -> str:
        """
        将图片编码为base64字符串
        自动处理 HEIC 格式转换
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            base64编码的图片字符串
        """
        # 检查是否为 HEIC 格式
        file_ext = os.path.splitext(image_path)[1].lower()
        temp_file = None
        
        try:
            if file_ext in ['.heic', '.heif']:
                # 转换为 JPG
                converted_path = self._convert_heic_to_jpg(image_path)
                temp_file = converted_path
                image_path = converted_path
            
            with open(image_path, 'rb') as image_file:
                return base64.b64encode(image_file.read()).decode('UTF-8')
        finally:
            # 清理临时文件
            if temp_file and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except:
                    pass
    
    def detect_text(self, image_path: str, detection_type: str = "DOCUMENT_TEXT_DETECTION") -> Dict:
        """
        检测图片中的文本
        
        Args:
            image_path: 图片文件路径
            detection_type: 检测类型
                - "TEXT_DETECTION": 通用文本检测
                - "DOCUMENT_TEXT_DETECTION": 文档文本检测（推荐用于打印文本，支持复杂布局）
        
        Returns:
            包含识别结果的字典
        """
        # 编码图片
        image_content = self._encode_image(image_path)
        
        # 构建请求体
        request_body = {
            "requests": [
                {
                    "image": {
                        "content": image_content
                    },
                    "features": [
                        {
                            "type": detection_type,
                            "maxResults": 10
                        }
                    ],
                    "imageContext": {
                        "languageHints": ["ja"]  # 提示API这是日语内容
                    }
                }
            ]
        }
        
        # 发送请求
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(self.api_url, json=request_body, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API请求失败: {str(e)}")
    
    def extract_text(self, image_path: str, detection_type: str = "DOCUMENT_TEXT_DETECTION") -> Dict[str, any]:
        """
        提取图片中的文本并返回结构化结果
        
        Args:
            image_path: 图片文件路径
            detection_type: 检测类型
        
        Returns:
            包含以下字段的字典:
            - full_text: 完整识别的文本
            - text_blocks: 文本块列表（带位置信息）
            - confidence: 置信度（如果有）
        """
        result = self.detect_text(image_path, detection_type)
        
        # 解析响应
        if 'responses' not in result or len(result['responses']) == 0:
            return {
                "full_text": "",
                "text_blocks": [],
                "error": "未检测到文本"
            }
        
        response = result['responses'][0]
        
        # 检查是否有错误
        if 'error' in response:
            return {
                "full_text": "",
                "text_blocks": [],
                "error": response['error'].get('message', '未知错误')
            }
        
        # 提取文本
        if detection_type == "DOCUMENT_TEXT_DETECTION":
            # DOCUMENT_TEXT_DETECTION返回fullTextAnnotation
            if 'fullTextAnnotation' in response:
                full_text_annotation = response['fullTextAnnotation']
                full_text = full_text_annotation.get('text', '')
                
                # 提取文本块
                text_blocks = []
                if 'pages' in full_text_annotation:
                    for page in full_text_annotation['pages']:
                        if 'blocks' in page:
                            for block in page['blocks']:
                                if 'paragraphs' in block:
                                    for paragraph in block['paragraphs']:
                                        block_text = ""
                                        if 'words' in paragraph:
                                            for word in paragraph['words']:
                                                if 'symbols' in word:
                                                    word_text = "".join([s['text'] for s in word['symbols']])
                                                    block_text += word_text
                                        if block_text:
                                            text_blocks.append({
                                                "text": block_text,
                                                "confidence": paragraph.get('confidence', 0)
                                            })
                
                return {
                    "full_text": full_text,
                    "text_blocks": text_blocks,
                    "language": full_text_annotation.get('pages', [{}])[0].get('property', {}).get('detectedLanguages', [])
                }
        
        elif detection_type == "TEXT_DETECTION":
            # TEXT_DETECTION返回textAnnotations
            if 'textAnnotations' in response and len(response['textAnnotations']) > 0:
                # 第一个是完整文本
                full_text = response['textAnnotations'][0].get('description', '')
                
                # 其余是单独的文本块
                text_blocks = []
                for annotation in response['textAnnotations'][1:]:
                    text_blocks.append({
                        "text": annotation.get('description', ''),
                        "bounding_box": annotation.get('boundingPoly', {})
                    })
                
                return {
                    "full_text": full_text,
                    "text_blocks": text_blocks
                }
        
        return {
            "full_text": "",
            "text_blocks": [],
            "error": "未找到文本数据"
        }


def main():
    """测试函数"""
    # 初始化
    ocr = PictureToText()
    
    # 测试图片路径
    test_images = [
        "Picture books/Kumon test.png",
        "Picture books/Kumon test2.png",
        "Picture books/Kumon test3.png",
        "Picture books/short para 1.png",
        "Picture books/short para 2.png",
        "Picture books/Qiaohu1.HEIC",
        "Picture books/Qiaohu2.HEIC"
    ]
    
    print("=" * 60)
    print("Google Cloud Vision API - 日语OCR测试")
    print("=" * 60)
    
    for image_path in test_images:
        if not os.path.exists(image_path):
            print(f"\n⚠️  图片不存在: {image_path}")
            continue
        
        print(f"\n📷 处理图片: {image_path}")
        print("-" * 60)
        
        try:
            # 使用DOCUMENT_TEXT_DETECTION（更适合打印文本）
            result = ocr.extract_text(image_path, detection_type="DOCUMENT_TEXT_DETECTION")
            
            if "error" in result:
                print(f"❌ 错误: {result['error']}")
                continue
            
            print(f"✅ 识别成功！")
            print(f"\n完整文本:\n{result['full_text']}")
            
            if result['text_blocks']:
                print(f"\n文本块数量: {len(result['text_blocks'])}")
                print("\n前3个文本块:")
                for i, block in enumerate(result['text_blocks'][:3], 1):
                    print(f"  {i}. {block['text'][:50]}...")
            
            if result.get('language'):
                print(f"\n检测到的语言: {result['language']}")
        
        except Exception as e:
            print(f"❌ 处理失败: {str(e)}")


if __name__ == "__main__":
    main()

