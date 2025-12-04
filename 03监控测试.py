import requests

# ================= 配置区域 =================
# 1. 填入你的 Token
my_token = 'b4687307eeda489b8b7922dd66b661a5'

# 2. 设置你的“心理价位”
# 为了测试成功，我们故意设得很低（比如 10000），确保现在的价格能触发它！
target_threshold = 90000
# ===========================================

print("【第一步】正在查询 Binance 价格...")
url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
response = requests.get(url)
data = response.json()

# 注意：API 给我们的价格是 "字符串" (带引号的文本)，我们要把它变成 "数字" 才能比大小
current_price = float(data['price']) 

print(f"查询成功！当前 BTC 价格是: ${current_price}")

print("【第二步】正在进行逻辑判断...")
# 这里是核心逻辑：如果 当前价格 > 目标阈值
if current_price > target_threshold:
    print(f"!!! 触发报警：当前价格 {current_price} 高于设定值 {target_threshold}")
    print("【第三步】正在发送微信通知...")
    
    # 发送通知的代码
    notify_url = 'http://www.pushplus.plus/send'
    content = f"比特币价格为 {current_price} 了！已经超过了你设定的 {target_threshold} 美元！"
    notify_data = {
        "token": my_token,
        "title": "💰 价格突破报警",
        "content": content,
        "template": "html"
    }
    requests.post(notify_url, json=notify_data)
    print("✅ 通知已发送，请检查手机！")

else:
    # 如果价格没达到，程序就会走这条路
    print(f"😴 价格平静：当前 {current_price} 还没超过 {target_threshold}，无需打扰。")