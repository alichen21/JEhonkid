"""
测试文本处理性能
用于诊断文本处理慢的问题
"""

import os
import sys
import time
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from text_processor import TextProcessor
from picture_to_text import PictureToText

def test_text_processing_performance():
    """测试文本处理性能"""
    print("=" * 60)
    print("文本处理性能测试")
    print("=" * 60)
    
    # 初始化处理器
    try:
        text_processor = TextProcessor()
        print("✅ 文本处理器初始化成功\n")
    except Exception as e:
        print(f"❌ 文本处理器初始化失败: {e}")
        return
    
    # 测试用例1: 短文本
    print("-" * 60)
    print("测试用例 1: 短文本 (<100字符)")
    print("-" * 60)
    short_text = """4A 101-a
☆☆
でてきた
ものは?
げんき よく よみましょう。
なつにすなはまで
すいかわりを します。
しろい かもめが
とんで います。"""
    
    print(f"输入文本长度: {len(short_text)} 字符")
    print(f"输入文本:\n{short_text}\n")
    
    start_time = time.time()
    result = text_processor.process_ocr_text(short_text)
    total_time = time.time() - start_time
    
    if "error" in result:
        print(f"❌ 处理失败: {result['error']}")
    else:
        print(f"✅ 处理成功")
        if "_performance" in result:
            perf = result["_performance"]
            print(f"\n性能数据:")
            print(f"  - 总耗时: {perf['total_time']:.2f} 秒")
            print(f"  - API调用时间: {perf['api_time']:.2f} 秒")
            print(f"  - 解析时间: {perf['parse_time']:.2f} 秒")
            print(f"  - Prompt长度: {perf['prompt_length']} 字符")
            print(f"  - 响应长度: {perf['response_length']} 字符")
        print(f"\n处理结果:")
        print(f"  日语正文: {result.get('japanese_text', '')[:100]}...")
        print(f"  中文翻译: {result.get('chinese_translation', '')[:100]}...")
        print(f"  分段数量: {len(result.get('segments', []))}")
    
    print(f"\n总耗时: {total_time:.2f} 秒\n")
    
    # 测试用例2: 从实际图片OCR
    print("-" * 60)
    print("测试用例 2: 从实际图片OCR")
    print("-" * 60)
    
    test_image = "Picture books/Kumon test.png"
    if os.path.exists(test_image):
        try:
            ocr = PictureToText()
            print(f"📷 处理图片: {test_image}")
            
            ocr_start = time.time()
            ocr_result = ocr.extract_text(test_image)
            ocr_time = time.time() - ocr_start
            
            if "error" in ocr_result:
                print(f"❌ OCR失败: {ocr_result['error']}")
            else:
                print(f"✅ OCR成功，耗时: {ocr_time:.2f} 秒")
                full_text = ocr_result.get('full_text', '')
                print(f"OCR文本长度: {len(full_text)} 字符")
                print(f"OCR文本预览:\n{full_text[:200]}...\n")
                
                # 测试文本处理
                print("开始文本处理...")
                result = text_processor.process_ocr_text(full_text)
                
                if "error" in result:
                    print(f"❌ 文本处理失败: {result['error']}")
                else:
                    print(f"✅ 文本处理成功")
                    if "_performance" in result:
                        perf = result["_performance"]
                        print(f"\n性能数据:")
                        print(f"  - OCR耗时: {ocr_time:.2f} 秒")
                        print(f"  - 文本处理总耗时: {perf['total_time']:.2f} 秒")
                        print(f"  - API调用时间: {perf['api_time']:.2f} 秒 ({perf['api_time']/perf['total_time']*100:.1f}%)")
                        print(f"  - 解析时间: {perf['parse_time']:.2f} 秒 ({perf['parse_time']/perf['total_time']*100:.1f}%)")
                        print(f"  - Prompt长度: {perf['prompt_length']} 字符")
                        print(f"  - 响应长度: {perf['response_length']} 字符")
                        print(f"\n  ⚠️  如果API调用时间占比 >80%，说明API是瓶颈")
                        print(f"  ⚠️  如果API调用时间 >20秒，建议优化API或更换模型")
        except Exception as e:
            print(f"❌ 测试失败: {e}")
    else:
        print(f"⚠️  测试图片不存在: {test_image}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    print("\n💡 提示:")
    print("  - 如果API调用时间很长(>10秒)，说明LLM API是瓶颈")
    print("  - 如果Prompt长度很大(>2000字符)，考虑优化prompt或限制输入长度")
    print("  - 如果解析时间很长(>1秒)，检查解析逻辑")


if __name__ == "__main__":
    test_text_processing_performance()




