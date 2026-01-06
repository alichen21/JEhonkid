"""
文本转语音模块 - 使用 Google Cloud Text-to-Speech API
将日语文本转换为音频，适合儿童绘本朗读
支持 API Key 方式（REST API）
"""

import os
import json
import base64
from typing import Optional, Dict
from dotenv import load_dotenv
import requests

# 加载环境变量
load_dotenv()

class TextToSpeech:
    """文本转语音类，使用Google Cloud Text-to-Speech API (REST API + API Key)"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化文本转语音客户端
        
        Args:
            api_key: Google Cloud API Key，如果不提供则从环境变量读取
        """
        self.api_key = api_key or os.getenv('GOOGLE_CLOUD_API_KEY')
        if not self.api_key:
            raise ValueError("Google Cloud API Key未设置，请检查.env文件")
        
        # Google Cloud Text-to-Speech API REST端点
        self.api_url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={self.api_key}"
    
    def synthesize_japanese(
        self, 
        text: str, 
        voice_name: str = "ja-JP-Neural2-B",
        speaking_rate: float = 0.75,
        output_format: str = "mp3",
        model: Optional[str] = None
    ) -> Dict:
        """
        将日语文本转换为音频
        
        Args:
            text: 要转换的日语文本
            voice_name: 语音名称，默认为 ja-JP-Neural2-B（女声）
            speaking_rate: 语速，0.25-4.0，默认0.75（适合儿童）
            output_format: 输出格式，'mp3' 或 'wav'，默认 'mp3'
            model: 模型类型，如 'chirp-3-hd' 用于 Chirp 3 HD 模型，None 使用默认模型
        
        Returns:
            包含音频数据和元信息的字典:
            - audio_content: 音频二进制数据（base64解码后）
            - audio_format: 音频格式
            - voice_name: 使用的语音名称
            - model: 使用的模型类型
            - error: 错误信息（如果有）
        """
        if not text or not text.strip():
            return {
                "audio_content": None,
                "error": "输入文本为空"
            }
        
        # 设置音频编码格式（REST API 格式）
        audio_encoding_map = {
            "mp3": "MP3",
            "wav": "LINEAR16",
            "ogg": "OGG_OPUS"
        }
        
        if output_format.lower() not in audio_encoding_map:
            output_format = "mp3"
        
        audio_encoding = audio_encoding_map[output_format.lower()]
        
        # 构建请求体
        request_body = {
            "input": {
                "text": text
            },
            "voice": {
                "languageCode": "ja-JP",
                "name": voice_name
            },
            "audioConfig": {
                "audioEncoding": audio_encoding,
                "speakingRate": speaking_rate,
                "pitch": 2.0,  # 稍微提高音调，更适合儿童
                "volumeGainDb": 1.0  # 稍微增加音量
            }
        }
        
        # 如果指定了模型（如 Chirp 3 HD），添加到 audioConfig
        if model:
            request_body["audioConfig"]["model"] = model
        
        # 发送请求
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(self.api_url, json=request_body, headers=headers, timeout=30)
            
            # 如果状态码不是 200，尝试解析错误响应
            if response.status_code != 200:
                try:
                    error_data = response.json()
                    error_message = error_data.get('error', {}).get('message', f'HTTP {response.status_code}')
                    error_details = error_data.get('error', {}).get('details', [])
                    return {
                        "audio_content": None,
                        "error": f"TTS API错误 ({response.status_code}): {error_message}",
                        "error_details": str(error_details) if error_details else None,
                        "request_body": request_body  # 用于调试
                    }
                except:
                    return {
                        "audio_content": None,
                        "error": f"TTS API请求失败: HTTP {response.status_code} - {response.text[:200]}",
                        "request_body": request_body  # 用于调试
                    }
            
            result = response.json()
            
            # 检查是否有错误
            if 'error' in result:
                return {
                    "audio_content": None,
                    "error": result['error'].get('message', '未知错误')
                }
            
            # 解码 base64 音频数据
            audio_content_base64 = result.get('audioContent', '')
            if not audio_content_base64:
                return {
                    "audio_content": None,
                    "error": "API返回中没有音频数据"
                }
            
            # 解码 base64 字符串为二进制数据
            audio_content = base64.b64decode(audio_content_base64)
            
            return {
                "audio_content": audio_content,
                "audio_format": output_format.lower(),
                "voice_name": voice_name,
                "speaking_rate": speaking_rate,
                "model": model or "default"
            }
        
        except requests.exceptions.RequestException as e:
            return {
                "audio_content": None,
                "error": f"TTS API请求失败: {str(e)}"
            }
        except Exception as e:
            return {
                "audio_content": None,
                "error": f"TTS API调用失败: {str(e)}"
            }
    
    def save_audio(self, audio_content: bytes, output_path: str) -> bool:
        """
        保存音频内容到文件
        
        Args:
            audio_content: 音频二进制数据
            output_path: 输出文件路径
        
        Returns:
            是否保存成功
        """
        try:
            with open(output_path, 'wb') as out:
                out.write(audio_content)
            return True
        except Exception as e:
            print(f"保存音频文件失败: {str(e)}")
            return False


def main():
    """测试函数"""
    try:
        tts = TextToSpeech()
        
        # 测试文本
        test_text = "こんにちは。これはテストです。"
        
        print("=" * 60)
        print("测试日语文本转语音功能")
        print("=" * 60)
        print(f"\n输入文本: {test_text}\n")
        
        result = tts.synthesize_japanese(
            text=test_text,
            voice_name="ja-JP-Neural2-B",
            speaking_rate=0.75
        )
        
        if "error" in result:
            print(f"❌ 错误: {result['error']}")
        else:
            print("✅ 转换成功！")
            print(f"语音: {result['voice_name']}")
            print(f"语速: {result['speaking_rate']}")
            print(f"格式: {result['audio_format']}")
            print(f"音频大小: {len(result['audio_content'])} 字节")
            
            # 保存测试音频
            output_file = "test_audio.mp3"
            if tts.save_audio(result['audio_content'], output_file):
                print(f"\n✅ 音频已保存到: {output_file}")
    
    except Exception as e:
        print(f"❌ 初始化失败: {str(e)}")
        print("\n提示：")
        print("1. 确保已设置 GOOGLE_CLOUD_API_KEY 环境变量")
        print("2. 或在 .env 文件中设置 GOOGLE_CLOUD_API_KEY")
        print("3. 确保已启用 Cloud Text-to-Speech API")


if __name__ == "__main__":
    main()

