# 测试文件说明

本目录包含项目的测试脚本。

## 测试文件列表

### test_ocr.py
测试 OCR 功能，验证图片文字识别是否正常工作。

**使用方法：**
```bash
# 测试所有示例图片
python tests/test_ocr.py

# 测试指定图片
python tests/test_ocr.py "Picture books/your_image.png"
```

### test_fastapi.py
测试 FastAPI 后端服务是否正常运行。

**使用方法：**
```bash
# 确保 FastAPI 服务正在运行
python tests/test_fastapi.py
```

### test_segmentation.py
测试文本分段功能和指导语识别。

**使用方法：**
```bash
python tests/test_segmentation.py
```

## 注意事项

- 运行测试前确保已安装所有依赖：`pip install -r requirements.txt`
- 某些测试需要配置环境变量（如 API 密钥）
- 测试文件会自动添加项目根目录到 Python 路径

