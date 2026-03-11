#!/usr/bin/env python3
"""
市场扫描器
自动扫描多个交易所寻找交易机会
"""
import ccxt
import time

class MarketScanner:
    """市场扫描器"""
    
    def __init__(self):
        self.exchanges = {}
        
    def add_exchange(self, exchange_id):
        """添加交易所"""
        try:
            exchange_class = getattr(ccxt, exchange_id)
            exchange = exchange_class()
            self.exchanges[exchange_id] = exchange
            print(f"✅ 添加交易所: {exchange_id}")
        except Exception as e:
            print(f"❌ 添加失败 {exchange_id}: {e}")
    
    def scan_markets(self, symbols):
        """扫描市场"""
        results = []
        
        for exchange_id, exchange in self.exchanges.items():
            print(f"🔍 扫描 {exchange_id}...")
            
            try:
                for symbol in symbols:
                    try:
                        ticker = exchange.fetch_ticker(symbol)
                        
                        result = {
                            'exchange': exchange_id,
                            'symbol': symbol,
                            'price': ticker['last'],
                            'volume_24h': ticker['quoteVolume'],
                            'change_24h': ticker['percentage'],
                            'bid': ticker.get('bid', 0),
                            'ask': ticker.get('ask', 0),
                            'spread': ticker.get('ask', 0) - ticker.get('bid', 0)
                        }
                        
                        # 计算套利机会
                        if result['spread'] > 0:
                            result['spread_pct'] = result['spread'] / result['price'] * 100
                        
                        results.append(result)
                        
                    except Exception as e:
                        pass
                        
                time.sleep(0.5)  # 避免限流
                
            except Exception as e:
                print(f"❌ {exchange_id} 错误: {e}")
        
        return results
    
    def find_arbitrage(self, results):
        """寻找套利机会"""
        # 按symbol分组
        by_symbol = {}
        for r in results:
            s = r['symbol']
            if s not in by_symbol:
                by_symbol[s] = []
            by_symbol[s].append(r)
        
        opportunities = []
        
        for symbol, data in by_symbol.items():
            if len(data) < 2:
                continue
            
            # 找最低价和最高价
            prices = [(r['price'], r['exchange']) for r in data]
            min_price, min_ex = min(prices)
            max_price, max_ex = max(prices)
            
            spread = (max_price - min_price) / min_price * 100
            
            if spread > 0.5:  # 0.5%以上有机会
                opportunities.append({
                    'symbol': symbol,
                    'buy_exchange': min_ex,
                    'sell_exchange': max_ex,
                    'buy_price': min_price,
                    'sell_price': max_price,
                    'spread_pct': spread,
                    'potential_profit': spread - 0.2  # 减去手续费估计
                })
        
        return sorted(opportunities, key=lambda x: x['spread_pct'], reverse=True)
    
    def print_results(self, results, opportunities=None):
        """打印结果"""
        print("\n" + "="*70)
        print("📊 市场扫描结果")
        print("="*70)
        
        # 按涨幅排序
        sorted_results = sorted(results, key=lambda x: x.get('change_24h', 0), reverse=True)
        
        print("\n🔥 涨幅榜:")
        for r in sorted_results[:5]:
            change = r.get('change_24h', 0) or 0
            emoji = '🟢' if change >= 0 else '🔴'
            print(f"  {emoji} {r['exchange']:12} {r['symbol']:15} ${r['price']:,.2f} ({change:+.2f}%)")
        
        print("\n📈 跌幅榜:")
        for r in sorted_results[-5:]:
            change = r.get('change_24h', 0) or 0
            emoji = '🟢' if change >= 0 else '🔴'
            print(f"  {emoji} {r['exchange']:12} {r['symbol']:15} ${r['price']:,.2f} ({change:+.2f}%)")
        
        if opportunities:
            print("\n💰 套利机会:")
            for o in opportunities[:5]:
                print(f"  {o['symbol']}: {o['buy_exchange']}买 ${o['buy_price']:.2f} -> {o['sell_exchange']}卖 ${o['sell_price']:.2f}")
                print(f"    利润: {o['potential_profit']:.2f}%")

def main():
    scanner = MarketScanner()
    
    # 添加交易所
    scanner.add_exchange('binance')
    scanner.add_exchange('bybit')
    scanner.add_exchange('okx')
    
    # 扫描
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT', 'XRP/USDT']
    results = scanner.scan_markets(symbols)
    
    # 找套利
    opportunities = scanner.find_arbitrage(results)
    
    # 打印
    scanner.print_results(results, opportunities)

if __name__ == "__main__":
    main()
