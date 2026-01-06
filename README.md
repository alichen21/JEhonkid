# 亲子日语可理解输入助手 - MVP

## 项目简介

一个面向不会日语的家长的亲子学习助手：通过拍照，把绘本中的日语内容转化为"可听、可懂"的输入。

## 当前功能

### ✅ Picture to Text (图片转文字)

使用 Google Cloud Vision API 进行日语OCR识别。

### ✅ Web可视化界面

通过Web界面查看所有图片的OCR识别结果，包括：
- 图片预览
- 文件名显示
- 完整识别文本
- 文本块列表（带置信度）
- 语言检测结果

### ✅ LLM文本处理与翻译

使用 space.ai-builders.com 的 grok-4-fast 模型对OCR结果进行智能处理：
- **去噪**：删除页码、教材级别（如4A）、水印等无关信息
- **去重**：删除重复的注音假名
- **合并**：将断行合并为自然的句子
- **翻译**：生成适合家长阅读的中文翻译
- 输出两个版本：清理后的日语正文 + 中文翻译

#### 功能特点

- **支持两种检测模式**：
  - `TEXT_DETECTION`: 通用文本检测
  - `DOCUMENT_TEXT_DETECTION`: 文档文本检测（推荐用于打印文本，支持复杂布局）
  
- **日语优化**：
  - 自动检测日语内容
  - 支持横排和竖排文本
  - 支持手写体和印刷体

#### 使用方法

```python
from picture_to_text import PictureToText

# 初始化
ocr = PictureToText()

# 识别图片中的文本
result = ocr.extract_text("Picture books/Kumon test.png")

# 获取完整文本
print(result['full_text'])

# 获取文本块列表
for block in result['text_blocks']:
    print(block['text'])
```

#### 测试

**命令行测试：**
```bash
source venv/bin/activate
python picture_to_text.py
```

**Web界面测试：**

方式1 - 使用启动脚本（推荐）：
```bash
# macOS/Linux
./start_web.sh

# Windows
start_web.bat
```

方式2 - 手动启动：
```bash
source venv/bin/activate  # Windows: venv\Scripts\activate
python app.py
```

启动后，在浏览器中访问：**http://127.0.0.1:5000**

Web界面会显示：
- 📊 统计信息（总图片数、成功/失败数）
- 🖼️ 所有图片的预览
- 📝 每张图片的OCR识别结果
- 🏷️ 语言检测信息

## 环境设置

1. 创建虚拟环境（已完成）：
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置API密钥：
   - 复制 `.env.example` 为 `.env`
   - 在 `.env` 中填入你的 API 密钥

## Google Cloud Vision API 功能说明

### 可用的检测类型

1. **TEXT_DETECTION**
   - 通用文本检测
   - 适合简单场景
   - 返回文本和边界框

2. **DOCUMENT_TEXT_DETECTION** (推荐)
   - 文档文本检测
   - 更适合打印文本
   - 支持复杂布局
   - 返回结构化文本（页面、段落、单词、符号）
   - 提供置信度信息

### API限制

- 免费额度：每月前1000次请求免费
- 图片大小：最大20MB
- 支持格式：JPEG, PNG, GIF, BMP, WEBP

## 项目结构

```
JKid/
├── Picture books/          # 示例图片
├── templates/              # HTML模板
│   └── index.html         # 主页面模板
├── static/                 # 静态文件
│   └── css/
│       └── style.css       # 样式文件
├── venv/                   # 虚拟环境
├── .env                    # 环境变量（不提交到Git）
├── .env.example            # 环境变量模板
├── .gitignore             # Git忽略文件
├── requirements.txt        # Python依赖
├── app.py                 # Flask Web应用
├── picture_to_text.py      # Picture to Text功能模块
├── test_ocr.py            # OCR测试脚本
├── example_usage.py        # API密钥使用示例
└── README.md              # 项目说明文档
```

## 功能说明

### OCR识别流程

1. **图片上传** → 自动扫描 `Picture books/` 文件夹
2. **OCR识别** → 使用Google Cloud Vision API识别日语文本
3. **LLM处理** → 使用grok-4-fast模型清理和翻译文本
4. **结果展示** → 在Web界面显示原始文本和处理后的结果

### LLM处理功能

文本处理器会自动：
- 清理OCR识别中的噪音（页码、级别标识等）
- 合并断行的文本为完整句子
- 生成自然流畅的日语正文
- 提供准确的中文翻译供家长参考

## 下一步开发计划

- [x] OCR识别功能
- [x] Web可视化界面
- [x] LLM文本处理与翻译
- [ ] TTS功能（文本转语音）
- [ ] 移动端优化
- [ ] 批量处理功能

