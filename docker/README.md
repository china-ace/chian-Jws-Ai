# Docker 部署

## 快速启动

```bash
# 构建
cd docker
docker-compose build

# 运行
docker-compose up -d

# 查看日志
docker-compose logs -f
```

## 服务

- trading-bot: 交易机器人 (端口 8000)
- webhook: TradingView Webhook (端口 5000)

## 数据卷

- `/app/data` - 数据文件
- `/app/reports` - 报告文件
