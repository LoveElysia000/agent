#!/usr/bin/env python3
"""
简化测试 - 直接测试预测功能
"""
import sys
import os
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

from weather_tools import predict_weather_trend
import datetime

def test_simple():
    """简单测试预测功能"""
    print("Simple Weather Prediction Test")
    print("=" * 40)

    # 测试超出预报范围的日期
    target_date = (datetime.datetime.now() + datetime.timedelta(days=20)).strftime("%Y-%m-%d")
    print(f"Testing prediction for Beijing on {target_date}")

    result = predict_weather_trend.invoke({"city": "Beijing", "target_date": target_date})

    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Success! Predicted temperature: {result['prediction']['predicted_temperature']}°C")
        print(f"Season: {result['prediction']['season']}")
        print(f"Confidence: {result['confidence']}")

if __name__ == "__main__":
    test_simple()