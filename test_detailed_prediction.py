#!/usr/bin/env python3
"""
测试详细的天气预测功能
"""
import sys
import os
from dotenv import load_dotenv

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from weather_tools import predict_weather_trend

def test_detailed_prediction():
    """测试详细的天气预测功能"""
    print("Testing Detailed Weather Prediction")
    print("=" * 50)

    # 测试预测功能
    result = predict_weather_trend.invoke({"city": "北京", "target_date": "2025-10-10"})

    if "error" in result:
        print(f"Error: {result['error']}")
        return

    print(f"City: {result['city']}")
    print(f"Target Date: {result['target_date']}")
    print(f"Days Ahead: {result['days_ahead']}")
    print(f"Confidence: {result['confidence']}")
    print()

    prediction = result['prediction']
    print("Prediction Details:")
    print(f"Temperature: {prediction['predicted_temperature']}C")
    print(f"Humidity: {prediction['predicted_humidity']}%")
    print(f"Wind Speed: {prediction['predicted_wind_speed']}m/s")
    print(f"Weather Description: {prediction['predicted_weather_description']}")
    print(f"Temperature Trend: {prediction['temperature_trend']}")
    print(f"Season: {prediction['season']}")
    print(f"Typical Weather: {prediction['typical_weather']}")
    print(f"Recommendation: {prediction['recommendation']}")
    print()

    print("Weather Probabilities:")
    for prob in prediction['weather_probabilities']:
        print(f"  {prob['weather']}: {prob['probability']}%")

if __name__ == "__main__":
    test_detailed_prediction()