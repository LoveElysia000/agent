#!/usr/bin/env python3
"""
天气预报Agent测试脚本
"""
import os
from dotenv import load_dotenv
from weather_tools import WeatherTools
from model_config import get_qwen_model

# 加载环境变量
load_dotenv()

def test_weather_tools():
    """测试天气工具"""
    print("🧪 测试天气工具...")
    
    weather_tools = WeatherTools()
    
    # 测试当前天气
    print("\n1. 测试当前天气查询:")
    result = weather_tools.get_current_weather("Beijing")
    print(f"结果: {result}")
    
    # 测试天气预报
    print("\n2. 测试天气预报查询:")
    result = weather_tools.get_weather_forecast("Shanghai")
    print(f"结果: {result}")

def test_model_config():
    """测试模型配置"""
    print("\n🧪 测试模型配置...")
    
    try:
        model = get_qwen_model()
        print(f"✅ 模型配置成功: {model}")
    except Exception as e:
        print(f"❌ 模型配置失败: {e}")

if __name__ == "__main__":
    print("=== 天气预报Agent测试 ===")
    
    # 检查API密钥
    if not os.getenv("OPENWEATHERMAP_API_KEY"):
        print("⚠️  请先在.env文件中配置OpenWeatherMap API密钥")
    else:
        test_weather_tools()
    
    if not os.getenv("QWEN_API_KEY"):
        print("⚠️  请先在.env文件中配置Qwen API密钥")
    else:
        test_model_config()
    
    print("\n✅ 测试完成")