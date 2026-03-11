"""
风险管理模块
"""
import math

class RiskManager:
    """风险管理器"""
    
    def __init__(self, max_position=0.1, max_loss=0.02, max_leverage=3):
        self.max_position = max_position  # 最大仓位 10%
        self.max_loss = max_loss          # 单次最大亏损 2%
        self.max_leverage = max_leverage  # 最大杠杆
        
    def calculate_position_size(self, balance, price, risk_percent=0.02):
        """计算仓位大小"""
        risk_amount = balance * risk_percent
        # 简化: 假设1%价格波动止损
        position = risk_amount / (price * 0.01)
        return min(position, balance * self.max_position / price)
    
    def check_risk(self, order_price, stop_loss, balance):
        """检查风险"""
        potential_loss = abs(order_price - stop_loss) * 1  # 简化
        loss_ratio = potential_loss / balance
        
        if loss_ratio > self.max_loss:
            return False, f"风险过高: {loss_ratio*100:.1f}%"
        return True, "风险可控"
    
    def calculate_leverage(self, balance, position_value):
        """计算杠杆"""
        if position_value == 0:
            return 1
        leverage = balance / position_value
        return min(leverage, self.max_leverage)
    
    def portfolio_risk(self, positions, total_value):
        """组合风险评估"""
        if total_value == 0:
            return 0
        
        # 简化: 假设等权重
        position_weights = [p['value'] / total_value for p in positions]
        
        # VaR 简化计算
        var_95 = total_value * 0.02 * sum(position_weights)
        
        return {
            'total_exposure': sum(p['value'] for p in positions),
            'var_95': var_95,
            'positions_count': len(positions),
            'diversification': 1 - max(position_weights) if position_weights else 0
        }

def main():
    rm = RiskManager()
    
    # 测试
    balance = 10000
    price = 50000
    size = rm.calculate_position_size(balance, price)
    print(f"建议仓位: {size:.4f} BTC")
    
    ok, msg = rm.check_risk(50000, 49000, balance)
    print(f"风险检查: {msg}")
    
    portfolio = [{'value': 5000}, {'value': 3000}]
    risk = rm.portfolio_risk(portfolio, 10000)
    print(f"组合风险: {risk}")

if __name__ == "__main__":
    main()
