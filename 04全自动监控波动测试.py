import requests
import time
from datetime import datetime

# ================= 用户配置区域 =================
# 1. 填入 Token
my_token = 'b4687307eeda489b8b7922dd66b661a5'

# 2. 监控币种
symbol = 'BTCUSDT'

# 3. 波动阈值 (0.05 代表 5%)
# 【测试建议】为了立刻看到效果，先设为 0.0001 (0.01%)，测完改回 0.05
threshold_percent = 0.02 

# 4. 时间窗口 (秒)
# 每过多久重置一次基准价格？5分钟 = 300秒
window_seconds = 300 
# ===========================================

def get_price():
    """获取当前价格的工具函数"""
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        res = requests.get(url, timeout=5)
        return float(res.json()['price'])
    except:
        return None # 如果网络出问题，返回空

def send_alert(content):
    """发微信的工具函数"""
    url = 'http://www.pushplus.plus/send'
    data = {
        "token": my_token,
        "title": f"🔥 {symbol} 价格异动！",
        "content": content,
        "template": "html"
    }
    requests.post(url, json=data)

# --- 主程序开始 ---
print(f"🚀 开始监控 {symbol}，每 5 秒检查一次...")
print(f"🎯 目标：5分钟内波动超过 {threshold_percent*100}%")

# 1. 设定初始基准
base_price = get_price()
start_time = time.time()
print(f"📍 初始基准价格: ${base_price}")

# 进入死循环，一直运行，直到你手动停止
while True:
    # 休息 5 秒，避免请求太频繁被封 IP
    time.sleep(5) 
    
    current_price = get_price()
    if current_price is None:
        print("网络抖动，跳过本次...")
        continue

    # 计算波动率：(当前 - 基准) / 基准
    change = (current_price - base_price) / base_price
    
    # 获取当前时间
    now_time = time.time()
    
    # 打印一条简短的日志，让你知道它在活着
    # {:.4f}% 表示保留4位小数
    print(f"当前: ${current_price} | 波动: {change*100:.4f}% | 耗时: {int(now_time - start_time)}秒")

    # --- 判断逻辑 A: 是否触发报警？ ---
    # abs(change) 取绝对值，不管涨跌，只要幅度够大就触发
    if abs(change) > threshold_percent:
        direction = "暴涨 📈" if change > 0 else "暴跌 📉"
        msg = (
            f"监控对象: {symbol}<br>"
            f"异动类型: {direction}<br>"
            f"基准价格: {base_price}<br>"
            f"当前价格: {current_price}<br>"
            f"波动幅度: {change*100:.2f}%<br>"
            f"触发时间: {datetime.now().strftime('%H:%M:%S')}"
        )
        print("!!! 触发报警，正在发送微信...")
        send_alert(msg)
        
        # 报警后，通常重置基准，防止一直重复报警
        base_price = current_price
        start_time = time.time()
        print("✅ 报警已发送，基准价格已重置，继续监控...")

    # --- 判断逻辑 B: 是否超时 5 分钟？ ---
    # 如果过了5分钟还没触发报警，也要重置基准，因为我们要监控的是“短时”波动
    elif (now_time - start_time) > window_seconds:
        print("⏱️ 5分钟时间窗口已到，重置基准价格...")
        base_price = current_price
        start_time = time.time()