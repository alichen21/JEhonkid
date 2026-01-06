# 🚀 快速启动指南

## 启动 Next.js 前端 + FastAPI 后端

由于需要同时运行两个服务，请按照以下步骤操作：

### 步骤 1: 安装 Next.js 前端依赖

```bash
cd frontend
npm install
```

如果遇到权限问题，可以尝试：
```bash
npm install --user
```

或者使用 yarn：
```bash
yarn install
```

### 步骤 2: 配置环境变量

在 `frontend` 目录下创建 `.env.local` 文件：

```bash
cd frontend
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
EOF
```

### 步骤 3: 启动服务

**终端 1 - 启动 FastAPI 后端：**
```bash
cd /Users/yurong/Desktop/AI编程练手/AI\ architect/JKid
python3 app_fastapi.py
```

等待看到：
```
启动 FastAPI 后端服务
API 地址: http://127.0.0.1:8000
```

**终端 2 - 启动 Next.js 前端：**
```bash
cd /Users/yurong/Desktop/AI编程练手/AI\ architect/JKid/frontend
npm run dev
```

等待看到：
```
- ready started server on 0.0.0.0:3000
- Local:        http://localhost:3000
```

### 步骤 4: 访问应用

- **Next.js 前端**: http://localhost:3000
- **FastAPI 后端 API**: http://127.0.0.1:8000
- **API 文档**: http://127.0.0.1:8000/docs

## ✅ 验证服务运行

### 检查 FastAPI 后端

在浏览器访问：http://127.0.0.1:8000/docs

应该看到 Swagger API 文档页面。

### 检查 Next.js 前端

在浏览器访问：http://localhost:3000

应该看到应用主页。

## 🔧 使用启动脚本（可选）

也可以使用提供的启动脚本：

**启动 FastAPI 后端：**
```bash
./start_fastapi.sh
```

**启动 Next.js 前端：**
```bash
cd frontend
./start.sh
```

## ⚠️ 常见问题

### 1. npm install 权限错误

如果遇到权限问题：
```bash
# 使用 --user 标志
npm install --user

# 或使用 yarn
yarn install

# 或使用 pnpm
pnpm install
```

### 2. 端口被占用

如果 3000 或 8000 端口被占用：

**检查端口占用：**
```bash
lsof -ti:3000  # Next.js
lsof -ti:8000  # FastAPI
```

**释放端口：**
```bash
kill -9 $(lsof -ti:3000)
kill -9 $(lsof -ti:8000)
```

### 3. 无法连接到 FastAPI 后端

确保：
1. FastAPI 后端正在运行（终端 1）
2. 检查 http://127.0.0.1:8000 是否可以访问
3. 检查 `.env.local` 中的 `NEXT_PUBLIC_API_URL` 配置

### 4. Next.js 编译错误

如果遇到 TypeScript 或编译错误：
```bash
# 清理缓存
rm -rf .next
rm -rf node_modules
npm install
npm run dev
```

## 📝 下一步

服务启动后，你可以：
1. 访问 http://localhost:3000 使用应用
2. 上传图片进行 OCR 识别
3. 查看处理结果和音频播放
4. 访问 http://127.0.0.1:8000/docs 查看 API 文档

## 🎉 完成！

现在你拥有了一个现代化的全栈应用：
- ✅ FastAPI 后端（高性能、自动文档）
- ✅ Next.js 前端（React、TypeScript）
- ✅ 完全前后端分离

享受开发吧！🚀

