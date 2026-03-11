"""
FastAPI Web服务
"""
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import sys
sys.path.append(__file__.rsplit('/', 1)[0])

from trading.bot import TradingBot
from trading.signals import SignalAnalyzer
from data.collector import DataCollector
from data.analyzer import DataAnalyzer

app = FastAPI(title="Javis Trading API")

# 初始化
bot = TradingBot()
collector = DataCollector()
analyzer = DataAnalyzer()

class TradeRequest(BaseModel):
    symbol: str
    side: str  # buy/sell
    amount: float
    price: Optional[float] = None

@app.get("/")
def root():
    return {"message": "Javis Trading API", "version": "1.0"}

@app.get("/price/{symbol}")
def get_price(symbol: str):
    """获取价格"""
    data = collector.fetch_crypto_prices([symbol.lower()])
    return data

@app.get("/market/{coin_id}")
def get_market(coin_id: str):
    """获取市场数据"""
    return collector.fetch_market_data(coin_id)

@app.post("/trade")
def trade(req: TradeRequest):
    """交易"""
    try:
        if req.side == 'buy':
            result = bot.buy(req.symbol, req.amount, req.price)
        else:
            result = bot.sell(req.symbol, req.amount, req.price)
        return {"status": "success", "order": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/signals/{symbol}")
def get_signals(symbol: str):
    """获取信号分析"""
    try:
        ohlcv = bot.get_ohlcv(symbol, limit=100)
        closes = [c[4] for c in ohlcv]
        signals = SignalAnalyzer.analyze_signals(closes)
        return signals
    except Exception as e:
        return {"error": str(e)}

@app.get("/balance")
def get_balance():
    """获取余额"""
    try:
        return bot.get_balance()
    except:
        return {"error": "需要API密钥"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
