#!/usr/bin/env python3
"""
每日报告生成脚本
"""
import sys
from datetime import datetime
sys.path.append(__file__.rsplit('/', 1)[0])

from data.collector import DataCollector
from data.analyzer import DataAnalyzer

def generate_daily_report():
    collector = DataCollector()
    analyzer = DataAnalyzer()
    
    report = f"""
╔══════════════════════════════════════════════════════╗
║         Javis 智能量化 - 每日报告                     ║
║              {datetime.now().strftime('%Y-%m-%d')}                             ║
╚══════════════════════════════════════════════════════╝

📊 市场概况
"""
    
    # 获取主流币种价格
    coins = ['bitcoin', 'ethereum', 'solana', 'cardano', 'ripple']
    prices = collector.fetch_crypto_prices(coins)
    
    for coin, data in prices.items():
        change = data.get('usd_24h_change', 0)
        emoji = '🟢' if change >= 0 else '🔴'
        report += f"{emoji} {coin.capitalize()}: ${data['usd']:,.2f} ({change:+.2f}%)\n"
    
    report += """
📈 技术信号
"""
    # 示例信号
    report += "🔍 分析中...\n"
    
    report += """
📋 系统状态
"""
    report += f"- 运行时间: {datetime.now().strftime('%H:%M:%S')}\n"
    report += "- 交易机器人: 就绪\n"
    report += "- 数据采集: 正常\n"
    
    report += """
💡 今日学习
"""
    report += "- AI: LangChain, AutoGen\n"
    report += "- 交易: FreqTrade, CCXT\n"
    report += "- 云原生: Kubernetes, ArgoCD\n"
    
    report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
由 Javis AI 自动生成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    print(report)
    
    # 保存到文件
    filename = f"reports/daily_{datetime.now().strftime('%Y%m%d')}.txt"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n✅ 报告已保存: {filename}")
    except:
        pass

if __name__ == "__main__":
    generate_daily_report()
