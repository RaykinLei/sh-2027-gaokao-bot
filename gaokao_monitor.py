# gaokao_monitor.py（仓库根目录）
import os
import requests
import json

# 从环境变量获取密钥（由YAML传递过来）
DOUBAO_API_KEY = os.getenv("DOUBAO_API_KEY")
DOUBAO_ENDPOINT_ID = os.getenv("DOUBAO_ENDPOINT_ID")
SENDKEY = os.getenv("SENDKEY")  # 新增：获取SendKey

# 调用豆包API查询高考信息（这部分不变）
def query_gaokao_info():
    url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    headers = {
        "Authorization": f"Bearer {DOUBAO_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": DOUBAO_ENDPOINT_ID,
        "messages": [{"role": "user", "content": "查询上海2027年高考最新官方政策、报名时间、考试科目，只返回关键信息"}],
        "temperature": 0.1
    }
    try:
        res = requests.post(url, headers=headers, json=data, timeout=10)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"查询失败：{str(e)}"

# 重点改这里：换成 SendKey（Server酱）推送
def push_sendkey(content):
    url = f"https://sctapi.ftqq.com/{SENDKEY}.send"  # SendKey接口地址
    data = {
        "title": "上海2027高考监控",  # 推送标题
        "desp": content  # 推送内容
    }
    requests.post(url, data=data, timeout=5)

# 主程序（调用SendKey推送）
if __name__ == "__main__":
    info = query_gaokao_info()
    print("高考信息：", info)
    push_sendkey(info)  # 改成调用SendKey推送
