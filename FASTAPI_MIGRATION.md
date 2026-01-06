# FastAPI 后端迁移说明

## 📋 概述

项目已成功迁移后端 API 到 FastAPI，前端暂时继续使用 Flask 模板渲染。这是一个分阶段迁移策略，确保平滑过渡。

## 🏗️ 架构说明

### 当前架构

```
┌─────────────────┐         ┌─────────────────┐
│  Flask 前端      │ ──────> │  FastAPI 后端   │
│  (模板渲染)      │ 代理API  │  (API 服务)     │
│  Port: 5000     │         │  Port: 8000     │
└─────────────────┘         └─────────────────┘
```

- **Flask 前端** (`app_flask_frontend.py`): 负责模板渲染和页面展示，API 请求代理到 FastAPI
- **FastAPI 后端** (`app_fastapi.py`): 提供所有 API 端点，处理业务逻辑

## 🚀 快速开始

### 1. 安装依赖

```bash
# 激活虚拟环境
source venv/bin/activate

# 安装新依赖
pip install -r requirements.txt
```

### 2. 启动服务

**方式一：使用启动脚本（推荐）**

```bash
# 终端 1: 启动 FastAPI 后端
./start_fastapi.sh

# 终端 2: 启动 Flask 前端
./start_flask_frontend.sh
```

**方式二：手动启动**

```bash
# 终端 1: 启动 FastAPI 后端
python app_fastapi.py

# 终端 2: 启动 Flask 前端
python app_flask_frontend.py
```

### 3. 访问应用

- **前端页面**: http://127.0.0.1:5000
- **FastAPI API**: http://127.0.0.1:8000
- **API 文档**: http://127.0.0.1:8000/docs (Swagger UI)
- **API 文档 (ReDoc)**: http://127.0.0.1:8000/redoc

## 📁 文件说明

### 新增文件

- `app_fastapi.py` - FastAPI 后端应用（所有 API 端点）
- `app_flask_frontend.py` - Flask 前端应用（模板渲染 + API 代理）
- `start_fastapi.sh` - FastAPI 启动脚本
- `start_flask_frontend.sh` - Flask 前端启动脚本

### 保留文件

- `app.py` - 原始 Flask 应用（保留作为备份）
- `templates/` - HTML 模板（继续使用）
- `static/` - 静态文件（继续使用）
- 所有业务逻辑模块（`picture_to_text.py`, `text_processor.py`, `text_to_speech.py`, `task_manager.py`）

## 🔌 API 端点

所有 API 端点已迁移到 FastAPI，保持与原有 API 格式兼容：

### 文件上传
- `POST /api/upload` - 上传图片文件

### 任务管理
- `GET /api/task/{task_id}` - 查询任务状态

### OCR 识别
- `GET /api/ocr/{filename}` - 获取 OCR 结果

### 图片服务
- `GET /images/{filename}` - 获取图片（支持 HEIC 转换）

### 文本转语音
- `POST /api/tts` - TTS 生成（返回 base64）
- `POST /api/tts/audio` - TTS 生成（返回音频文件）

## 🔧 配置

### 环境变量

FastAPI 后端地址可以通过环境变量配置：

```bash
export FASTAPI_BASE_URL=http://127.0.0.1:8000
```

Flask 前端会自动使用此地址代理 API 请求。

### CORS 配置

FastAPI 已配置 CORS，允许来自 Flask 前端的请求：

```python
allow_origins=["http://127.0.0.1:5000", "http://localhost:5000"]
```

## 📝 迁移细节

### 已迁移的功能

✅ 文件上传和异步任务处理  
✅ OCR 识别 API  
✅ 文本处理 API  
✅ TTS 生成 API  
✅ 任务状态查询  
✅ 图片服务（包括 HEIC 转换）  
✅ 静态文件服务  

### 保持不变的功能

✅ 前端模板（Jinja2）  
✅ 前端 JavaScript 逻辑  
✅ 业务逻辑模块  
✅ 任务管理器（内存存储）  

## 🐛 故障排除

### 问题：无法连接到 FastAPI 后端

**症状**: Flask 前端显示 "无法连接到 FastAPI 后端服务"

**解决**:
1. 确保 FastAPI 后端正在运行（检查 http://127.0.0.1:8000）
2. 检查 `FASTAPI_BASE_URL` 环境变量是否正确
3. 检查防火墙设置

### 问题：CORS 错误

**症状**: 浏览器控制台显示 CORS 错误

**解决**:
1. 检查 `app_fastapi.py` 中的 CORS 配置
2. 确保 Flask 前端地址在允许列表中

### 问题：文件上传失败

**症状**: 上传文件时返回错误

**解决**:
1. 检查文件大小是否超过 10MB
2. 检查文件格式是否支持
3. 检查 `static/uploads` 目录权限

## 🔄 下一步：前端迁移到 Next.js

当前阶段完成后，可以继续迁移前端到 Next.js：

1. 创建 Next.js 项目
2. 迁移 HTML 模板到 React 组件
3. 迁移 JavaScript 逻辑到 React hooks
4. 配置 API 调用（直接调用 FastAPI，无需代理）

## 📚 参考文档

- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [Flask 文档](https://flask.palletsprojects.com/)
- [Uvicorn 文档](https://www.uvicorn.org/)

## ⚠️ 注意事项

1. **必须同时运行两个服务**: FastAPI 后端和 Flask 前端都需要运行
2. **端口冲突**: 确保 5000 和 8000 端口未被占用
3. **环境变量**: 确保所有必要的环境变量已设置（`.env` 文件）
4. **备份**: 原始 `app.py` 已保留作为备份，可以随时回退

## 🎉 迁移完成

后端 API 已成功迁移到 FastAPI！现在可以享受：

- ✅ 自动生成的 API 文档（Swagger UI）
- ✅ 更好的性能（异步支持）
- ✅ 类型安全（Pydantic 模型）
- ✅ 现代化的 API 框架

下一步可以继续迁移前端到 Next.js，实现完全的前后端分离。

