"""测试智谱大模型补全实例"""
import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量（从项目根目录）
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

# 初始化客户端
client = OpenAI(
    base_url=os.getenv("ZHIPU_BASE_URL"),
    api_key=os.getenv("ZHIPU_API_KEY")
)

# 测试补全
response = client.chat.completions.create(
    model="glm-4-flash",
    messages=[
        {"role": "user", "content": "你好，请用一句话介绍自己"}
    ]
)

print(response.choices[0].message.content)
