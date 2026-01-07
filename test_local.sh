#!/bin/bash

# 本地测试脚本
# 用于验证项目配置是否正确

set -e

echo "============================================================"
echo "本地测试 - 检查项目配置"
echo "============================================================"

# 1. 检查 Python 环境
echo ""
echo "1. 检查 Python 环境..."
python3 --version
if [ -d "venv" ]; then
    echo "✅ 虚拟环境存在"
else
    echo "⚠️  虚拟环境不存在，需要创建"
fi

# 2. 检查 Python 依赖
echo ""
echo "2. 检查 Python 依赖..."
if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt 存在"
    if [ -d "venv" ]; then
        source venv/bin/activate
        echo "已激活虚拟环境，检查关键依赖..."
        python3 -c "import fastapi; print('✅ FastAPI')" 2>/dev/null || echo "❌ FastAPI 未安装"
        python3 -c "import uvicorn; print('✅ uvicorn')" 2>/dev/null || echo "❌ uvicorn 未安装"
        python3 -c "from google.cloud import vision; print('✅ google-cloud-vision')" 2>/dev/null || echo "❌ google-cloud-vision 未安装"
        python3 -c "from PIL import Image; print('✅ Pillow')" 2>/dev/null || echo "❌ Pillow 未安装"
        deactivate
    fi
else
    echo "❌ requirements.txt 不存在"
fi

# 3. 检查前端环境
echo ""
echo "3. 检查前端环境..."
if [ -d "frontend" ]; then
    echo "✅ frontend 目录存在"
    if [ -f "frontend/package.json" ]; then
        echo "✅ package.json 存在"
        if [ -d "frontend/node_modules" ]; then
            echo "✅ node_modules 存在"
            cd frontend
            if command -v npm &> /dev/null; then
                echo "检查关键依赖..."
                npm list next 2>/dev/null | grep -q "next@" && echo "✅ Next.js" || echo "❌ Next.js 未安装"
                npm list react 2>/dev/null | grep -q "react@" && echo "✅ React" || echo "❌ React 未安装"
            fi
            cd ..
        else
            echo "⚠️  node_modules 不存在，需要运行: cd frontend && npm install"
        fi
    else
        echo "❌ package.json 不存在"
    fi
else
    echo "❌ frontend 目录不存在"
fi

# 4. 检查关键文件
echo ""
echo "4. 检查关键文件..."
[ -f "app_fastapi.py" ] && echo "✅ app_fastapi.py" || echo "❌ app_fastapi.py"
[ -f "picture_to_text.py" ] && echo "✅ picture_to_text.py" || echo "❌ picture_to_text.py"
[ -f "text_processor.py" ] && echo "✅ text_processor.py" || echo "❌ text_processor.py"
[ -f "text_to_speech.py" ] && echo "✅ text_to_speech.py" || echo "❌ text_to_speech.py"
[ -f "task_manager.py" ] && echo "✅ task_manager.py" || echo "❌ task_manager.py"
[ -f ".gitignore" ] && echo "✅ .gitignore" || echo "❌ .gitignore"

# 5. 检查目录结构
echo ""
echo "5. 检查目录结构..."
[ -d "static" ] && echo "✅ static/" || echo "⚠️  static/ 不存在（会自动创建）"
[ -d "static/uploads" ] && echo "✅ static/uploads/" || echo "⚠️  static/uploads/ 不存在（会自动创建）"
[ -d "static/audio" ] && echo "✅ static/audio/" || echo "⚠️  static/audio/ 不存在（会自动创建）"
[ -d "scripts" ] && echo "✅ scripts/" || echo "❌ scripts/ 不存在"

# 6. 检查环境变量文件
echo ""
echo "6. 检查环境变量配置..."
if [ -f ".env" ]; then
    echo "✅ .env 文件存在"
    if grep -q "GOOGLE_CLOUD_API_KEY" .env 2>/dev/null; then
        echo "✅ GOOGLE_CLOUD_API_KEY 已配置"
    else
        echo "⚠️  GOOGLE_CLOUD_API_KEY 未配置"
    fi
    if grep -q "AI_BUILDER_TOKEN\|SUPER_MIND_API_KEY" .env 2>/dev/null; then
        echo "✅ LLM API Key 已配置"
    else
        echo "⚠️  LLM API Key 未配置"
    fi
else
    echo "⚠️  .env 文件不存在，需要创建并配置 API 密钥"
fi

# 7. 检查 Git 状态
echo ""
echo "7. 检查 Git 状态..."
if [ -d ".git" ]; then
    echo "✅ Git 仓库已初始化"
    echo "被忽略的文件（应该包含 venv/, node_modules/, static/uploads/ 等）:"
    git status --ignored 2>/dev/null | grep -E "venv/|node_modules/|static/(uploads|audio)/" | head -5 || echo "  (无)"
else
    echo "⚠️  Git 仓库未初始化"
fi

echo ""
echo "============================================================"
echo "测试完成！"
echo "============================================================"
echo ""
echo "下一步："
echo "1. 如果依赖未安装，运行:"
echo "   - 后端: source venv/bin/activate && pip install -r requirements.txt"
echo "   - 前端: cd frontend && npm install"
echo ""
echo "2. 启动服务："
echo "   - 后端: ./scripts/start_fastapi.sh"
echo "   - 前端: cd frontend && npm run dev"
echo ""
echo "3. 访问："
echo "   - API 文档: http://127.0.0.1:8000/docs"
echo "   - 前端: http://localhost:3000"
echo "============================================================"

