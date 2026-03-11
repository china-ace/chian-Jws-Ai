"""
配置文件
"""

# 交易配置
TRADING_CONFIG = {
    'default_exchange': 'binance',
    'default_symbol': 'BTC/USDT',
    'default_timeframe': '1h',
    
    # 风险管理
    'max_position_pct': 0.1,      # 最大仓位10%
    'max_loss_pct': 0.02,         # 最大亏损2%
    'stop_loss_pct': 0.01,        # 止损1%
    'take_profit_pct': 0.03,     # 止盈3%
}

# API配置
API_CONFIG = {
    'host': '0.0.0.0',
    'port': 8000,
    'debug': False,
}

# 数据源
DATA_CONFIG = {
    'price_api': 'coingecko',
    'news_api': 'cryptopanic',
    'cache_ttl': 300,  # 5分钟
}

# 交易所API (需要手动配置)
EXCHANGE_KEYS = {
    'binance': {
        'apiKey': 'YOUR_API_KEY',
        'secret': 'YOUR_SECRET',
    },
    'bybit': {
        'apiKey': 'YOUR_API_KEY',
        'secret': 'YOUR_SECRET',
    }
}

# 通知配置
NOTIFY_CONFIG = {
    'enabled': False,
    'email': 'your@email.com',
    'telegram_bot_token': '',
    'telegram_chat_id': '',
}
