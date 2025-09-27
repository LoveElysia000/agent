#!/usr/bin/env python3
"""
简化测试天气概率预测功能
"""
import sys
import os
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from weather_tools import predict_weather_trend

def test_prob_simple():
    """简单测试概率预测"""
    print("Testing Weather Probabilities")
    print("=" * 40)

    # 测试未来的预测
    result = predict_weather_trend.invoke({"city": "Beijing", "target_date": "2025-10-07"})

    if "error" in result:
        print("Error:", result['error'])
    else:
        print("Success! Weather prediction with probabilities working.")

        prediction = result['prediction']
        print(f"Temperature: {prediction['predicted_temperature']}C")
        print(f"Season: {prediction['season']}")
        print(f"Confidence: {result['confidence']}")

        print("\nWeather Probabilities:")
        for prob in prediction['weather_probabilities']:
            print(f"  {prob['weather']}: {prob['probability']}%")

        print(f"\nTotal weather types: {len(prediction['weather_probabilities'])}")
        if prediction['weather_probabilities']:
            highest = prediction['weather_probabilities'][0]
            print(f"Most likely: {highest['weather']} ({highest['probability']}%)")

if __name__ == "__main__":
    test_prob_simple()