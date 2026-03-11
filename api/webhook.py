#!/usr/bin/env python3
"""
TradingView Webhook 处理器
接收TradingView警报并执行交易
"""
from flask import Flask, request, jsonify
import sys
import hmac
import hashlib
sys.path.append(__file__.rsplit('/', 1)[0])

from trading.bot import TradingBot
from trading.sentiment import SentimentAnalyzer

app = Flask(__name__)

# 配置
SECRET_KEY = "your-webhook-secret"  # TradingView Webhook URL中的密钥
bot = TradingBot()

def verify_signature(data, signature):
    """验证签名"""
    if not SECRET_KEY:
        return True
    expected = hmac.new(
        SECRET_KEY.encode(),
        data.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected)

@app.route('/webhook', methods=['POST'])
def webhook():
    """处理TradingView webhook"""
    try:
        # 获取数据
        data = request.get_data(as_text=True)
        signature = request.headers.get('X-Webhook-Signature', '')
        
        # 验证签名
        if not verify_signature(data, signature):
            return jsonify({'error': 'Invalid signature'}), 401
        
        # 解析JSON
        alert = request.json
        
        print(f"📨 收到TradingView警报: {alert}")
        
        # 提取信号
        action = alert.get('action', '').lower()
        symbol = alert.get('symbol', 'BTC/USDT')
        price = alert.get('price')
        
        # 执行交易
        if action == 'buy':
            amount = alert.get('amount', 0.001)
            if price:
                result = bot.buy(symbol, amount, price)
            else:
                result = bot.buy(symbol, amount)
            return jsonify({'status': 'success', 'action': 'buy', 'result': result})
            
        elif action == 'sell':
            # 卖出全部
            balance = bot.get_balance()
            amount = balance['total'].get('BTC', 0)
            if amount > 0:
                result = bot.sell(symbol, amount, price)
                return jsonify({'status': 'success', 'action': 'sell', 'result': result})
            return jsonify({'status': 'skipped', 'reason': 'no position'})
        
        else:
            return jsonify({'status': 'unknown action', 'action': action})
    
    except Exception as e:
        print(f"❌ Webhook错误: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({'status': 'ok'})

def main():
    print("🚀 TradingView Webhook服务启动")
    print("📝 在TradingView设置Webhook URL为:")
    print("   https://your-domain.com/webhook")
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    main()
