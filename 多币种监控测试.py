import requests
import time
from datetime import datetime

# ================= 升级版配置区域 =================
# 1. 填入 Token
my_token = 'b4687307eeda489b8b7922dd66b661a5'

# 2. 监控名单 (想监控谁，就加在列表里，用英文逗号隔开)
target_coins = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'BNBUSDT']

# 3. 波动阈值 (5%)
# 【注意】正式使用设为 0.05。测试时可暂时设为 0.0001
threshold_percent = 0.01

# 4. 时间窗口 (秒) - 5分钟
window_seconds = 900 

# 5. [新增] 冷却时间 (秒) - 报警后多少秒内不再发通知？
# 这里设为 900秒 (15分钟)，防止刷屏
cooldown_seconds = 900
# ================================================

# --- 初始化“文件柜” ---
# 用来存放每个币的状态：基准价格、开始时间、上次报警时间
coin_states = {}

def get_price(symbol):
    """查询单个币种价格"""
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        res = requests.get(url, timeout=3) # 设置超时防止卡死
        return float(res.json()['price'])
    except:
        return None # 网络错误返回空

def send_alert(symbol, direction, price, change):
    """发送微信通知"""
    try:
        url = 'http://www.pushplus.plus/send'
        content = (
            f"<b>{symbol} 触发 {direction} 预警</b><br>"
            f"当前价格: ${price}<br>"
            f"波动幅度: {change*100:.2f}%<br>"
            f"触发时间: {datetime.now().strftime('%H:%M:%S')}"
        )
        data = {
            "token": my_token,
            "title": f"🚨 {symbol} 价格异动",
            "content": content,
            "template": "html"
        }
        requests.post(url, json=data)
        print(f"✅ [微信发送成功] {symbol}")
    except Exception as e:
        print(f"❌ 发送失败: {e}")

# --- 1. 程序启动，先给每个币录入初始信息 ---
print("🚀 系统启动，正在初始化所有币种基准价格...")
for symbol in target_coins:
    price = get_price(symbol)
    if price:
        coin_states[symbol] = {
            'base_price': price,
            'start_time': time.time(),
            'last_alert_time': 0  # 0 代表从来没报过警
        }
        print(f"   - {symbol} 初始录入: ${price}")
    else:
        print(f"   - {symbol} 获取失败，将在循环中重试")

print("-" * 30)
print(f"开始 7x24h 轮询监控，名单: {target_coins}")

# --- 2. 进入主循环 ---
while True:
    # 每一轮循环后休息 5 秒
    time.sleep(5)
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 新一轮巡检...")

    for symbol in target_coins:
        # 如果这个币之前初始化失败了，这里尝试补录
        if symbol not in coin_states:
            p = get_price(symbol)
            if p:
                coin_states[symbol] = {'base_price': p, 'start_time': time.time(), 'last_alert_time': 0}
            continue

        # 获取当前最新价格
        current_price = get_price(symbol)
        if current_price is None:
            continue # 网络不好，跳过这个币，看下一个

        # 取出“档案”里的旧数据
        state = coin_states[symbol]
        base_price = state['base_price']
        start_time = state['start_time']
        last_alert = state['last_alert_time']

        # 计算波动
        change = (current_price - base_price) / base_price
        
        # 打印简报 (只在控制台显示，不发微信)
        print(f"   {symbol}: {base_price} -> {current_price} | 浮动 {change*100:.3f}%")

        now = time.time()

        # --- 判断 A: 是否触发阈值？ ---
        if abs(change) > threshold_percent:
            # 检查是否还在“冷却期”
            if (now - last_alert) < cooldown_seconds:
                print(f"   🚫 {symbol} 波动达标，但处于冷却期 (还剩 {int(cooldown_seconds - (now-last_alert))}秒)，不发送。")
            else:
                # 真的报警！
                direction = "暴涨 📈" if change > 0 else "暴跌 📉"
                print(f"   !!! {symbol} 触发报警！发送微信...")
                send_alert(symbol, direction, current_price, change)
                
                # 更新档案：记录这次报警时间，并重置基准价格
                coin_states[symbol]['last_alert_time'] = now
                coin_states[symbol]['base_price'] = current_price
                coin_states[symbol]['start_time'] = now

        # --- 判断 B: 时间窗口是否过期 (5分钟) ---
        # 如果5分钟内无事发生，也要重置基准，跟上最新行情
        elif (now - start_time) > window_seconds:
            # print(f"   (窗口重置) {symbol} 5分钟已到，更新基准价")
            coin_states[symbol]['base_price'] = current_price
            coin_states[symbol]['start_time'] = now