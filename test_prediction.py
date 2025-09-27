#!/usr/bin/env python3
"""
测试天气预测功能
"""
import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from weather_tools import predict_weather_trend

def test_prediction():
    """测试天气预测功能"""
    print("Testing weather prediction functionality")
    print("=" * 50)

    # 测试超出预报范围的日期（10天后）
    target_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")

    print(f"\n1. 测试未来10天预测 (日期: {target_date})")
    print("-" * 40)

    result = predict_weather_trend.invoke({"city": "北京", "target_date": target_date})

    if "error" in result:
        print("Error:", result['error'])
    else:
        print(f"Success: Predicted weather for {result['city']} on {result['target_date']}")
        print(f"Days ahead: {result['days_ahead']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Data source: {result['data_source']}")
        print(f"Limitation: {result['limitation']}")

        prediction = result['prediction']
        print("\nPrediction details:")
        print(f"  Predicted temperature: {prediction.get('predicted_temperature', 'N/A')}°C")
        print(f"  Temperature trend: {prediction.get('temperature_trend', 'N/A')}")
        print(f"  Season: {prediction.get('season', 'N/A')}")
        print(f"  Typical weather: {prediction.get('typical_weather', 'N/A')}")
        print(f"  Recommendation: {prediction.get('recommendation', 'N/A')}")

    # 测试无效日期
    print("\n2. 测试无效日期")
    print("-" * 40)

    result = predict_weather_trend.invoke({"city": "北京", "target_date": "2024-01-01"})
    print("Response:", result)

    # 测试近期的预测（应该使用常规预报）
    target_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
    print(f"\n3. 测试未来3天预测")
    print("-" * 40)

    result = predict_weather_trend.invoke({"city": "上海", "target_date": target_date})

    if "error" in result:
        print("Error:", result['error'])
    else:
        print(f"Prediction for {result['city']} on {result['target_date']}")
        prediction = result['prediction']
        if prediction.get('predicted_temperature'):
            print(f"Temperature: {prediction['predicted_temperature']}°C")

if __name__ == "__main__":
    test_prediction()