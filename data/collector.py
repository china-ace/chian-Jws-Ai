"""
数据采集模块
"""
import requests
import pandas as pd
from datetime import datetime

class DataCollector:
    """数据采集器"""
    
    def __init__(self):
        self.cache = {}
        
    def fetch_crypto_prices(self, coins=['bitcoin', 'ethereum', 'solana']):
        """获取加密货币价格"""
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': ','.join(coins),
            'vs_currencies': 'usd',
            'include_24hr_change': 'true'
        }
        try:
            resp = requests.get(url, params=params, timeout=10)
            return resp.json()
        except Exception as e:
            print(f"获取价格失败: {e}")
            return {}
    
    def fetch_market_data(self, coin_id='bitcoin'):
        """获取市场数据"""
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        params = {
            'localization': 'false',
            'tickers': 'false',
            'community_data': 'false',
            'developer_data': 'false'
        }
        try:
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
            return {
                'name': data.get('name'),
                'symbol': data.get('symbol'),
                'price': data.get('market_data', {}).get('current_price', {}).get('usd'),
                'market_cap': data.get('market_data', {}).get('market_cap', {}).get('usd'),
                'volume': data.get('market_data', {}).get('total_volume', {}).get('usd'),
                'change_24h': data.get('market_data', {}).get('price_change_percentage_24h'),
            }
        except Exception as e:
            print(f"获取市场数据失败: {e}")
            return {}
    
    def fetch_news(self, query='crypto'):
        """获取新闻"""
        # 简化: 返回模拟数据
        return [
            {'title': 'BTC突破新高', 'source': 'CoinDesk'},
            {'title': 'ETH升级临近', 'source': 'Cointelegraph'},
        ]
    
    def to_dataframe(self, data):
        """转换为DataFrame"""
        return pd.DataFrame(data)
    
    def save_csv(self, data, filename):
        """保存为CSV"""
        df = self.to_dataframe(data)
        df.to_csv(filename, index=False)
        print(f"已保存: {filename}")

def main():
    collector = DataCollector()
    
    # 获取价格
    prices = collector.fetch_crypto_prices()
    print("=== 加密货币价格 ===")
    for coin, data in prices.items():
        print(f"{coin}: ${data['usd']:.2f} ({data.get('usd_24h_change', 0):.2f}%)")
    
    # 获取BTC详情
    btc = collector.fetch_market_data('bitcoin')
    print(f"\n=== Bitcoin ===")
    print(f"市值: ${btc.get('market_cap', 0):,.0f}")

if __name__ == "__main__":
    main()
