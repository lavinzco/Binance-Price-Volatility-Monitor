# 📈 Binance Price Volatility Monitor (币安价格异动监控机器人)

这是一个基于 Python 开发的轻量级加密货币行情监控脚本。它能够通过币安 (Binance) 公共 API 实时监控指定代币的价格，当在设定时间窗口内（如 5 分钟）发生大幅波动（如 ±5%）时，通过微信及时发送报警通知。

## ✨ 主要功能

* **多币种监控**：支持同时监控多个交易对（如 BTC/USDT, ETH/USDT, SOL/USDT 等）。
* **智能波动算法**：基于滑动时间窗口（Rolling Window）计算价格变化率。
* **防骚扰机制**：内置冷却时间（Cooldown），避免在剧烈波动行情中通过微信连续刷屏。
* **微信推送**：集成 PushPlus 服务，报警消息直接推送到个人微信。
* **零成本部署**：无需 API Key（仅读取公共行情），无需付费软件，支持本地或云服务器运行。

## 🛠️ 技术栈

* **语言**：Python 3.x
* **数据源**：Binance Public API (REST)
* **通知服务**：PushPlus (推送加)
* **依赖库**：`requests`

## 🚀 快速开始

### 1. 环境准备
确保你的电脑或服务器已安装 Python 3。

安装必要的依赖库：
```bash
pip install requests
```

### 2. 获取通知 Token
本项目使用 PushPlus 进行微信推送：

访问 PushPlus 官网。

使用微信扫码登录。

在“发送消息” -> “一对一消息”中复制你的 Token。

### 3. 配置参数
打开 monitor.py 文件，修改顶部的配置区域：

Python

1. 填入你的 PushPlus Token
```
my_token = '这里粘贴你的Token'
```

2. 修改监控名单
```
target_coins = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'BNBUSDT']
```

3. 设置报警阈值 (例如 0.05 代表 5%)
```
threshold_percent = 0.05
```

4. 设置时间窗口 (秒)
```
window_seconds = 300 
```

5. 设置冷却时间 (秒)
```
cooldown_seconds = 900
```

### 4. 运行程序
在终端或命令行中运行：

```bash
python monitor.py
