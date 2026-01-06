"""
简单的OCR测试脚本
快速测试单张图片的识别效果
"""

import sys
import os
from picture_to_text import PictureToText

def test_single_image(image_path: str):
    """测试单张图片的OCR识别"""
    print(f"正在处理: {image_path}\n")
    
    ocr = PictureToText()
    
    try:
        # 使用DOCUMENT_TEXT_DETECTION（推荐用于打印文本）
        result = ocr.extract_text(image_path, detection_type="DOCUMENT_TEXT_DETECTION")
        
        if "error" in result:
            print(f"❌ 错误: {result['error']}")
            return
        
        print("=" * 60)
        print("识别结果:")
        print("=" * 60)
        print(f"\n完整文本:\n{result['full_text']}")
        print("\n" + "-" * 60)
        
        if result['text_blocks']:
            print(f"\n文本块数量: {len(result['text_blocks'])}")
            print("\n所有文本块:")
            for i, block in enumerate(result['text_blocks'], 1):
                text_preview = block['text'][:100] + "..." if len(block['text']) > 100 else block['text']
                confidence = block.get('confidence', 'N/A')
                print(f"  {i}. [{confidence:.2f}] {text_preview}")
        
        if result.get('language'):
            print(f"\n检测到的语言:")
            for lang in result['language']:
                print(f"  - {lang['languageCode']}: {lang['confidence']:.2%}")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"❌ 处理失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 使用命令行参数指定的图片
        image_path = sys.argv[1]
        test_single_image(image_path)
    else:
        # 测试所有图片，包括 Qiaohu1 和 Qiaohu2
        test_images = [
            "Picture books/Kumon test.png",
            "Picture books/Qiaohu1.HEIC",
            "Picture books/Qiaohu2.HEIC"
        ]
        
        for image_path in test_images:
            if os.path.exists(image_path):
                test_single_image(image_path)
                print("\n" + "=" * 60 + "\n")
            else:
                print(f"⚠️  图片不存在: {image_path}\n")

