import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def get_qwen_model():
    """配置并返回Qwen3-Max模型"""
    api_key = os.getenv("QWEN_API_KEY")
    base_url = os.getenv("QWEN_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    
    model = ChatOpenAI(
        model="qwen-turbo",  # Qwen3-Max对应的模型名称
        api_key=api_key,
        base_url=base_url,
        temperature=0.1,
        max_tokens=2000
    )
    
    return model

def get_model_config():
    """返回模型配置信息"""
    return {
        "model_name": "qwen-turbo",
        "model_type": "chat",
        "provider": "Alibaba Cloud DashScope"
    }