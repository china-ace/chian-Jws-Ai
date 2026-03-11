"""
智能交易机器人
基于CCXT多交易所支持
"""
import ccxt
import time
from datetime import datetime

class TradingBot:
    def __init__(self, exchange_id='binance', api_key=None, secret=None):
        self.exchange = getattr(ccxt, exchange_id)({
            'apiKey': api_key,
            'secret': secret,
            'enableRateLimit': True,
        })
        
    def get_balance(self):
        """获取账户余额"""
        return self.exchange.fetch_balance()
    
    def get_price(self, symbol='BTC/USDT'):
        """获取价格"""
        return self.exchange.fetch_ticker(symbol)
    
    def buy(self, symbol, amount, price=None):
        """买入"""
        if price:
            return self.exchange.create_order(symbol, 'limit', 'buy', amount, price)
        return self.exchange.create_market_buy_order(symbol, amount)
    
    def sell(self, symbol, amount, price=None):
        """卖出"""
        if price:
            return self.exchange.create_order(symbol, 'limit', 'sell', amount, price)
        return self.exchange.create_market_sell_order(symbol, amount)
    
    def get_ohlcv(self, symbol, timeframe='1h', limit=100):
        """获取K线数据"""
        return self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    
    def print_balance(self):
        """打印余额"""
        balance = self.get_balance()
        print(f"=== {self.exchange.id} 账户余额 ===")
        for currency, amount in balance['total'].items():
            if amount > 0:
                print(f"{currency}: {amount}")

def main():
    # 示例: 只读模式
    bot = TradingBot('binance')
    bot.print_balance()
    
    # 获取BTC价格
    btc = bot.get_price('BTC/USDT')
    print(f"\nBTC/USDT: ${btc['last']:.2f}")

if __name__ == "__main__":
    main()
