"""
vLLM API代理
连接量化系统与大模型
"""
import requests
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

VLLM_URL = os.environ.get('VLLM_BASE_URL', 'http://localhost:8000')

@app.route('/v1/chat/completions', methods=['POST'])
def chat():
    """Chat接口"""
    data = request.json
    
    # 转换格式
    messages = data.get('messages', [])
    prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
    
    # 调用vLLM
    resp = requests.post(
        f"{VLLM_URL}/v1/completions",
        json={
            "prompt": prompt,
            "max_tokens": data.get('max_tokens', 500),
            "temperature": data.get('temperature', 0.7)
        }
    )
    
    return jsonify(resp.json())

@app.route('/v1/completions', methods=['POST'])
def complete():
    """Completion接口"""
    data = request.json
    
    resp = requests.post(
        f"{VLLM_URL}/v1/completions",
        json=data
    )
    
    return jsonify(resp.json())

@app.route('/models', methods=['GET'])
def models():
    """列出可用模型"""
    resp = requests.get(f"{VLLM_URL}/v1/models")
    return jsonify(resp.json())

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "vllm": VLLM_URL})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
