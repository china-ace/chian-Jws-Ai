#!/usr/bin/env python3
"""
价格告警系统
监控价格并发送告警
"""
import requests
import time
from datetime import datetime

class PriceAlert:
    """价格告警"""
    
    def __init__(self):
        self.alerts = []
        self.last_notify = {}
        
    def add_alert(self, symbol, price, condition='above', callback=None):
        """添加告警
        
        symbol: BTC/USDT
        price: 目标价格
        condition: 'above' or 'below'
        callback: 触发回调函数
        """
        alert = {
            'symbol': symbol,
            'target': price,
            'condition': condition,
            'callback': callback,
            'created_at': datetime.now().isoformat()
        }
        self.alerts.append(alert)
        print(f"✅ 添加告警: {symbol} {condition} ${price}")
        
    def check(self, prices):
        """检查告警"""
        triggered = []
        
        for alert in self.alerts:
            symbol = alert['symbol']
            target = alert['target']
            condition = alert['condition']
            
            current = prices.get(symbol)
            if not current:
                continue
            
            # 检查是否触发
            if condition == 'above' and current > target:
                triggered.append(alert)
                self._notify(alert, current)
                
            elif condition == 'below' and current < target:
                triggered.append(alert)
                self._notify(alert, current)
        
        return triggered
    
    def _notify(self, alert, current):
        """发送通知"""
        # 避免重复通知 (5分钟内)
        key = f"{alert['symbol']}_{alert['condition']}_{alert['target']}"
        now = time.time()
        
        if key in self.last_notify:
            if now - self.last_notify[key] < 300:
                return  # 5分钟内不重复
        
        self.last_notify[key] = now
        
        print("\n" + "="*50)
        print(f"🔔 价格告警!")
        print(f"品种: {alert['symbol']}")
        print(f"条件: {alert['condition']} ${alert['target']}")
        print(f"当前: ${current}")
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50)
        
        # 执行回调
        if alert['callback']:
            try:
                alert['callback'](alert, current)
            except Exception as e:
                print(f"回调错误: {e}")
        
        # 可以添加: 邮件/Telegram/短信通知
    
    def remove_alert(self, symbol, condition, target):
        """删除告警"""
        self.alerts = [
            a for a in self.alerts 
            if not (a['symbol'] == symbol and 
                   a['condition'] == condition and 
                   a['target'] == target)
        ]
        print(f"🗑️ 删除告警: {symbol}")

def get_prices(symbols):
    """获取价格 (简化版)"""
    # 实际应该用API获取
    import random
    prices = {}
    for s in symbols:
        base = {'BTC/USDT': 50000, 'ETH/USDT': 3000, 'SOL/USDT': 100}
        prices[s] = base.get(s, 1000) * (1 + random.uniform(-0.02, 0.02))
    return prices

def main():
    alert = PriceAlert()
    
    # 添加告警
    alert.add_alert('BTC/USDT', 52000, 'above')
    alert.add_alert('BTC/USDT', 48000, 'below')
    alert.add_alert('ETH/USDT', 3200, 'above')
    
    # 模拟监控
    symbols = ['BTC/USDT', 'ETH/USDT']
    
    print("🔍 启动价格监控...")
    
    for i in range(5):
        prices = get_prices(symbols)
        print(f"\n轮询 {i+1}: {prices}")
        
        triggered = alert.check(prices)
        
        time.sleep(2)
    
    print("\n监控结束")

if __name__ == "__main__":
    main()
