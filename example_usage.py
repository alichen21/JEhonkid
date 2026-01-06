"""
示例：如何使用 .env 文件中的 API 密钥

注意：确保已安装 python-dotenv
    pip install python-dotenv
"""

import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 获取 API 密钥
google_cloud_api_key = os.getenv('GOOGLE_CLOUD_API_KEY')
super_mind_api_key = os.getenv('SUPER_MIND_API_KEY')

# 验证密钥是否已加载
if google_cloud_api_key:
    print("✓ Google Cloud API Key 已加载")
    # 在实际使用中，不要打印完整的密钥
    print(f"  密钥前缀: {google_cloud_api_key[:10]}...")
else:
    print("✗ Google Cloud API Key 未找到")

if super_mind_api_key:
    print("✓ Super Mind API Key 已加载")
    print(f"  密钥前缀: {super_mind_api_key[:10]}...")
else:
    print("✗ Super Mind API Key 未找到")

# 使用示例（不要在实际代码中打印完整密钥）
# 在你的代码中使用这些变量，例如：
# 
# import requests
# 
# # 使用 Google Cloud API
# response = requests.get(
#     'https://some-api.google.com/endpoint',
#     params={'key': google_cloud_api_key}
# )
# 
# # 使用 Super Mind API
# headers = {
#     'Authorization': f'Bearer {super_mind_api_key}'
# }
# response = requests.get(
#     'https://space.ai-builders.com/api/endpoint',
#     headers=headers
# )

