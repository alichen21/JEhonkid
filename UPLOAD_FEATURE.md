# 文件上传功能说明

## 新增功能

### 1. 文件上传 API
- **路由**: `POST /api/upload`
- **功能**: 支持通过HTTP上传图片文件
- **支持格式**: PNG, JPG, JPEG, HEIC, HEIF, GIF, BMP
- **文件大小限制**: 10MB
- **返回**: 任务ID，用于后续查询处理结果

### 2. 任务状态查询 API
- **路由**: `GET /api/task/<task_id>`
- **功能**: 查询任务的处理状态和结果
- **状态**: pending, processing, completed, failed
- **进度**: OCR识别、文本处理、TTS生成三个阶段的进度

### 3. 后台异步处理
- **实现方式**: Flask 后台线程
- **处理流程**: 
  1. OCR识别 → 
  2. LLM文本处理 → 
  3. TTS语音生成
- **特点**: 
  - 无需数据库，使用内存存储任务状态
  - 任务自动过期（1小时）
  - 支持并发处理多个任务

### 4. 移动端上传页面
- **路由**: `/upload`
- **功能**: 
  - 支持拍照上传（iPhone/iPad）
  - 支持拖拽上传
  - 实时进度显示
  - 结果展示（文本+音频）

## 使用方式

### 方式1: Web界面上传
1. 访问 `http://127.0.0.1:5000/upload`
2. 点击上传区域或拖拽图片
3. 点击"开始处理"按钮
4. 等待处理完成，查看结果

### 方式2: API调用
```python
import requests

# 上传文件
files = {'file': open('image.jpg', 'rb')}
response = requests.post('http://127.0.0.1:5000/api/upload', files=files)
data = response.json()
task_id = data['task_id']

# 查询任务状态
response = requests.get(f'http://127.0.0.1:5000/api/task/{task_id}')
status = response.json()
print(status['status'])  # pending, processing, completed, failed
```

## 文件存储

- **用户上传文件**: `static/uploads/`
- **生成的音频**: `static/audio/`
- **原始图片库**: `Picture books/` (保持不变)

## 技术实现

### 任务管理器 (`task_manager.py`)
- 内存存储任务状态
- 线程安全的任务状态更新
- 自动清理过期任务

### 后台处理函数 (`process_image_task`)
- 在独立线程中执行
- 分阶段更新任务状态
- 错误处理和异常捕获

## 注意事项

1. **内存限制**: 任务存储在内存中，服务器重启后任务会丢失
2. **并发处理**: 支持多个任务同时处理，但受限于服务器资源
3. **任务过期**: 任务1小时后自动清理
4. **文件清理**: 上传的文件和生成的音频文件需要手动清理（未来可添加自动清理）

## 未来改进方向

1. 添加数据库持久化（SQLite/PostgreSQL）
2. 实现任务队列（Celery + Redis）
3. 添加文件自动清理机制
4. 支持批量上传
5. 添加用户认证和会话管理

