import requests
import json

# FastAPI 默认运行地址
BASE_URL = "http://127.0.0.1:8000"


def test_generate_name():
    print ("--- 正在测试: AI 命名生成接口 ---")
    url = f"{BASE_URL}/name"

    # 根据你的 NameIn 模型构建请求体
    payload = {
        "category": "婴儿",  # 起名类型
        "vision": "大气、博学",  # 核心愿景
        "surname": "张",  # 姓氏
        "gender": "男",  # 性别
        "length": "两字",  # 字数限制
        "other": "要尽量大气一点",  # 其他要求
        "exclude": []  # 排除的名字
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        # 发送 POST 请求
        response = requests.post (url, json=payload, headers=headers)

        print (f"状态码: {response.status_code}")
        if response.status_code == 200:
            print ("生成结果:")
            print (json.dumps (response.json (), indent=4, ensure_ascii=False))
        else:
            print (f"请求失败，错误信息: {response.text}")

    except Exception as e:
        print (f"发送请求时出现异常: {e}")
    print ("\n")


if __name__ == "__main__":
    # 执行测试前请确保 main.py 已启动
    test_generate_name ()