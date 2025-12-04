# 导入发送网络请求的工具库
import requests

# 1. 这里填入你在 PushPlus 获取的 Token
# 务必保留引号，例如 my_token = 'a1b2c3d4...'
my_token = 'b4687307eeda489b8b7922dd66b661a5' 

# 2. 定义我们要发送的内容
url = 'http://www.pushplus.plus/send'
data = {
    "token": my_token,
    "title": "我的第一个监控程序",
    "content": "你好！如果你收到这条消息，说明你的代码已经成功跑通了！下一步就是监控币安价格了！",
    "template": "html"
}

# 3. 发送请求
print("正在尝试发送消息...")
response = requests.post(url, json=data)

# 4. 告诉我们结果
print("发送结果:", response.text)