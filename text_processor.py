"""
文本处理模块 - 使用LLM清理和翻译OCR结果
"""

import os
import json
from typing import Dict, Optional
from dotenv import load_dotenv
import requests

# 加载环境变量
load_dotenv()

class TextProcessor:
    """文本处理器，使用space.ai-builders.com的LLM API"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "grok-4-fast"):
        """
        初始化文本处理器
        
        Args:
            api_key: Super Mind API Key，如果不提供则从环境变量读取
            model: 使用的LLM模型，默认为grok-4-fast
        """
        self.api_key = api_key or os.getenv('SUPER_MIND_API_KEY')
        if not self.api_key:
            raise ValueError("Super Mind API Key未设置，请检查.env文件")
        
        self.model = model
        self.base_url = "https://space.ai-builders.com/backend/v1"
        self.api_url = f"{self.base_url}/chat/completions"
    
    def process_ocr_text(self, raw_text: str) -> Dict[str, str]:
        """
        处理OCR识别的原始文本
        
        Args:
            raw_text: OCR识别的原始文本
            
        Returns:
            包含处理后的日语正文和中文翻译的字典，以及指导语和分段信息
        """
        if not raw_text or not raw_text.strip():
            return {
                "japanese_text": "",
                "chinese_translation": "",
                "instruction": "",
                "main_text": "",
                "segments": [],
                "error": "输入文本为空"
            }
        
        # 构建prompt
        prompt = f"""你是一个日语绘本专家。以下是从图片中 OCR 提取的碎片内容：{raw_text}

请执行：

1. 去噪：删除页码、教材级别（如 4A）、水印等无关信息。
2. 去重：删除重复的注音假名。
3. 合并：将断行合并为自然的句子。
4. 识别指导语：识别出指导语（如"でてきたものは？げんきよく読みましょう。"这类教学指导），如果没有指导语则留空。
5. 识别正文：识别出实际的故事内容。
6. 分段：将正文按语义分成合适的段落，每段2-3句，适合单独朗读。

请严格按照以下格式输出（不要添加任何其他说明）：

指导语：
[指导语内容，如果没有则留空]

正文：
[处理后的日语正文]

分段：
[段落1]
[段落2]
[段落3]
...

