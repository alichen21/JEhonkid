#!/bin/bash
# 部署脚本 - 部署到 space.ai-builders.com

API_TOKEN="sk_6e7ae450_dea1302ce81603cdb8ab92d53373de1e9c77"
API_BASE_URL="https://space.ai-builders.com/backend/v1"
DEPLOYMENT_ENDPOINT="${API_BASE_URL}/deployments"

# 从 deploy-config.json 读取配置（如果存在）
if [ -f "deploy-config.json" ]; then
    REPO_URL=$(grep -o '"repo_url": "[^"]*"' deploy-config.json | cut -d'"' -f4)
    SERVICE_NAME=$(grep -o '"service_name": "[^"]*"' deploy-config.json | cut -d'"' -f4)
    BRANCH=$(grep -o '"branch": "[^"]*"' deploy-config.json | cut -d'"' -f4)
    PORT=$(grep -o '"port": [0-9]*' deploy-config.json | grep -o '[0-9]*')
else
    # 默认值
    REPO_URL="https://github.com/alichen21/JEhonkid"
    SERVICE_NAME="jehonkid"
    BRANCH="main"
    PORT=8000
fi

echo "============================================================"
echo "部署到 space.ai-builders.com"
echo "============================================================"
echo "仓库 URL: $REPO_URL"
echo "服务名称: $SERVICE_NAME"
echo "Git 分支: $BRANCH"
echo "端口: $PORT"
echo "============================================================"
echo ""

# 调用部署 API
curl -X POST "$DEPLOYMENT_ENDPOINT" \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"repo_url\": \"$REPO_URL\",
    \"service_name\": \"$SERVICE_NAME\",
    \"branch\": \"$BRANCH\",
    \"port\": $PORT
  }" | python3 -m json.tool

echo ""
echo "============================================================"
echo "部署请求已提交！"
echo "服务将在以下地址可用: https://${SERVICE_NAME}.ai-builders.space/"
echo "部署通常需要 5-10 分钟完成"
echo "============================================================"




