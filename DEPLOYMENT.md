# 部署指南 - JKid 到 space.ai_builder

## 前置要求

1. **GitHub 公开仓库** - 代码必须推送到 GitHub
2. **环境变量** - 需要配置 API 密钥
3. **AI_BUILDER_TOKEN** - 部署时会自动注入，无需手动配置

## 部署步骤

### 1. 准备 GitHub 仓库

```bash
# 初始化 Git 仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交更改
git commit -m "Prepare for deployment to space.ai_builder"

# 在 GitHub 上创建新仓库，然后推送
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 2. 配置部署信息

复制 `deploy-config.json.example` 为 `deploy-config.json`：

```bash
cp deploy-config.json.example deploy-config.json
```

编辑 `deploy-config.json`，填入：
- `repo_url`: 你的 GitHub 仓库 URL
- `service_name`: 服务名称（将成为 `https://your-service-name.ai-builders.space`）
- `branch`: Git 分支（通常是 `main`）
- `env_vars`: 环境变量（API 密钥等）

**重要**: `deploy-config.json` 包含敏感信息，不要提交到 Git！

### 3. 部署

部署可以通过以下方式：

#### 方式1: 使用 AI 助手部署

告诉 AI 助手："请帮我部署到 space.ai_builder"，AI 会读取 `deploy-config.json` 并执行部署。

#### 方式2: 使用 API 直接部署

```python
import requests
import json
import os

# 读取部署配置
with open('deploy-config.json', 'r') as f:
    config = json.load(f)

# 获取 AI_BUILDER_TOKEN（从环境变量）
token = os.getenv('AI_BUILDER_TOKEN')
if not token:
    raise ValueError("请设置 AI_BUILDER_TOKEN 环境变量")

# 调用部署 API
response = requests.post(
    'https://space.ai-builders.com/backend/v1/deployments',
    headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    },
    json=config
)

print(response.json())
```

### 4. 检查部署状态

部署需要 5-10 分钟。可以通过以下方式检查：

```python
import requests
import os

token = os.getenv('AI_BUILDER_TOKEN')
service_name = "your-service-name"  # 替换为你的服务名称

response = requests.get(
    f'https://space.ai-builders.com/backend/v1/deployments/{service_name}',
    headers={'Authorization': f'Bearer {token}'}
)

print(response.json())
```

## 环境变量说明

### 必需的环境变量

- `GOOGLE_CLOUD_API_KEY`: Google Cloud Vision API 密钥（用于 OCR）
- `OPENAI_API_KEY`: OpenAI API 密钥（用于文本处理，如果使用 OpenAI）

### 自动注入的环境变量

- `AI_BUILDER_TOKEN`: 部署时自动注入，无需手动配置
- `PORT`: 由 Koyeb 自动设置，应用会自动读取

## 注意事项

1. **公开仓库**: 代码必须是公开的 GitHub 仓库
2. **不要提交敏感信息**: `.env`、`deploy-config.json` 等文件不要提交到 Git
3. **单进程限制**: 应用必须运行在单进程单端口模式下（已配置）
4. **资源限制**: 容器有 256MB RAM 限制，注意优化
5. **文件持久化**: `static/uploads` 和 `static/audio` 目录的文件在容器重启后会丢失

## 故障排查

### 部署失败

1. 检查 GitHub 仓库是否为公开
2. 检查 Dockerfile 是否存在且正确
3. 检查分支名称是否正确
4. 查看部署日志：`GET /v1/deployments/{service_name}/logs`

### 应用无法启动

1. 检查环境变量是否正确设置
2. 检查端口是否正确读取（应用会自动读取 PORT 环境变量）
3. 查看运行时日志

## 更新部署

修改代码后，重新提交到 GitHub：

```bash
git add .
git commit -m "Update code"
git push
```

然后重新部署（使用相同的 `service_name` 会更新现有部署）。

