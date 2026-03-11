# 🤖 Javis 智能量化交易系统

> 由 AI 助手 Javis 自动维护

## 📦 项目结构

```
.
├── README.md                    # 本文件
├── trading/                     # 交易策略
│   ├── bot.py                   # 交易机器人
│   ├── signals.py                # 信号分析
│   └── risk_manager.py          # 风险管理
├── data/                        # 数据处理
│   ├── collector.py              # 数据采集
│   └── analyzer.py              # 数据分析
├── api/                         # API接口
│   └── server.py                # FastAPI服务
├── scripts/                     # 脚本
│   ├── daily_report.py           # 日报生成
│   └── backup.py                # 自动备份
└── config/                      # 配置
    └── settings.py               # 设置
```

## 🚀 功能特性

### 🤖 智能交易
- 多交易所支持 (CCXT)
- 情绪分析 (LangChain)
- 自动止损/止盈

### 📊 数据分析
- 实时行情监控
- 技术指标计算
- 异常检测告警

### 🔄 自动化
- 定时交易执行
- 收益报告生成
- 异常告警通知

## 🛠️ 技术栈

| 技术 | 用途 |
|------|------|
| Python | 主语言 |
| CCXT | 交易所API |
| LangChain | AI分析 |
| FastAPI | Web服务 |
| Pandas | 数据处理 |

## 📈 近期更新

- 2026-03-11: 系统初始化，由Javis AI创建

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 许可证

MIT License
