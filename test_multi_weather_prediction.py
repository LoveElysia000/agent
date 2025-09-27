#!/usr/bin/env python3
"""
测试多天气类型独立预测功能
"""
import sys
import os
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from weather_tools import predict_weather_trend

def test_multi_weather_prediction():
    """测试多天气类型独立预测"""
    print("Testing Multi-Weather Type Prediction")
    print("=" * 60)

    # 测试预测功能
    result = predict_weather_trend.invoke({"city": "Beijing", "target_date": "2025-10-15"})

    if "error" in result:
        print(f"Error: {result['error']}")
        return

    print(f"City: {result['city']}")
    print(f"Target Date: {result['target_date']}")
    print(f"Days Ahead: {result['days_ahead']}")
    print(f"Confidence: {result['confidence']}")
    print()

    prediction = result['prediction']

    print("Overall Prediction:")
    print(f"Temperature: {prediction['predicted_temperature']}C")
    print(f"Humidity: {prediction['predicted_humidity']}%")
    print(f"Wind Speed: {prediction['predicted_wind_speed']}m/s")
    print(f"Main Weather: {prediction['predicted_weather_description']}")
    print()

    print("Individual Weather Type Predictions:")
    print("-" * 50)

    for i, wt_pred in enumerate(prediction['weather_type_predictions'], 1):
        print(f"{i}. {wt_pred['weather_type']} ({wt_pred['probability']}% probability)")
        print(f"   Temperature: {wt_pred['predicted_temperature']}C")
        print(f"   Humidity: {wt_pred['predicted_humidity']}%")
        print(f"   Wind Speed: {wt_pred['predicted_wind_speed']}m/s")
        print(f"   Description: {wt_pred['weather_description']}")
        print(f"   Suggestion: {wt_pred['suggestion']}")
        print(f"   Typical: {wt_pred['typical_conditions']}")
        print("-" * 50)

if __name__ == "__main__":
    test_multi_weather_prediction()