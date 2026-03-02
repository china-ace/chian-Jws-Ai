#!/usr/bin/env python3
"""
收入报告系统 - 自动统计和报告收入情况
支持微信、支付宝、USDT 等多种收款方式
"""

import json
import datetime
from typing import Dict, List, Optional

class IncomeReporter:
    def __init__(self):
        self.payment_methods = {
            'wechat': '微信支付',
            'alipay': '支付宝', 
            'usdt_erc20': 'USDT (ERC20)',
            'usdt_trc20': 'USDT (TRC20)'
        }
        
        # 你的收款地址信息（从环境变量或配置文件读取）
        self.payment_addresses = {
            'usdt_erc20': '0x0c4828ad682a1e531ada65fed31abb0f52de4627',
            'usdt_trc20': 'TJyUtTpAtRWvNgjrGyEfrtjwmsKviD7ro4'
        }
        
        self.income_records = []
    
    def add_income_record(self, amount: float, currency: str, payment_method: str, 
                         service_type: str, timestamp: Optional[datetime.datetime] = None):
        """添加收入记录"""
        if timestamp is None:
            timestamp = datetime.datetime.now()
            
        record = {
            'amount': amount,
            'currency': currency,
            'payment_method': payment_method,
            'service_type': service_type,
            'timestamp': timestamp.isoformat(),
            'date': timestamp.strftime('%Y-%m-%d')
        }
        
        self.income_records.append(record)
        self.save_records()
        return record
    
    def get_daily_income(self, date: str = None) -> Dict[str, float]:
        """获取每日收入统计"""
        if date is None:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            
        daily_income = {}
        for record in self.income_records:
            if record['date'] == date:
                method = record['payment_method']
                if method not in daily_income:
                    daily_income[method] = 0
                daily_income[method] += record['amount']
                
        return daily_income
    
    def get_weekly_income(self) -> Dict[str, float]:
        """获取本周收入统计"""
        today = datetime.datetime.now()
        week_start = today - datetime.timedelta(days=today.weekday())
        week_start_str = week_start.strftime('%Y-%m-%d')
        
        weekly_income = {}
        for record in self.income_records:
            record_date = datetime.datetime.fromisoformat(record['timestamp']).date()
            if record_date >= week_start.date():
                method = record['payment_method']
                if method not in weekly_income:
                    weekly_income[method] = 0
                weekly_income[method] += record['amount']
                
        return weekly_income
    
    def generate_income_report(self, period: str = 'daily') -> str:
        """生成收入报告"""
        if period == 'daily':
            income_data = self.get_daily_income()
            report_title = f"今日收入报告 ({datetime.datetime.now().strftime('%Y-%m-%d')})"
        elif period == 'weekly':
            income_data = self.get_weekly_income()
            report_title = f"本周收入报告"
        else:
            income_data = self.get_daily_income()
            report_title = "收入报告"
            
        total_income = sum(income_data.values())
        
        report = f"{report_title}\n"
        report += "=" * len(report_title) + "\n\n"
        
        if income_data:
            for method, amount in income_data.items():
                method_name = self.payment_methods.get(method, method)
                report += f"{method_name}: ¥{amount:.2f}\n"
            report += f"\n总收入: ¥{total_income:.2f}\n"
        else:
            report += "暂无收入记录\n"
            
        return report
    
    def save_records(self):
        """保存收入记录到文件"""
        with open('income_records.json', 'w', encoding='utf-8') as f:
            json.dump(self.income_records, f, ensure_ascii=False, indent=2)
    
    def load_records(self):
        """从文件加载收入记录"""
        try:
            with open('income_records.json', 'r', encoding='utf-8') as f:
                self.income_records = json.load(f)
        except FileNotFoundError:
            self.income_records = []

# 使用示例
if __name__ == "__main__":
    reporter = IncomeReporter()
    
    # 添加测试记录
    reporter.add_income_record(50.0, 'CNY', 'wechat', '量化交易咨询')
    reporter.add_income_record(100.0, 'CNY', 'alipay', '自动化服务')
    reporter.add_income_record(20.0, 'USDT', 'usdt_trc20', 'AI咨询服务')
    
    # 生成报告
    print(reporter.generate_income_report('daily'))
    print("\n" + "="*50 + "\n")
    print(reporter.generate_income_report('weekly'))