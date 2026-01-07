#!/bin/bash

echo "============================================================"
echo "重启 FastAPI 服务"
echo "============================================================"

# 停止可能运行的服务
echo "1. 停止现有服务..."
pkill -f "app_fastapi.py" 2>/dev/null || echo "   没有找到运行中的服务"

# 等待端口释放
sleep 2

# 启动 FastAPI 服务
echo "2. 启动 FastAPI 服务..."
echo "   API 地址: http://127.0.0.1:8000"
echo "   API 文档: http://127.0.0.1:8000/docs"
echo "   按 Ctrl+C 停止服务器"
echo "============================================================"

cd "$(dirname "$0")"
python3 app_fastapi.py




