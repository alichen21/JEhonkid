# GitHub 仓库设置指南

## 快速开始

### 方式1: 使用脚本（推荐）

```bash
./prepare-github.sh
```

脚本会引导你完成：
1. 初始化 Git 仓库（如果还没有）
2. 配置远程仓库
3. 提交更改
4. 推送到 GitHub

### 方式2: 手动操作

#### 步骤 1: 在 GitHub 上创建仓库

1. 访问 https://github.com/new
2. 仓库名称：`jkid` 或 `jkid-app`（建议使用小写字母和连字符）
3. 设置为 **公开仓库（Public）**（必需！）
4. **不要**勾选 "Initialize this repository with a README"
5. 点击 "Create repository"

#### 步骤 2: 初始化本地 Git 仓库

```bash
# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交更改
git commit -m "Initial commit: Prepare for deployment"

# 添加远程仓库（替换 YOUR_USERNAME 和 YOUR_REPO_NAME）
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 设置默认分支为 main
git branch -M main

# 推送到 GitHub
git push -u origin main
```

## 重要文件说明

### 需要提交的文件 ✅

- `app_fastapi.py` - 后端代码
- `frontend/` - 前端代码（不包括 node_modules 和构建文件）
- `*.py` - 所有 Python 文件
- `requirements.txt` - Python 依赖
- `Dockerfile` - Docker 构建文件
- `README.md` - 项目说明
- `.gitignore` - Git 忽略规则

### 不要提交的文件 ❌

以下文件已在 `.gitignore` 中，不会提交：

- `.env` - 环境变量（包含 API 密钥）
- `venv/` - Python 虚拟环境
- `frontend/node_modules/` - Node.js 依赖
- `frontend/.next/` - Next.js 构建缓存
- `frontend/out/` - Next.js 静态导出文件（会在 Docker 中构建）
- `__pycache__/` - Python 缓存
- `static/uploads/` - 用户上传的文件
- `static/audio/` - 生成的音频文件

### 可选文件

- `deploy-config.json` - 部署配置（包含敏感信息，不要提交）
- `deploy-config.json.example` - 部署配置模板（可以提交）

## 验证设置

推送成功后，检查：

1. **仓库是公开的**: 访问 `https://github.com/YOUR_USERNAME/YOUR_REPO_NAME`，确认可以看到代码
2. **Dockerfile 存在**: 确认仓库根目录有 `Dockerfile` 文件
3. **分支名称**: 确认默认分支是 `main` 或 `master`

## 常见问题

### Q: 推送时提示需要认证？

A: GitHub 现在要求使用 Personal Access Token 或 SSH 密钥。可以：
- 使用 GitHub CLI: `gh auth login`
- 配置 SSH 密钥: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
- 使用 Personal Access Token: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

### Q: 如何更新代码？

A: 修改代码后：

```bash
git add .
git commit -m "描述你的更改"
git push
```

### Q: 忘记添加远程仓库？

A: 检查远程仓库：

```bash
git remote -v
```

如果没有，添加：

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

## 下一步

完成 GitHub 设置后：

1. 创建 `deploy-config.json`（从 `deploy-config.json.example` 复制）
2. 填入你的 GitHub 仓库 URL 和服务名称
3. 告诉 AI 助手："请帮我部署到 space.ai_builder"

