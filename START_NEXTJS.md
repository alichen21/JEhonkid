# 🚀 手动启动 Next.js 前端

由于自动启动可能遇到权限问题，请按照以下步骤手动启动：

## 步骤 1: 打开终端

打开一个新的终端窗口。

## 步骤 2: 进入前端目录

```bash
cd /Users/yurong/Desktop/AI编程练手/AI\ architect/JKid/frontend
```

## 步骤 3: 检查依赖

```bash
# 检查 node_modules 是否存在
ls -la node_modules

# 如果不存在，安装依赖
npm install
```

## 步骤 4: 检查环境变量

```bash
# 检查 .env.local 文件
cat .env.local

# 如果不存在或内容不对，创建/更新它
echo "NEXT_PUBLIC_API_URL=http://127.0.0.1:8000" > .env.local
```

## 步骤 5: 启动 Next.js 开发服务器

```bash
npm run dev
```

你应该看到类似这样的输出：
```
- ready started server on 0.0.0.0:3000
- Local:        http://localhost:3000
- Network:      http://192.168.x.x:3000
```

## 步骤 6: 访问应用

在浏览器中打开：http://localhost:3000

## ⚠️ 常见问题

### 问题 1: 端口 3000 被占用

如果看到端口被占用的错误：

```bash
# 查找占用端口的进程
lsof -ti:3000

# 杀死进程（替换 PID 为实际进程号）
kill -9 <PID>

# 或者使用其他端口启动
PORT=3001 npm run dev
```

### 问题 2: 依赖安装失败

```bash
# 清理并重新安装
rm -rf node_modules package-lock.json
npm install
```

### 问题 3: 编译错误

```bash
# 清理 Next.js 缓存
rm -rf .next
npm run dev
```

### 问题 4: 无法连接到 FastAPI 后端

确保：
1. FastAPI 后端正在运行（另一个终端）
2. 检查 http://127.0.0.1:8000/docs 可以访问
3. `.env.local` 中的 `NEXT_PUBLIC_API_URL` 配置正确

## 📝 同时运行两个服务

你需要**两个终端窗口**：

**终端 1 - FastAPI 后端：**
```bash
cd /Users/yurong/Desktop/AI编程练手/AI\ architect/JKid
python3 app_fastapi.py
```

**终端 2 - Next.js 前端：**
```bash
cd /Users/yurong/Desktop/AI编程练手/AI\ architect/JKid/frontend
npm run dev
```

## ✅ 验证

两个服务都启动后：

- ✅ FastAPI: http://127.0.0.1:8000/docs
- ✅ Next.js: http://localhost:3000

两个地址都应该可以正常访问！

