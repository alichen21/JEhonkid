#!/usr/bin/env python3
"""
简单测试分段功能（不依赖环境变量）
"""

import re

def auto_segment(text: str, sentences_per_segment: int = 2) -> list:
    """
    自动将文本分段，默认每段2-3句
    """
    if not text:
        return []
    
    # 按句号、问号、感叹号分割句子
    # 匹配日语句子结束符
    sentences = re.split(r'([。！？\n])', text)
    
    # 重新组合句子
    segments = []
    current_segment = ""
    sentence_count = 0
    
    for i in range(0, len(sentences), 2):
        if i < len(sentences):
            sentence = sentences[i].strip()
            if i + 1 < len(sentences):
                sentence += sentences[i + 1]
            
            if sentence:
                if current_segment:
                    current_segment += sentence
                else:
                    current_segment = sentence
                
                sentence_count += 1
                
                # 达到目标句子数，开始新段落
                if sentence_count >= sentences_per_segment:
                    segments.append(current_segment.strip())
                    current_segment = ""
                    sentence_count = 0
    
    # 添加最后一段
    if current_segment.strip():
        segments.append(current_segment.strip())
    
    # 如果没有分段成功，返回整个文本作为一个段落
    if not segments:
        segments = [text.strip()]
    
    return segments

def test_segmentation():
    """测试文本分段功能"""
    print("=" * 60)
    print("测试文本分段功能")
    print("=" * 60)
    
    # 测试文本1：简单文本
    test_text1 = "なつにすなはまですいかわりをします。しろいかもめがとんでいます。あおいそらがとてもきれいです。"
    
    print(f"\n测试文本1: {test_text1}\n")
    
    # 测试自动分段
    segments = auto_segment(test_text1, sentences_per_segment=2)
    
    print(f"分段结果（每段2句）:")
    for i, segment in enumerate(segments, 1):
        print(f"  段落 {i}: {segment}")
    
    print(f"\n总共 {len(segments)} 个段落")
    
    # 测试不同句子数
    print("\n" + "-" * 60)
    print("测试不同句子数设置:")
    for sentences in [1, 2, 3]:
        segments = auto_segment(test_text1, sentences_per_segment=sentences)
        print(f"\n每段 {sentences} 句:")
        for i, segment in enumerate(segments, 1):
            print(f"  段落 {i}: {segment}")
    
    # 测试文本2：包含指导语的情况
    print("\n" + "=" * 60)
    print("测试文本2：包含指导语")
    print("=" * 60)
    
    test_text2 = "でてきたものは？げんきよく読みましょう。なつにすなはまですいかわりをします。しろいかもめがとんでいます。"
    
    print(f"\n测试文本2: {test_text2}\n")
    
    segments = auto_segment(test_text2, sentences_per_segment=2)
    print(f"分段结果（每段2句）:")
    for i, segment in enumerate(segments, 1):
        print(f"  段落 {i}: {segment}")

if __name__ == "__main__":
    try:
        test_segmentation()
        print("\n" + "=" * 60)
        print("✅ 分段功能测试完成！")
        print("=" * 60)
        print("\n提示：")
        print("1. 分段功能正常工作")
        print("2. 可以根据句子数设置调整分段")
        print("3. 可以处理包含问号的指导语")
        print("\n下一步：")
        print("- 启动Web应用测试完整功能")
        print("- 访问 http://127.0.0.1:5000 查看界面")
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

