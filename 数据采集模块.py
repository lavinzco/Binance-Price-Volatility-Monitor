import requests # 导入网络请求工具

# 1. 设置币安的“价格查询地址”
# symbol=BTCUSDT 表示我们要查比特币兑泰达币的价格
# 如果你想查以太坊，改成 ETHUSDT 即可
target_url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

print("正在向币安询问价格...")

# 2. 发送请求 (就像在浏览器按回车)
response = requests.get(target_url)

# 3. 解析结果 (把原本的一长串数据变成能看懂的字典)
data = response.json()

# 4. 打印出来看看
print("查询成功！")
print("交易对:", data['symbol'])
print("当前价格:", data['price'])