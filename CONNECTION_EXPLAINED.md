# 🔌 前端后端连接方式说明

## 当前架构

```
┌─────────────────┐        直接 HTTP 请求        ┌─────────────────┐
│  Next.js 前端   │ ──────────────────────────> │  FastAPI 后端   │
│  Port: 3000     │                             │  Port: 8000     │
└─────────────────┘                             └─────────────────┘
```

## 连接流程

### 1. 前端 API 调用

前端代码 (`frontend/lib/api.ts`) 直接调用 FastAPI：

```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

// 上传图片
fetch(`${API_BASE_URL}/api/upload`, { ... })
```

**注意**：前端是**直接**调用 FastAPI，不经过 Next.js 代理。

### 2. CORS 配置

FastAPI 后端需要配置 CORS 来允许前端请求：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js 前端
        "http://127.0.0.1:3000",  # Next.js 前端
        # ... 其他地址
    ],
    ...
)
```

## 🔧 已修复的问题

### 问题：CORS 配置缺少 Next.js 端口

**原因**：FastAPI 的 CORS 只允许了 Flask 的端口（5000），没有包含 Next.js 的端口（3000）。

**修复**：已更新 `app_fastapi.py` 中的 CORS 配置，添加了：
- `http://localhost:3000`
- `http://127.0.0.1:3000`

## 🚀 需要重启 FastAPI 服务

**重要**：修改 CORS 配置后，需要重启 FastAPI 服务才能生效！

### 重启步骤：

1. 停止当前运行的 FastAPI 服务（在运行它的终端按 `Ctrl+C`）
2. 重新启动：
   ```bash
   cd /Users/yurong/Desktop/AI编程练手/AI\ architect/JKid
   python3 app_fastapi.py
   ```

## 📝 上传流程

1. **用户点击"开始处理"**
   - 前端调用 `uploadImage(file)` 函数
   - 发送 POST 请求到 `http://127.0.0.1:8000/api/upload`

2. **FastAPI 接收请求**
   - 保存文件到 `static/uploads/`
   - 创建任务并返回 `task_id`
   - 启动后台线程处理（OCR → 文本处理 → TTS）

3. **前端开始轮询**
   - 使用 `useTaskPolling` hook
   - 每秒查询一次任务状态：`GET /api/task/{task_id}`

4. **显示进度和结果**
   - 根据任务状态显示进度条
   - 任务完成后显示结果

## 🐛 调试方法

### 检查浏览器控制台

打开浏览器开发者工具（F12），查看：
1. **Network 标签**：检查 API 请求是否成功
2. **Console 标签**：查看是否有错误信息

### 常见错误

1. **CORS 错误**
   ```
   Access to fetch at 'http://127.0.0.1:8000/api/upload' from origin 
   'http://localhost:3000' has been blocked by CORS policy
   ```
   **解决**：确保 FastAPI 的 CORS 配置包含 `http://localhost:3000`

2. **404 错误**
   ```
   GET http://127.0.0.1:8000/api/task/xxx 404
   ```
   **解决**：确保 FastAPI 服务正在运行

3. **网络错误**
   ```
   Failed to fetch
   ```
   **解决**：检查 FastAPI 服务是否启动，端口是否正确

## ✅ 验证连接

### 方法 1：浏览器控制台

打开浏览器控制台，执行：
```javascript
fetch('http://127.0.0.1:8000/')
  .then(r => r.json())
  .then(console.log)
```

应该看到 API 信息。

### 方法 2：直接访问 API 文档

访问：http://127.0.0.1:8000/docs

应该看到 Swagger UI 文档页面。

## 📋 检查清单

- [ ] FastAPI 服务正在运行（端口 8000）
- [ ] Next.js 服务正在运行（端口 3000）
- [ ] CORS 配置包含 `http://localhost:3000`
- [ ] `.env.local` 文件存在且配置正确
- [ ] 浏览器控制台没有 CORS 错误

## 🔄 如果还是不行

1. **重启两个服务**：
   - 停止 FastAPI（Ctrl+C）
   - 停止 Next.js（Ctrl+C）
   - 重新启动两个服务

2. **清除浏览器缓存**：
   - 硬刷新：`Cmd+Shift+R` (Mac) 或 `Ctrl+Shift+R` (Windows)

3. **检查环境变量**：
   ```bash
   cd frontend
   cat .env.local
   ```
   应该看到：`NEXT_PUBLIC_API_URL=http://127.0.0.1:8000`