中文翻译：
[对应的中文翻译]"""
        
        # 构建请求
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,  # 降低温度以获得更稳定的输出
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            # 提取回复内容
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                
                # 解析输出
                parsed_result = self._parse_response(content)
                
                return {
                    "japanese_text": parsed_result.get("japanese_text", ""),
                    "chinese_translation": parsed_result.get("chinese_translation", ""),
                    "instruction": parsed_result.get("instruction", ""),
                    "main_text": parsed_result.get("main_text", ""),
                    "segments": parsed_result.get("segments", []),
                    "raw_response": content
                }
            else:
                return {
                    "japanese_text": "",
                    "chinese_translation": "",
                    "instruction": "",
                    "main_text": "",
                    "segments": [],
                    "error": "API返回格式异常"
                }
        
        except requests.exceptions.RequestException as e:
            return {
                "japanese_text": "",
                "chinese_translation": "",
                "instruction": "",
                "main_text": "",
                "segments": [],
                "error": f"API请求失败: {str(e)}"
            }
        except Exception as e:
            return {
                "japanese_text": "",
                "chinese_translation": "",
                "instruction": "",
                "main_text": "",
                "segments": [],
                "error": f"处理失败: {str(e)}"
            }
    
    def _parse_response(self, content: str) -> Dict:
        """
        解析LLM返回的内容，提取指导语、正文、分段和中文翻译
        
        Args:
            content: LLM返回的原始内容
            
        Returns:
            包含instruction, main_text, segments, japanese_text, chinese_translation的字典
        """
        instruction = ""
        main_text = ""
        segments = []
        japanese_text = ""
        chinese_translation = ""
        
        # 尝试按格式解析
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            # 识别各个部分
            if '指导语' in line:
                current_section = 'instruction'
                if '：' in line or ':' in line:
                    sep = '：' if '：' in line else ':'
                    instruction = line.split(sep, 1)[1].strip()
                continue
            
            if '正文' in line and '分段' not in line:
                current_section = 'main_text'
                if '：' in line or ':' in line:
                    sep = '：' if '：' in line else ':'
                    main_text = line.split(sep, 1)[1].strip()
                continue
            
            if '分段' in line:
                current_section = 'segments'
                continue
            
            if '日语正文' in line or '日语：' in line or '日语文本' in line:
                current_section = 'japanese'
                if '：' in line or ':' in line:
                    sep = '：' if '：' in line else ':'
                    japanese_text = line.split(sep, 1)[1].strip()
                continue
            
            if '中文翻译' in line or '中文：' in line or '中文文本' in line:
                current_section = 'chinese'
                if '：' in line or ':' in line:
                    sep = '：' if '：' in line else ':'
                    chinese_translation = line.split(sep, 1)[1].strip()
                continue
            
            # 根据当前部分添加内容
            if current_section == 'instruction' and line:
                if instruction:
                    instruction += ' ' + line
                else:
                    instruction = line
            
            elif current_section == 'main_text' and line:
                if main_text:
                    main_text += '\n' + line
                else:
                    main_text = line
            
            elif current_section == 'segments' and line:
                # 分段内容，每行一个段落
                if line and not line.startswith('[') and not line.endswith(']'):
                    segments.append(line)
            
            elif current_section == 'japanese' and line:
                if japanese_text:
                    japanese_text += '\n' + line
                else:
                    japanese_text = line
            
            elif current_section == 'chinese' and line:
                if chinese_translation:
                    chinese_translation += '\n' + line
                else:
                    chinese_translation = line
        
        # 如果没有分段，尝试从正文自动分段
        if main_text and not segments:
            segments = self._auto_segment(main_text)
        
        # 如果没有找到正文，使用japanese_text作为正文
        if not main_text and japanese_text:
            main_text = japanese_text
            if not segments:
                segments = self._auto_segment(main_text)
        
        # 如果没有找到格式化的输出，尝试其他方法
        if not main_text and not japanese_text and not chinese_translation:
            # 尝试按段落分割
            paragraphs = content.split('\n\n')
            if len(paragraphs) >= 2:
                main_text = paragraphs[0].strip()
                japanese_text = main_text
                chinese_translation = paragraphs[1].strip()
                segments = self._auto_segment(main_text)
            else:
                # 如果都失败了，返回原始内容作为日语文本
                main_text = content.strip()
                japanese_text = main_text
                segments = self._auto_segment(main_text)
        
        return {
            "instruction": instruction.strip(),
            "main_text": main_text.strip(),
            "segments": [s.strip() for s in segments if s.strip()],
            "japanese_text": japanese_text.strip() if japanese_text else main_text.strip(),
            "chinese_translation": chinese_translation.strip()
        }
    
    def _auto_segment(self, text: str, sentences_per_segment: int = 2) -> list:
        """
        自动将文本分段，默认每段2-3句
        
        Args:
            text: 要分段的文本
            sentences_per_segment: 每段的句子数，默认2句
            
        Returns:
            分段后的列表
        """
        if not text:
            return []
        
        # 按句号、问号、感叹号分割句子
        import re
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


def main():
    """测试函数"""
    processor = TextProcessor()
    
    # 测试文本
    test_text = """4A 101-a
☆☆
でてきた
ものは?
げんき よく よみましょう。
なつにすなはまで
すいかわりを します。
しろい かもめが
とんで います。"""
    
    print("=" * 60)
    print("测试文本处理功能")
    print("=" * 60)
    print(f"\n原始文本:\n{test_text}\n")
    
    result = processor.process_ocr_text(test_text)
    
    if "error" in result:
        print(f"❌ 错误: {result['error']}")
    else:
        print("✅ 处理成功！\n")
        print(f"日语正文:\n{result['japanese_text']}\n")
        print(f"中文翻译:\n{result['chinese_translation']}\n")


if __name__ == "__main__":
    main()

