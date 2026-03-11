"""
情绪分析模块
基于新闻和社交媒体分析市场情绪
"""
import requests
import re
from collections import Counter

class SentimentAnalyzer:
    """市场情绪分析"""
    
    def __init__(self):
        self.keywords = {
            'bullish': ['buy', 'bull', 'moon', 'pump', 'gain', 'rise', 'up', 'positive', 'growth', 'breakout'],
            'bearish': ['sell', 'bear', 'dump', 'crash', 'down', 'drop', 'negative', 'loss', 'reject'],
            'neutral': ['hold', 'wait', 'watch', 'range', 'consolidate']
        }
    
    def analyze_text(self, text):
        """分析文本情绪"""
        text = text.lower()
        words = re.findall(r'\w+', text)
        
        scores = {'bullish': 0, 'bearish': 0, 'neutral': 0}
        
        for word in words:
            for sentiment, keywords in self.keywords.items():
                if word in keywords:
                    scores[sentiment] += 1
        
        total = sum(scores.values())
        if total == 0:
            return {'sentiment': 'neutral', 'scores': scores, 'confidence': 0}
        
        # 计算情绪
        bull_score = scores['bullish'] / total
        bear_score = scores['bearish'] / total
        
        if bull_score > bear_score + 0.2:
            sentiment = 'bullish'
        elif bear_score > bull_score + 0.2:
            sentiment = 'bearish'
        else:
            sentiment = 'neutral'
        
        return {
            'sentiment': sentiment,
            'scores': scores,
            'confidence': max(bull_score, bear_score),
            'bullish_pct': bull_score * 100,
            'bearish_pct': bear_score * 100
        }
    
    def analyze_news(self, news_list):
        """分析新闻列表"""
        results = []
        for news in news_list:
            title = news.get('title', '')
            result = self.analyze_text(title)
            result['title'] = title
            results.append(result)
        
        # 汇总
        sentiments = [r['sentiment'] for r in results]
        counter = Counter(sentiments)
        
        return {
            'total': len(results),
            'summary': dict(counter),
            'overall': counter.most_common(1)[0][0] if counter else 'neutral',
            'details': results
        }
    
    def get_trading_signal(self, sentiment_analysis):
        """生成交易信号"""
        s = sentiment_analysis['overall']
        confidence = sentiment_analysis.get('confidence', 0)
        
        if s == 'bullish' and confidence > 0.6:
            return 'STRONG_BUY'
        elif s == 'bullish':
            return 'BUY'
        elif s == 'bearish' and confidence > 0.6:
            return 'STRONG_SELL'
        elif s == 'bearish':
            return 'SELL'
        else:
            return 'HOLD'

def main():
    analyzer = SentimentAnalyzer()
    
    # 测试
    news = [
        {'title': 'Bitcoin breaks $100k resistance - bullish momentum'},
        {'title': 'Whales accumulating BTC at current levels'},
        {'title': 'Market shows signs of consolidation'},
        {'title': 'Regulatory concerns could impact prices'},
    ]
    
    result = analyzer.analyze_news(news)
    print("=== 情绪分析 ===")
    print(f"总体: {result['overall']}")
    print(f"详情: {result['summary']}")
    print(f"信号: {analyzer.get_trading_signal(result)}")

if __name__ == "__main__":
    main()
