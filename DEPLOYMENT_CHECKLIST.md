# 部署前检查清单

## ✅ 已完成的工作

1. **文件清单梳理** - 已创建 `FILES_CHECKLIST.md`
2. **.gitignore 优化** - 已修复，确保 `frontend/lib/` 和 `frontend/next-env.d.ts` 不被忽略
3. **测试脚本** - 已创建 `test_local.sh`

## 📋 文件分类总结

### ✅ 需要提交到 Git 的文件

#### 后端代码
- `app_fastapi.py`
- `picture_to_text.py`
- `text_processor.py`
- `text_to_speech.py`
- `task_manager.py`
- `requirements.txt`

#### 前端代码
- `frontend/app/` - 所有源代码
- `frontend/components/` - 所有组件
- `frontend/lib/` - 工具库（已修复，不再被忽略）
- `frontend/styles/` - 样式文件
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/tsconfig.json`
- `frontend/next.config.js`
- `frontend/next-env.d.ts` - 类型定义（已修复，不再被忽略）

#### 测试和脚本
- `tests/` - 所有测试文件
- `scripts/` - 所有脚本文件
- `test_local.sh` - 本地测试脚本

#### 配置文件
- `Dockerfile`
- `deploy-config.json.example` - 示例配置（不包含敏感信息）
- `.gitignore` - Git 忽略规则

#### 文档
- `README.md`
- `docs/` - 所有文档
- `FILES_CHECKLIST.md` - 文件清单
- `DEPLOYMENT_CHECKLIST.md` - 本文件

### ❌ 不应该提交的文件（已在 .gitignore 中）

- `venv/` - Python 虚拟环境
- `__pycache__/` - Python 缓存
- `frontend/node_modules/` - Node.js 依赖
- `frontend/.next/` - Next.js 构建缓存
- `frontend/out/` - Next.js 构建输出
- `static/uploads/` - 用户上传的文件
- `static/audio/` - 生成的音频文件
- `Picture books/` - 示例图片（可选）
- `.env` - 环境变量（包含敏感信息）
- `deploy-config.json` - 实际部署配置（包含敏感信息）
- `.DS_Store` - macOS 系统文件

## 🧪 本地测试步骤

### 1. 检查环境

```bash
# 检查 Python 版本
python3 --version

# 检查 Node.js 版本（如果已安装）
node --version
npm --version
```

### 2. 安装依赖

```bash
# 后端依赖
source venv/bin/activate
pip install -r requirements.txt
deactivate

# 前端依赖
cd frontend
npm install
cd ..
```

### 3. 配置环境变量

创建 `.env` 文件（如果不存在）：

```bash
# 复制示例文件（如果有）
# cp .env.example .env

# 编辑 .env 文件，添加以下内容：
GOOGLE_CLOUD_API_KEY=your_google_cloud_api_key
AI_BUILDER_TOKEN=your_ai_builder_token
# 或
SUPER_MIND_API_KEY=your_super_mind_api_key
```

### 4. 运行测试脚本

```bash
# 运行本地测试脚本
bash test_local.sh
```

### 5. 启动服务

**终端 1 - 启动后端：**
```bash
./scripts/start_fastapi.sh
# 或
source venv/bin/activate
python app_fastapi.py
```

**终端 2 - 启动前端：**
```bash
cd frontend
npm run dev
```

### 6. 验证服务

- **后端 API 文档**: http://127.0.0.1:8000/docs
- **前端应用**: http://localhost:3000

## 🚀 重新部署到 GitHub

### ⚠️ 重要：处理已跟踪的敏感文件

如果 `deploy-config.json` 之前已经被 Git 跟踪，需要先从 Git 中移除（但保留本地文件）：

```bash
# 从 Git 中移除 deploy-config.json（但保留本地文件）
git rm --cached deploy-config.json

# 确认它现在被忽略
git check-ignore -v deploy-config.json
```

### 步骤 1: 检查 Git 状态

```bash
# 查看所有更改
git status

# 查看被忽略的文件（确认重要文件不被忽略）
git status --ignored | grep -E "frontend/lib|frontend/next-env"

# 确认 deploy-config.json 被忽略
git check-ignore -v deploy-config.json
```

### 步骤 2: 添加文件

```bash
# 添加所有应该提交的文件
git add .

# 添加 frontend/lib/ 和 frontend/next-env.d.ts（如果它们显示为未跟踪）
git add frontend/lib/ frontend/next-env.d.ts

# 检查将要提交的文件
git status
```

### 步骤 3: 提交更改

```bash
git commit -m "准备重新部署：优化 .gitignore，添加文件清单和测试脚本"
```

### 步骤 4: 连接到新的 GitHub 仓库

```bash
# 如果删除了远程仓库，添加新的远程仓库
git remote remove origin  # 如果存在
git remote add origin <your-new-repo-url>

# 推送到 GitHub
git push -u origin main
```

## ⚠️ 注意事项

1. **环境变量**: 确保 `.env` 文件不会被提交（已在 .gitignore 中）
2. **部署配置**: `deploy-config.json` 包含敏感信息，不要提交（已有示例文件）
3. **依赖安装**: 部署后需要在服务器上重新安装依赖
4. **前端构建**: 生产环境需要运行 `npm run build` 构建前端

## 📝 验证清单

在推送到 GitHub 之前，确认：

- [ ] `.env` 文件不在 Git 跟踪列表中
- [ ] `deploy-config.json` 不在 Git 跟踪列表中（只有 `.example` 版本）
- [ ] `venv/` 目录不在 Git 跟踪列表中
- [ ] `frontend/node_modules/` 不在 Git 跟踪列表中
- [ ] `frontend/lib/` 在 Git 跟踪列表中（源代码）
- [ ] `frontend/next-env.d.ts` 在 Git 跟踪列表中
- [ ] 所有源代码文件都已添加
- [ ] 所有配置文件都已添加
- [ ] 本地测试通过

## 🔍 快速检查命令

```bash
# 检查关键文件是否被正确忽略
git check-ignore -v venv/ frontend/node_modules/ .env deploy-config.json

# 检查关键文件是否被正确跟踪
git ls-files | grep -E "frontend/lib/|frontend/next-env.d.ts|app_fastapi.py|requirements.txt"

# 查看所有将被提交的文件
git status --short
```

