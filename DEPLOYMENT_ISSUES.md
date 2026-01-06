# 部署失败问题分析

## ✅ 当前状态确认

### 1. 前端配置
- **是静态前端**：`next.config.js` 中已配置 `output: 'export'`
- Next.js 14 会在构建时自动生成 `out` 目录（静态文件）
- 配置正确 ✅

### 2. Dockerfile 配置
- ✅ 使用多阶段构建
- ✅ CMD 使用 shell 形式：`CMD sh -c "uvicorn app_fastapi:app --host 0.0.0.0 --port ${PORT:-8000}"`
- ✅ 正确复制前端静态文件：`COPY --from=frontend-builder /app/frontend/out ./frontend/out`
- ✅ 暴露端口：`EXPOSE 8000`

### 3. 应用代码
- ✅ 正确读取 PORT 环境变量：`port = int(os.getenv("PORT", "8000"))`
- ✅ 前端静态文件挂载逻辑存在

## 🔍 可能的问题

### 问题 1: 前端构建可能失败
**症状**：如果 Next.js 构建失败，`out` 目录可能不存在

**检查方法**：
```bash
# 本地测试构建
cd frontend
npm ci
npm run build
ls -la out/  # 检查是否生成了 out 目录
```

**解决方案**：
- 确保 `frontend/package.json` 中的依赖版本兼容
- 检查是否有构建错误

### 问题 2: 路径问题
**可能的问题**：
- Dockerfile 中复制路径：`COPY --from=frontend-builder /app/frontend/out ./frontend/out`
- 应用代码中路径：`FRONTEND_BUILD_DIR = Path("frontend/out")`

**检查**：路径应该匹配 ✅

### 问题 3: 内存限制
根据部署指南，容器只有 **256 MB RAM**。如果构建或运行时内存不足，会导致失败。

**解决方案**：
- 优化 Dockerfile，减少镜像大小
- 确保没有不必要的依赖

### 问题 4: 环境变量缺失 ⚠️ **关键问题**
**问题**：
- `PictureToText()` 和 `TextProcessor()` 在应用启动时就会初始化
- 如果没有 `GOOGLE_CLOUD_API_KEY` 和 `SUPER_MIND_API_KEY`，应用会直接崩溃
- 部署平台只注入 `AI_BUILDER_TOKEN`，不会自动设置其他环境变量

**当前代码问题**：
```python
# app_fastapi.py 第 104-105 行
ocr = PictureToText()  # 如果没有 GOOGLE_CLOUD_API_KEY 会抛出异常
text_processor = TextProcessor()  # 如果没有 SUPER_MIND_API_KEY 会抛出异常
```

**解决方案**：
1. 修改初始化逻辑，使用 try-except 包裹，允许应用在没有环境变量时启动
2. 或者修改 `TextProcessor` 使用 `AI_BUILDER_TOKEN`（根据部署指南，这是注入的 token）
3. 在部署配置中设置必要的环境变量

### 问题 5: 依赖安装失败
**可能的问题**：
- `npm ci` 或 `pip install` 可能因为网络问题失败
- 某些依赖版本不兼容

**解决方案**：
- 确保 `package.json` 和 `requirements.txt` 中的版本固定
- 使用 `npm ci` 而不是 `npm install`（已在 Dockerfile 中使用）✅

### 问题 6: 静态文件服务顺序
**检查**：FastAPI 中静态文件挂载的顺序很重要
- `/static` 挂载 ✅
- `/_next` 挂载 ✅  
- catch-all 路由在最后 ✅

## ✅ 已修复的问题

### 修复 1: 环境变量处理
- ✅ 修改 `text_processor.py` 支持 `AI_BUILDER_TOKEN`（部署平台注入的 token）
- ✅ 修改 `app_fastapi.py` 使用 try-except 包裹模块初始化，允许应用在没有环境变量时启动
- ✅ 添加 None 检查，确保在使用模块前验证是否已初始化

### 修复 2: 应用启动健壮性
- ✅ OCR 和文本处理模块初始化失败不会导致应用崩溃
- ✅ API 端点会返回适当的错误信息而不是崩溃

## 🛠️ 建议的修复步骤

### 步骤 1: 提交修复
```bash
git add .
git commit -m "Fix deployment issues: support AI_BUILDER_TOKEN and graceful initialization"
git push
```

### 步骤 2: 本地测试 Docker 构建（推荐）
```bash
# 构建镜像
docker build -t jkid-test .

# 运行容器（测试没有环境变量的情况）
docker run -p 8000:8000 -e PORT=8000 jkid-test

# 运行容器（测试有环境变量的情况）
docker run -p 8000:8000 -e PORT=8000 -e AI_BUILDER_TOKEN=test_token jkid-test
```

### 步骤 3: 检查构建日志
如果部署失败，查看部署日志中的错误信息：
- 前端构建是否成功？
- Python 依赖安装是否成功？
- 应用启动时是否有错误？

### 步骤 4: 优化 Dockerfile（如果需要）
如果内存不足，可以考虑：
- 使用更小的基础镜像
- 清理构建缓存
- 减少不必要的依赖

## 📋 部署前检查清单

- [x] 所有代码已提交并推送到 GitHub
- [x] Dockerfile 存在于根目录
- [x] `requirements.txt` 存在且包含所有依赖
- [x] `frontend/package.json` 存在且依赖版本固定
- [x] `next.config.js` 配置了 `output: 'export'`
- [x] Dockerfile CMD 使用 shell 形式展开 PORT
- [x] 应用代码读取 PORT 环境变量
- [x] 应用支持 `AI_BUILDER_TOKEN` 环境变量
- [x] 应用能在没有环境变量时优雅启动
- [ ] 本地可以成功构建 Docker 镜像（可选但推荐）

## 🎯 关于环境变量

根据部署指南，部署平台会注入 `AI_BUILDER_TOKEN`。应用现在：
- ✅ `TextProcessor` 可以使用 `AI_BUILDER_TOKEN` 或 `SUPER_MIND_API_KEY`
- ✅ `PictureToText` 仍需要 `GOOGLE_CLOUD_API_KEY`（这是 Google Cloud 的 API，不是平台提供的）
- ✅ 如果缺少环境变量，应用仍能启动，但相关功能会不可用

**注意**：`GOOGLE_CLOUD_API_KEY` 需要在部署配置中手动设置，或者通过其他方式提供。

## 🔗 相关文档

- [部署指南](./DEPLOYMENT_EXPLANATION.md)
- [Space.ai-builder 部署指南](https://www.ai-builders.com/resources/students-backend/openapi.json)

