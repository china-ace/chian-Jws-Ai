"""
回测引擎
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class Backtester:
    """回测引擎"""
    
    def __init__(self, initial_balance=10000, fee=0.001):
        self.initial_balance = initial_balance
        self.fee = fee  # 交易手续费 0.1%
        self.trades = []
        self.balance = initial_balance
        self.position = 0  # 持仓数量
        self.position_price = 0  # 持仓价格
        
    def buy(self, price, amount, date):
        """买入"""
        cost = price * amount * (1 + self.fee)
        if cost > self.balance:
            # 全部买入
            amount = self.balance / (price * (1 + self.fee))
            cost = price * amount * (1 + self.fee)
        
        self.balance -= cost
        self.position += amount
        self.position_price = price
        
        self.trades.append({
            'date': date,
            'type': 'BUY',
            'price': price,
            'amount': amount,
            'value': cost
        })
        
    def sell(self, price, amount, date):
        """卖出"""
        if amount > self.position:
            amount = self.position
            
        value = price * amount * (1 - self.fee)
        self.balance += value
        self.position -= amount
        
        profit = (price - self.position_price) * amount - (price * amount * self.fee * 2)
        
        self.trades.append({
            'date': date,
            'type': 'SELL',
            'price': price,
            'amount': amount,
            'value': value,
            'profit': profit
        })
        
        if self.position == 0:
            self.position_price = 0
    
    def run(self, prices, signals):
        """运行回测
        
        prices: 价格列表 [price1, price2, ...]
        signals: 信号列表 ['buy', 'sell', 'hold']
        """
        for i in range(len(prices)):
            signal = signals[i] if i < len(signals) else 'hold'
            
            if signal == 'buy' and self.position == 0:
                # 用80%仓位买入
                amount = (self.balance * 0.8) / prices[i]
                self.buy(prices[i], amount, i)
                
            elif signal == 'sell' and self.position > 0:
                self.sell(prices[i], self.position, i)
        
        # 最终平仓
        if self.position > 0:
            self.sell(prices[-1], self.position, len(prices)-1)
    
    def get_results(self):
        """获取回测结果"""
        final_value = self.balance
        total_return = (final_value - self.initial_balance) / self.initial_balance * 100
        
        # 计算交易次数
        buy_count = sum(1 for t in self.trades if t['type'] == 'BUY')
        sell_count = sum(1 for t in self.trades if t['type'] == 'SELL')
        
        # 计算利润
        profits = [t['profit'] for t in self.trades if 'profit' in t]
        wins = sum(1 for p in profits if p > 0)
        losses = sum(1 for p in profits if p < 0)
        
        # 最大回撤
        balance_history = [self.initial_balance]
        for t in self.trades:
            if t['type'] == 'BUY':
                balance_history.append(balance_history[-1] - t['value'])
            else:
                balance_history.append(balance_history[-1] + t['value'])
        
        peak = max(balance_history)
        max_dd = min((b - peak) / peak for b in balance_history) * 100
        
        return {
            'initial_balance': self.initial_balance,
            'final_balance': final_value,
            'total_return': total_return,
            'total_trades': buy_count + sell_count,
            'win_rate': wins / (wins + losses) * 100 if (wins + losses) > 0 else 0,
            'max_drawdown': max_dd,
            'wins': wins,
            'losses': losses,
            'trades': self.trades
        }
    
    def print_results(self):
        """打印结果"""
        r = self.get_results()
        print("=" * 50)
        print("           回测结果")
        print("=" * 50)
        print(f"初始资金:   ${r['initial_balance']:,.2f}")
        print(f"最终资金:   ${r['final_balance']:,.2f}")
        print(f"总收益率:   {r['total_return']:.2f}%")
        print(f"交易次数:   {r['total_trades']}")
        print(f"胜率:       {r['win_rate']:.1f}%")
        print(f"最大回撤:   {r['max_drawdown']:.2f}%")
        print(f"盈利交易:   {r['wins']}")
        print(f"亏损交易:   {r['losses']}")
        print("=" * 50)

def simple_ma_strategy(prices, short_ma=5, long_ma=20):
    """简单均线策略"""
    signals = []
    for i in range(len(prices)):
        if i < long_ma:
            signals.append('hold')
        else:
            avg_short = np.mean(prices[i-short_ma:i])
            avg_long = np.mean(prices[i-long_ma:i])
            
            # 前一个状态
            prev_short = np.mean(prices[i-short_ma-1:i-1])
            prev_long = np.mean(prices[i-long_ma-1:i-1])
            
            # 金叉买入，死叉卖出
            if prev_short <= prev_long and avg_short > avg_long:
                signals.append('buy')
            elif prev_short >= prev_long and avg_short < avg_long:
                signals.append('sell')
            else:
                signals.append('hold')
    
    return signals

def main():
    # 模拟数据
    np.random.seed(42)
    prices = [100]
    for i in range(199):
        change = np.random.randn() * 2
        prices.append(prices[-1] * (1 + change/100))
    
    # 均线策略
    signals = simple_ma_strategy(prices)
    
    # 回测
    bt = Backtester(initial_balance=10000)
    bt.run(prices, signals)
    bt.print_results()

if __name__ == "__main__":
    main()
