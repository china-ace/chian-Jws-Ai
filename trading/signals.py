"""
信号分析模块
基于技术指标和AI分析
"""
import pandas as pd
import numpy as np

class SignalAnalyzer:
    """技术信号分析"""
    
    @staticmethod
    def sma(data, period=20):
        """简单移动平均"""
        return pd.Series(data).rolling(period).mean().values
    
    @staticmethod
    def ema(data, period=20):
        """指数移动平均"""
        return pd.Series(data).ewm(span=period).mean().values
    
    @staticmethod
    def rsi(data, period=14):
        """RSI相对强弱指数"""
        delta = pd.Series(data).diff()
        gain = (delta.where(delta > 0, 0)).rolling(period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    @staticmethod
    def macd(data, fast=12, slow=26, signal=9):
        """MACD指标"""
        ema_fast = pd.Series(data).ewm(span=fast).mean()
        ema_slow = pd.Series(data).ewm(span=slow).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal).mean()
        histogram = macd_line - signal_line
        return macd_line.values, signal_line.values, histogram.values
    
    @staticmethod
    def analyze_signals(closes):
        """综合分析信号"""
        signals = {}
        
        # RSI
        rsi = SignalAnalyzer.rsi(closes)
        signals['rsi'] = rsi[-1]
        
        # MACD
        macd, signal, hist = SignalAnalyzer.macd(closes)
        signals['macd'] = {'macd': macd[-1], 'signal': signal[-1], 'hist': hist[-1]}
        
        # 均线交叉
        sma_fast = SignalAnalyzer.sma(closes, 5)
        sma_slow = SignalAnalyzer.sma(closes, 20)
        signals['crossover'] = 'golden' if sma_fast[-1] > sma_slow[-1] else 'death'
        
        # 建议
        if rsi[-1] < 30:
            signals['advice'] = 'BUY - 超卖'
        elif rsi[-1] > 70:
            signals['advice'] = 'SELL - 超买'
        else:
            signals['advice'] = 'HOLD'
            
        return signals

def main():
    # 测试数据
    test_data = [100 + i + np.random.randn() for i in range(50)]
    signals = SignalAnalyzer.analyze_signals(test_data)
    print("=== 信号分析 ===")
    for k, v in signals.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
