#!/usr/bin/env python3
"""
自动交易机器人
定时执行交易策略
"""
import sys
import time
import schedule
from datetime import datetime
sys.path.append(__file__.rsplit('/', 1)[0])

from trading.bot import TradingBot
from trading.signals import SignalAnalyzer
from trading.sentiment import SentimentAnalyzer
from trading.risk_manager import RiskManager
from data.collector import DataCollector

class AutoTrader:
    """自动交易机器人"""
    
    def __init__(self, symbol='BTC/USDT', dry_run=True):
        self.symbol = symbol
        self.dry_run = dry_run  # 模拟模式，不真实交易
        self.bot = TradingBot()
        self.analyzer = SignalAnalyzer()
        self.sentiment = SentimentAnalyzer()
        self.risk = RiskManager()
        self.collector = DataCollector()
        
    def get_market_data(self):
        """获取市场数据"""
        # 获取K线
        ohlcv = self.bot.get_ohlcv(self.symbol, limit=100)
        closes = [c[4] for c in ohlcv]
        
        # 技术信号
        signals = self.analyzer.analyze_signals(closes)
        
        # 新闻情绪 (模拟)
        news = [
            {'title': 'Market analysis: BTC showing bullish signs'},
            {'title': 'Institutional investors increasing positions'},
        ]
        sentiment = self.sentiment.analyze_news(news)
        
        return {
            'price': closes[-1],
            'signals': signals,
            'sentiment': sentiment
        }
    
    def make_decision(self, market_data):
        """决策"""
        signals = market_data['signals']
        sentiment = market_data['sentiment']
        
        # 综合判断
        score = 0
        
        # RSI信号
        if signals.get('rsi', 50) < 30:
            score += 1
        elif signals.get('rsi', 50) > 70:
            score -= 1
        
        # MACD信号
        macd = signals.get('macd', {})
        if macd.get('hist', 0) > 0:
            score += 1
        else:
            score -= 1
        
        # 情绪
        if sentiment.get('overall') == 'bullish':
            score += 1
        elif sentiment.get('overall') == 'bearish':
            score -= 1
        
        # 决定
        if score >= 2:
            return 'buy'
        elif score <= -2:
            return 'sell'
        return 'hold'
    
    def execute(self):
        """执行交易"""
        print(f"\n{'='*50}")
        print(f"🤖 自动交易 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}")
        
        try:
            # 获取数据
            data = self.get_market_data()
            
            print(f"📊 当前价格: ${data['price']:.2f}")
            print(f"📈 信号: {data['signals'].get('advice', 'N/A')}")
            print(f"💭 情绪: {data['sentiment'].get('overall', 'N/A')}")
            
            # 决策
            decision = self.make_decision(data)
            print(f"🎯 决策: {decision.upper()}")
            
            if decision == 'hold':
                print("⏸️  无交易执行")
                return
            
            if self.dry_run:
                print(f"🔒 模拟模式: 不会真实{decision}")
                return
            
            # 执行交易
            balance = self.bot.get_balance()
            usdt = balance['total'].get('USDT', 0)
            
            if decision == 'buy' and usdt > 10:
                amount = usdt * 0.95 / data['price']
                self.bot.buy(self.symbol, amount)
                print(f"✅ 买入 {amount:.6f} {self.symbol}")
                
            elif decision == 'sell':
                btc = balance['total'].get('BTC', 0)
                if btc > 0.0001:
                    self.bot.sell(self.symbol, btc)
                    print(f"✅ 卖出 {btc:.6f} {self.symbol}")
            
        except Exception as e:
            print(f"❌ 错误: {e}")
    
    def run(self):
        """运行定时任务"""
        print("🚀 自动交易机器人启动")
        
        # 立即执行一次
        self.execute()
        
        # 设置定时任务
        schedule.every().hour.do(self.execute)
        # 或者 每天8点
        # schedule.every().day.at("08:00").do(self.execute)
        
        while True:
            schedule.run_pending()
            time.sleep(60)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--live', action='store_true', help='真实交易模式')
    args = parser.parse_args()
    
    trader = AutoTrader(dry_run=not args.live)
    trader.run()

if __name__ == "__main__":
    main()
