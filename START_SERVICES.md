# 🚀 启动服务指南

## 快速启动

由于需要在两个终端中运行两个服务，请按照以下步骤操作：

### 方式一：使用启动脚本（推荐）

**终端 1 - 启动 FastAPI 后端：**
```bash
cd /Users/yurong/Desktop/AI编程练手/AI\ architect/JKid
./start_fastapi.sh
```

**终端 2 - 启动 Flask 前端：**
```bash
cd /Users/yurong/Desktop/AI编程练手/AI\ architect/JKid
./start_flask_frontend.sh
```

### 方式二：手动启动

**终端 1 - 启动 FastAPI 后端：**
```bash
cd /Users/yurong/Desktop/AI编程练手/AI\ architect/JKid
source venv/bin/activate  # 如果使用虚拟环境
python3 app_fastapi.py
```

**终端 2 - 启动 Flask 前端：**
```bash
cd /Users/yurong/Desktop/AI编程练手/AI\ architect/JKid
source venv/bin/activate  # 如果使用虚拟环境
python3 app_flask_frontend.py
```

## 📍 访问地址

启动成功后，可以通过以下地址访问：

- **前端页面**: http://127.0.0.1:5000
- **FastAPI API**: http://127.0.0.1:8000
- **API 文档 (Swagger)**: http://127.0.0.1:8000/docs
- **API 文档 (ReDoc)**: http://127.0.0.1:8000/redoc

## ✅ 验证服务是否正常运行

### 测试 FastAPI 后端

在浏览器中访问：http://127.0.0.1:8000/docs

或者使用命令行：
```bash
curl http://127.0.0.1:8000/
```

应该看到 JSON 响应：
```json
{
  "message": "JKid API",
  "version": "1.0.0",
  ...
}
```

### 测试 Flask 前端

在浏览器中访问：http://127.0.0.1:5000

应该看到主页正常加载。

## ⚠️ 常见问题

### 1. 端口被占用

如果遇到端口被占用错误：

**FastAPI (8000端口):**
```bash
lsof -ti:8000 | xargs kill -9
```

**Flask (5000端口):**
```bash
lsof -ti:5000 | xargs kill -9
```

### 2. 依赖未安装

如果提示模块未找到，安装依赖：
```bash
pip install -r requirements.txt
```

### 3. 环境变量未设置

确保 `.env` 文件存在并包含必要的 API Key：
- `GOOGLE_CLOUD_API_KEY` - Google Cloud API Key
- `SUPER_MIND_API_KEY` - Super Mind API Key

### 4. FastAPI 后端无法连接

如果 Flask 前端显示"无法连接到 FastAPI 后端服务"：
1. 确保 FastAPI 后端正在运行（终端 1）
2. 检查 http://127.0.0.1:8000 是否可以访问
3. 检查防火墙设置

## 🔄 停止服务

在运行服务的终端中按 `Ctrl+C` 停止服务。

## 📝 注意事项

1. **必须同时运行两个服务**：FastAPI 后端和 Flask 前端都需要运行
2. **启动顺序**：建议先启动 FastAPI 后端，再启动 Flask 前端
3. **环境变量**：确保 `.env` 文件配置正确
4. **虚拟环境**：如果使用虚拟环境，记得先激活

## 🎯 下一步

服务启动后，可以：
1. 访问 http://127.0.0.1:5000 使用应用
2. 访问 http://127.0.0.1:8000/docs 查看 API 文档
3. 测试文件上传和 OCR 功能
4. 准备迁移前端到 Next.js

