#!/bin/bash

echo "============================================================"
echo "检查服务状态"
echo "============================================================"

# 检查 FastAPI 后端
echo -n "FastAPI 后端 (http://127.0.0.1:8000): "
if curl -s http://127.0.0.1:8000/ > /dev/null 2>&1; then
    echo "✅ 运行中"
    echo "   API 文档: http://127.0.0.1:8000/docs"
else
    echo "❌ 未运行"
    echo "   启动命令: python3 app_fastapi.py"
fi

echo ""

# 检查 Next.js 前端
echo -n "Next.js 前端 (http://localhost:3000): "
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ 运行中"
    echo "   访问地址: http://localhost:3000"
else
    echo "❌ 未运行"
    echo "   启动命令: cd frontend && npm run dev"
fi

echo ""
echo "============================================================"




