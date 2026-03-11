"""
量化交易Prompt模板
"""
from string import Template

SYSTEM_PROMPT = """你是一个专业的量化交易分析师，专注于加密货币市场。

你的职责:
1. 分析技术指标和市场趋势
2. 评估交易风险
3. 生成量化交易策略
4. 提供风险管理建议

分析时请考虑:
- RSI, MACD, Bollinger Bands等技术指标
- 市场情绪和新闻影响
- 资金流向
- 支撑位和阻力位

请用JSON格式返回分析结果。
"""

TRADING_ANALYSIS_PROMPT = Template("""请分析以下交易对: $symbol

当前价格数据:
- 价格: $price
- 24h涨跌: $change%
- 24h成交量: $volume

技术指标:
- RSI(14): $rsi
- MACD: $macd_signal
- Bollinger: $bb_position

市场情绪: $sentiment

请返回JSON格式:
{
  "signal": "buy|sell|hold",
  "confidence": 0.0-1.0,
  "entry_price": 价格,
  "stop_loss": 价格,
  "take_profit": [价格数组],
  "position_size": 0.0-1.0,
  "risk_level": "low|medium|high",
  "analysis": "简要分析"
}
""")

RISK_ASSESSMENT_PROMPT = Template("""请评估以下交易的风险:

交易方向: $direction
入场价格: $entry
止损价格: $stop_loss
止盈价格: $take_profit
仓位大小: $position_size%
账户余额: $balance

请返回JSON:
{
  "risk_score": 0-100,
  "risk_level": "low|medium|high",
  "max_loss_usd": 金额,
  "risk_reward_ratio": 倍数,
  "recommendation": "执行|修改|放弃"
}
""")

PORTFOLIO_OPTIMIZATION_PROMPT = Template("""请优化投资组合:

当前持仓:
$holdings

可用资金: $cash
风险偏好: $risk_tolerance

请返回最优配置:
{
  "allocations": [
    {"symbol": "BTC", "weight": 0.0-1.0, "reason": "..."}
  ],
  "expected_return": "年化百分比",
  "risk_score": 0-100,
  "rebalance_needed": true/false
}
""")

def format_trading_analysis(symbol, data):
    """格式化交易分析"""
    return TRADING_ANALYSIS_PROMPT.substitute(
        symbol=symbol,
        price=data.get('price', 'N/A'),
        change=data.get('change_24h', 0),
        volume=data.get('volume_24h', 0),
        rsi=data.get('rsi', 'N/A'),
        macd_signal=data.get('macd', 'N/A'),
        bb_position=data.get('bb_position', 'N/A'),
        sentiment=data.get('sentiment', 'neutral')
    )

def format_risk_assessment(trade_data):
    """格式化风险评估"""
    return RISK_ASSESSMENT_PROMPT.substitute(
        direction=trade_data.get('direction'),
        entry=trade_data.get('entry'),
        stop_loss=trade_data.get('stop_loss'),
        take_profit=trade_data.get('take_profit'),
        position_size=trade_data.get('position_size'),
        balance=trade_data.get('balance')
    )

def format_portfolio_optimization(holdings, cash, risk_tolerance='medium'):
    """格式化组合优化"""
    holdings_str = "\n".join([
        f"- {h['symbol']}: {h['amount']} @ ${h['price']}"
        for h in holdings
    ])
    
    return PORTFOLIO_OPTIMIZATION_PROMPT.substitute(
        holdings=holdings_str,
        cash=cash,
        risk_tolerance=risk_tolerance
    )
