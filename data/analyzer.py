"""
数据分析模块
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class DataAnalyzer:
    """数据分析器"""
    
    def __init__(self):
        self.history = []
        
    def add_data(self, data):
        """添加数据"""
        self.history.append({
            'timestamp': datetime.now(),
            'data': data
        })
        
    def calculate_returns(self, prices):
        """计算收益率"""
        return pd.Series(prices).pct_change().values
    
    def sharpe_ratio(self, returns, risk_free_rate=0.02):
        """夏普比率"""
        excess_returns = returns - risk_free_rate / 252
        if excess_returns.std() == 0:
            return 0
        return np.sqrt(252) * excess_returns.mean() / excess_returns.std()
    
    def max_drawdown(self, prices):
        """最大回撤"""
        peak = prices.cummax()
        drawdown = (prices - peak) / peak
        return drawdown.min()
    
    def volatility(self, returns):
        """波动率"""
        return returns.std() * np.sqrt(252)
    
    def analyze_portfolio(self, holdings, prices):
        """组合分析"""
        total_value = sum(h['amount'] * prices.get(h['symbol'], 0) for h in holdings)
        
        returns = []
        for h in holdings:
            if h['symbol'] in prices:
                ret = self.calculate_returns([h.get('cost', 100), prices[h['symbol']]])
                returns.extend(ret[1:])
        
        if returns:
            returns = np.array(returns)
            analysis = {
                'total_value': total_value,
                'sharpe': self.sharpe_ratio(returns),
                'volatility': self.volatility(returns),
                'returns_mean': returns.mean() * 252,
            }
        else:
            analysis = {'total_value': total_value}
            
        return analysis
    
    def generate_report(self, holdings):
        """生成分析报告"""
        report = f"""
=== 投资组合分析报告 ===
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

持仓情况:
"""
        total = 0
        for h in holdings:
            value = h.get('amount', 0) * h.get('price', 0)
            total += value
            report += f"- {h.get('symbol')}: {h.get('amount')} @ ${h.get('price'):.2f} = ${value:.2f}\n"
        
        report += f"\n总价值: ${total:.2f}\n"
        
        return report

def main():
    analyzer = DataAnalyzer()
    
    # 测试
    holdings = [
        {'symbol': 'BTC', 'amount': 0.1, 'price': 50000, 'cost': 45000},
        {'symbol': 'ETH', 'amount': 1.0, 'price': 3000, 'cost': 2800},
    ]
    
    prices = {'BTC': 50000, 'ETH': 3000}
    analysis = analyzer.analyze_portfolio(holdings, prices)
    
    print("=== 组合分析 ===")
    for k, v in analysis.items():
        print(f"{k}: {v}")
    
    print(analyzer.generate_report(holdings))

if __name__ == "__main__":
    main()
