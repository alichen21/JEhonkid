# 🧹 清理计划

## 将要删除的 Flask 相关文件

### Flask 应用文件
- ✅ `app.py` - 原始 Flask 应用（已迁移到 FastAPI）
- ✅ `app_flask_frontend.py` - Flask 前端代理（已迁移到 Next.js）

### Flask 模板文件
- ✅ `templates/` - Flask Jinja2 模板目录（已迁移到 Next.js）

### Flask 启动脚本
- ✅ `start_web.sh` - Flask 启动脚本
- ✅ `start_web.bat` - Flask 启动脚本（Windows）
- ✅ `start_flask_frontend.sh` - Flask 前端启动脚本

## 保留的文件

### 核心应用文件
- ✅ `app_fastapi.py` - FastAPI 后端（必需）
- ✅ `frontend/` - Next.js 前端（必需）

### 业务逻辑模块
- ✅ `picture_to_text.py` - OCR 模块
- ✅ `text_processor.py` - 文本处理模块
- ✅ `text_to_speech.py` - TTS 模块
- ✅ `task_manager.py` - 任务管理模块

### 配置和数据
- ✅ `requirements.txt` - Python 依赖
- ✅ `static/` - 静态文件目录（FastAPI 也在使用）
- ✅ `Picture books/` - 图片数据目录

### 启动脚本（FastAPI/Next.js）
- ✅ `start_fastapi.sh` - FastAPI 启动脚本
- ✅ `restart_fastapi.sh` - FastAPI 重启脚本
- ✅ `frontend/start.sh` - Next.js 启动脚本
- ✅ `check_services.sh` - 服务检查脚本

### 文档和测试
- ✅ 所有 `.md` 文档文件
- ✅ 测试文件（`test_*.py`）

