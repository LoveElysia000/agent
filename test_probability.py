#!/usr/bin/env python3
"""
测试天气概率预测功能
"""
import sys
import os
from dotenv import load_dotenv

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from weather_tools import predict_weather_trend

def test_probability_prediction():
    """测试天气概率预测功能"""
    print("Testing Weather Probability Prediction")
    print("=" * 50)

    # 测试未来10天的预测
    print("\n1. Testing prediction for Beijing in 10 days:")
    result = predict_weather_trend.invoke({"city": "Beijing", "target_date": "2025-10-07"})

    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"City: {result['city']}")
        print(f"Target Date: {result['target_date']}")
        print(f"Days Ahead: {result['days_ahead']}")
        print(f"Confidence: {result['confidence']}")

        prediction = result['prediction']
        print(f"Predicted Temperature: {prediction['predicted_temperature']}°C")
        print(f"Temperature Trend: {prediction['temperature_trend']}")
        print(f"Season: {prediction['season']}")
        print(f"Typical Weather: {prediction['typical_weather']}")

        print("\nWeather Probabilities (sorted by probability):")
        for prob in prediction['weather_probabilities']:
            print(f"  {prob['icon']} {prob['weather']}: {prob['probability']}%")

        print(f"\nRecommendation: {prediction['recommendation']}")
        print(f"Data Source: {result['data_source']}")
        print(f"Limitation: {result['limitation']}")

if __name__ == "__main__":
    test_probability_prediction()