# 部署和 Repository 的关系说明

## 📚 基本概念

### Repository（代码仓库）
- **定义**：GitHub 上的代码仓库，包含你的所有源代码
- **作用**：存储和管理代码版本
- **位置**：`https://github.com/alichen21/JEhonkid`

### Deployment（部署）
- **定义**：将代码从 Repository 构建并运行在服务器上的过程
- **作用**：让应用可以通过互联网访问
- **位置**：`https://jehonkid.ai-builders.space/`

## 🔗 它们的关系

### 1. **部署系统会从 Repository 克隆代码**
```
部署流程：
Repository (GitHub) 
    ↓ (git clone)
部署服务器
    ↓ (Docker build)
构建镜像
    ↓ (运行容器)
在线服务
```

### 2. **Repository 必须包含所有必要文件**
部署系统会：
- ✅ 克隆你指定的分支（如 `main`）
- ✅ 读取 `Dockerfile` 来构建镜像
- ✅ 使用 Repository 中的代码和配置文件

### 3. **是否需要完全一样？**

**答案：是的！**

**原因：**
- 部署系统**只**从 Repository 读取代码
- 本地未提交的更改**不会**被部署
- Repository 中的代码必须**可以成功构建**

**重要规则：**
```
本地代码 ≠ Repository 代码 ≠ 部署的代码

只有 Repository 中的代码会被部署！
```

## ✅ 部署前的检查清单

1. **确保所有文件已提交**
   ```bash
   git status  # 检查是否有未提交的文件
   git add .   # 添加所有更改
   git commit -m "描述"  # 提交更改
   git push    # 推送到 GitHub
   ```

2. **确保 Dockerfile 存在且正确**
   - 必须在 Repository 根目录
   - 必须能成功构建

3. **确保所有依赖文件都在 Repository 中**
   - `requirements.txt` (Python)
   - `package.json` (Node.js)
   - 所有源代码文件

4. **确保没有敏感信息**
   - `.env` 文件**不应该**提交到 Repository
   - API 密钥应该通过环境变量注入

## 🚨 常见问题

### Q: 为什么本地能运行，但部署失败？
**A:** 可能是因为：
- 本地有未提交的文件
- 本地环境与 Docker 环境不同
- Repository 中缺少某些文件

### Q: 修改代码后需要重新部署吗？
**A:** 是的！步骤：
1. 修改代码
2. `git add .` 和 `git commit`
3. `git push` 推送到 GitHub
4. 调用部署 API 重新部署

### Q: 部署会使用哪个分支？
**A:** 部署时指定的分支（如 `main`）。确保该分支包含最新代码。

## 📝 当前项目配置

- **Repository URL**: `https://github.com/alichen21/JEhonkid`
- **分支**: `main`
- **服务名称**: `jehonkid`
- **部署 URL**: `https://jehonkid.ai-builders.space/`

## 🔧 部署命令

```bash
# 方式1: 使用部署脚本
./deploy.sh

# 方式2: 直接调用 API
curl -X POST "https://space.ai-builders.com/backend/v1/deployments" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/alichen21/JEhonkid",
    "service_name": "jehonkid",
    "branch": "main",
    "port": 8000
  }'
```




