# vLLM 本地大模型部署指南

## 前置要求

- GPU: NVIDIA GPU (至少16GB显存)
- CUDA: 12.1+
- Docker: 24.0+

## 快速启动

### 1. 单独启动vLLM

```bash
# 使用Docker
docker run --gpus all -v ./models:/models \
  -p 8000:8000 \
  vllm/vllm:latest \
  --model meta-llama/Llama-2-7b-chat-hf \
  --tensor-parallel-size 1
```

### 2. 使用Docker Compose

```bash
cd docker
docker-compose -f docker-compose.vllm.yml up -d
```

## 支持的模型

| 模型 | 显存需求 | 推荐用途 |
|-----|---------|---------|
| Llama-2-7b | 16GB | 通用分析 |
| Llama-2-13b | 24GB | 复杂策略 |
| CodeLlama-7b | 16 |
| Mistral-7b | 16GB | 快速GB | 代码生成推理 |

## API使用

```python
import requests

# Chat接口
response = requests.post("http://localhost:8080/v1/chat/completions", {
    "messages": [
        {"role": "user", "content": "分析BTC现在适合买入吗?"}
    ]
})
print(response.json())

# 模型列表
response = requests.get("http://localhost:8080/models")
print(response.json())
```

## 量化分析示例

```python
from llm.quant_llm import QuantLLM

llm = QuantLLM("meta-llama/Llama-2-7b-chat-hf")
llm.load()

# 分析市场
result = llm.analyze_market("BTC: $50,000, RSI: 65, MACD: 金叉")
print(result)

# 生成策略
strategy = llm.generate_strategy(
    signals={"rsi": 45, "macd": "bullish"},
    sentiment="fearful"
)
print(strategy)
```

## 性能优化

- 使用 `tensor-parallel-size` 跨多GPU
- 调整 `gpu-memory-utilization` 避免OOM
- 使用 `max-model-len` 限制上下文长度

## 常见问题

Q: 显存不够?
A: 使用量化模型 (Q4_K_M, Q8_0)

Q: 推理慢?
A: 启用TensorRT-LLM加速

Q: 如何更新模型?
A: 重新pull镜像或指定新模型
