# 文件清单 - 部署前检查

## ✅ 应该保留的文件（需要提交到 Git）

### 后端代码
- `app_fastapi.py` - FastAPI 主应用
- `picture_to_text.py` - OCR 功能模块
- `text_processor.py` - 文本处理模块
- `text_to_speech.py` - TTS 功能模块
- `task_manager.py` - 任务管理器
- `requirements.txt` - Python 依赖

### 前端代码
- `frontend/app/` - Next.js App Router 源代码
- `frontend/components/` - React 组件
- `frontend/lib/` - 工具库和 Hooks
- `frontend/styles/` - 样式文件
- `frontend/package.json` - 前端依赖配置
- `frontend/package-lock.json` - 依赖锁定文件
- `frontend/tsconfig.json` - TypeScript 配置
- `frontend/next.config.js` - Next.js 配置
- `frontend/next-env.d.ts` - Next.js 类型定义
- `frontend/README.md` - 前端说明文档

### 测试文件
- `tests/` - 测试目录（包括所有测试文件）
- `test_fastapi.py` - FastAPI 测试

### 脚本文件
- `scripts/` - 所有脚本文件
- `start_fastapi.sh` - 启动脚本
- `restart_fastapi.sh` - 重启脚本
- `check_services.sh` - 检查服务脚本
- `deploy.sh` - 部署脚本

### 配置文件
- `Dockerfile` - Docker 配置
- `deploy-config.json.example` - 部署配置示例
- `.gitignore` - Git 忽略规则

### 文档
- `README.md` - 项目主文档
- `docs/` - 文档目录
- `CLEANUP_GUIDE.md` - 清理指南
- `DEPLOYMENT_EXPLANATION.md` - 部署说明
- `DEPLOYMENT_ISSUES.md` - 部署问题记录
- `FILES_CHECKLIST.md` - 本文件

### 静态资源（部分）
- `static/css/` - CSS 样式文件（代码的一部分）
- `templates/` - HTML 模板（如果使用）

---

## ❌ 不应该保留的文件（已在 .gitignore 中）

### Python 相关
- `venv/` - Python 虚拟环境
- `__pycache__/` - Python 缓存文件
- `*.pyc`, `*.pyo`, `*.pyd` - Python 编译文件
- `*.egg-info/` - Python 包信息

### Node.js 相关
- `frontend/node_modules/` - Node.js 依赖
- `frontend/.next/` - Next.js 构建缓存
- `frontend/out/` - Next.js 构建输出（生产环境会重新构建）

### 运行时生成的文件
- `static/uploads/` - 用户上传的图片（运行时生成）
- `static/audio/` - 生成的音频文件（运行时生成）

### 示例/测试数据
- `Picture books/` - 示例图片（可选，建议不提交）

### 环境变量和密钥
- `.env` - 环境变量文件（包含敏感信息）
- `deploy-config.json` - 实际部署配置（包含敏感信息）

### IDE 和系统文件
- `.vscode/`, `.idea/` - IDE 配置
- `.DS_Store` - macOS 系统文件
- `Thumbs.db` - Windows 系统文件

### 日志文件
- `*.log` - 日志文件
- `npm-debug.log*` - npm 调试日志

---

## 📋 部署前检查清单

在重新部署到 GitHub 之前，请确认：

- [ ] 所有源代码文件都已保存
- [ ] `.env` 文件已添加到 .gitignore（不提交）
- [ ] `deploy-config.json` 已添加到 .gitignore（不提交）
- [ ] `venv/` 目录不会被提交
- [ ] `frontend/node_modules/` 不会被提交
- [ ] `static/uploads/` 和 `static/audio/` 不会被提交
- [ ] 所有必要的配置文件都已包含（requirements.txt, package.json 等）
- [ ] README.md 文档是最新的

---

## 🚀 重新部署步骤

1. **清理本地 Git 状态**（如果需要）
   ```bash
   git status
   git clean -fd  # 删除未跟踪的文件（谨慎使用）
   ```

2. **检查 .gitignore 是否生效**
   ```bash
   git status --ignored  # 查看被忽略的文件
   ```

3. **初始化新的 Git 仓库**（如果删除了远程仓库）
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

4. **连接到新的 GitHub 仓库**
   ```bash
   git remote add origin <your-new-repo-url>
   git push -u origin main
   ```

5. **本地测试**
   ```bash
   # 启动后端
   ./scripts/start_fastapi.sh
   
   # 启动前端（新终端）
   cd frontend && npm install && npm run dev
   ```

