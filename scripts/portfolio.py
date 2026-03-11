"""
投资组合追踪器
"""
import json
from datetime import datetime
from pathlib import Path

class Portfolio:
    """投资组合管理器"""
    
    def __init__(self, file_path='portfolio.json'):
        self.file_path = file_path
        self.data = self.load()
        
    def load(self):
        """加载数据"""
        if Path(self.file_path).exists():
            with open(self.file_path, 'r') as f:
                return json.load(f)
        return {'holdings': [], 'history': []}
    
    def save(self):
        """保存数据"""
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add_holding(self, symbol, amount, price, note=''):
        """添加持仓"""
        holding = {
            'symbol': symbol,
            'amount': amount,
            'avg_price': price,
            'note': note,
            'added_at': datetime.now().isoformat()
        }
        self.data['holdings'].append(holding)
        self.save()
        
    def update_price(self, symbol, price):
        """更新价格"""
        for h in self.data['holdings']:
            if h['symbol'] == symbol:
                h['current_price'] = price
                h['updated_at'] = datetime.now().isoformat()
        self.save()
    
    def get_value(self):
        """计算总价值"""
        total = 0
        for h in self.data['holdings']:
            current = h.get('current_price', h['avg_price'])
            value = h['amount'] * current
            total += value
        return total
    
    def get_pnl(self):
        """计算盈亏"""
        results = []
        for h in self.data['holdings']:
            current = h.get('current_price', h['avg_price'])
            cost = h['amount'] * h['avg_price']
            value = h['amount'] * current
            pnl = value - cost
            pnl_pct = (pnl / cost * 100) if cost > 0 else 0
            
            results.append({
                'symbol': h['symbol'],
                'amount': h['amount'],
                'avg_price': h['avg_price'],
                'current_price': current,
                'value': value,
                'pnl': pnl,
                'pnl_pct': pnl_pct
            })
        return results
    
    def print_portfolio(self):
        """打印组合"""
        print("\n" + "="*60)
        print("📊 投资组合")
        print("="*60)
        
        if not self.data['holdings']:
            print("暂无持仓")
            return
        
        total_value = 0
        total_cost = 0
        
        for h in self.get_pnl():
            emoji = '🟢' if h['pnl'] >= 0 else '🔴'
            print(f"\n{h['symbol']}")
            print(f"  数量: {h['amount']:.6f}")
            print(f"  平均价: ${h['avg_price']:.2f}")
            print(f"  当前价: ${h['current_price']:.2f}")
            print(f"  价值: ${h['value']:.2f}")
            print(f"  盈亏: {emoji} ${h['pnl']:.2f} ({h['pnl_pct']:+.2f}%)")
            
            total_value += h['value']
            total_cost += h['amount'] * h['avg_price']
        
        total_pnl = total_value - total_cost
        total_pnl_pct = (total_pnl / total_cost * 100) if total_cost > 0 else 0
        emoji = '🟢' if total_pnl >= 0 else '🔴'
        
        print("\n" + "-"*60)
        print(f"💰 总价值: ${total_value:,.2f}")
        print(f"💵 总成本: ${total_cost:,.2f}")
        print(f"📈 总盈亏: {emoji} ${total_pnl:,.2f} ({total_pnl_pct:+.2f}%)")
        print("="*60)

def main():
    import sys
    sys.path.append('.')
    
    p = Portfolio()
    
    # 添加测试持仓
    if not p.data['holdings']:
        p.add_holding('BTC', 0.1, 45000, '测试')
        p.add_holding('ETH', 1.0, 2800, '测试')
    
    # 更新价格
    p.update_price('BTC', 50000)
    p.update_price('ETH', 3000)
    
    # 显示
    p.print_portfolio()

if __name__ == "__main__":
    main()
