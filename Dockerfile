# 多阶段构建 Dockerfile
# 阶段1: 构建前端
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# 复制前端依赖文件
COPY frontend/package*.json ./

# 安装前端依赖
RUN npm ci

# 复制前端源代码
COPY frontend/ ./

# 构建前端（静态导出）
RUN npm run build

# 阶段2: Python 运行时
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖（用于图片处理等）
# Pillow 通常不需要 OpenGL 库，如果后续需要可以添加
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 复制 Python 依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY *.py ./

# 从构建阶段复制前端静态文件
COPY --from=frontend-builder /app/frontend/out ./frontend/out

# 创建必要的目录
RUN mkdir -p static/uploads static/audio "Picture books"

# 暴露端口（PORT 环境变量会在运行时设置）
EXPOSE 8000

# 使用 shell 形式确保环境变量正确展开
CMD sh -c "uvicorn app_fastapi:app --host 0.0.0.0 --port ${PORT:-8000}"

