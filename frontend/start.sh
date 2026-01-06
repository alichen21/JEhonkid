#!/bin/bash

# 启动 Next.js 前端开发服务器

echo "============================================================"
echo "启动 Next.js 前端开发服务器"
echo "============================================================"

# 检查 node_modules
if [ ! -d "node_modules" ]; then
    echo "📦 安装依赖..."
    npm install
fi

# 检查环境变量文件
if [ ! -f ".env.local" ]; then
    echo "⚠️  未找到 .env.local 文件"
    if [ -f ".env.local.example" ]; then
        echo "📝 从示例文件创建 .env.local..."
        cp .env.local.example .env.local
        echo "✅ 已创建 .env.local，请检查配置"
    else
        echo "⚠️  请手动创建 .env.local 文件"
    fi
fi

# 检查 FastAPI 后端是否运行
echo "🔍 检查 FastAPI 后端服务..."
if ! curl -s http://127.0.0.1:8000/ > /dev/null 2>&1; then
    echo "⚠️  警告: FastAPI 后端服务未运行"
    echo "   请先运行: python app_fastapi.py"
    echo "   或在另一个终端运行: ./start_fastapi.sh"
    echo ""
    read -p "是否继续启动 Next.js 前端? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 启动 Next.js 开发服务器
echo "🚀 启动 Next.js 前端..."
echo "前端地址: http://localhost:3000"
echo "FastAPI 后端: http://127.0.0.1:8000"
echo "按 Ctrl+C 停止服务器"
echo "============================================================"

npm run dev

