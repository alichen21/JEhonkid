"""
快速测试 FastAPI 后端是否正常运行
"""

import requests
import sys

FASTAPI_BASE_URL = "http://127.0.0.1:8000"

def test_root():
    """测试根路径"""
    print("测试根路径...")
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/")
        if response.status_code == 200:
            print("✅ 根路径正常")
            print(f"   响应: {response.json()}")
            return True
        else:
            print(f"❌ 根路径返回错误状态码: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到 FastAPI 后端")
        print("   请确保 FastAPI 服务正在运行: python app_fastapi.py")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False

def test_api_docs():
    """测试 API 文档"""
    print("\n测试 API 文档...")
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ API 文档可访问")
            print(f"   地址: {FASTAPI_BASE_URL}/docs")
            return True
        else:
            print(f"❌ API 文档返回错误状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("FastAPI 后端测试")
    print("=" * 60)
    
    success = True
    
    # 测试根路径
    if not test_root():
        success = False
    
    # 测试 API 文档
    if not test_api_docs():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("✅ 所有测试通过！FastAPI 后端运行正常")
    else:
        print("❌ 部分测试失败，请检查 FastAPI 后端服务")
        sys.exit(1)
    print("=" * 60)

if __name__ == "__main__":
    main()

