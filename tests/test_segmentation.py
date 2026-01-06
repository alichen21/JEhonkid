#!/usr/bin/env python3
"""
测试分段朗读功能
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from text_processor import TextProcessor

def test_segmentation():
    """测试文本分段功能"""
    print("=" * 60)
    print("测试文本分段功能")
    print("=" * 60)
    
    processor = TextProcessor()
    
    # 测试自动分段功能
    test_text = "なつにすなはまですいかわりをします。しろいかもめがとんでいます。あおいそらがとてもきれいです。"
    
    print(f"\n测试文本: {test_text}\n")
    
    # 测试自动分段
    segments = processor._auto_segment(test_text, sentences_per_segment=2)
    
    print(f"分段结果（每段2句）:")
    for i, segment in enumerate(segments, 1):
        print(f"  段落 {i}: {segment}")
    
    print(f"\n总共 {len(segments)} 个段落")
    
    # 测试不同句子数
    print("\n" + "-" * 60)
    print("测试不同句子数设置:")
    for sentences in [1, 2, 3]:
        segments = processor._auto_segment(test_text, sentences_per_segment=sentences)
        print(f"\n每段 {sentences} 句:")
        for i, segment in enumerate(segments, 1):
            print(f"  段落 {i}: {segment}")

def test_instruction_detection():
    """测试指导语识别"""
    print("\n" + "=" * 60)
    print("测试指导语识别")
    print("=" * 60)
    
    # 模拟LLM返回的格式
    mock_response = """指导语：
でてきたものは？げんきよく読みましょう。

正文：
なつにすなはまですいかわりをします。しろいかもめがとんでいます。

分段：
なつにすなはまですいかわりをします。
しろいかもめがとんでいます。

中文翻译：
夏天去沙滩做打西瓜游戏。白色的海鸥在飞翔。"""
    
    processor = TextProcessor()
    result = processor._parse_response(mock_response)
    
    print("\n解析结果:")
    print(f"指导语: {result['instruction']}")
    print(f"正文: {result['main_text']}")
    print(f"分段数: {len(result['segments'])}")
    for i, segment in enumerate(result['segments'], 1):
        print(f"  段落 {i}: {segment}")
    print(f"中文翻译: {result['chinese_translation']}")

if __name__ == "__main__":
    try:
        test_segmentation()
        test_instruction_detection()
        print("\n" + "=" * 60)
        print("✅ 测试完成！")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

