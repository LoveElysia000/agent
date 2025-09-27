#!/usr/bin/env python3
"""
最终测试 - 验证天气预测功能
"""
import sys
import os
from dotenv import load_dotenv

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from weather_tools import parse_and_predict_weather, predict_weather_trend

def test_final():
    """测试最终功能"""
    print("Final Weather Prediction Test")
    print("=" * 50)

    # 测试日期解析功能
    test_cases = [
        ("北京", "未来6小时"),
        ("上海", "未来3天"),
        ("广州", "10天后"),
        ("深圳", "2025-10-10"),
        ("杭州", "明天")
    ]

    for city, date_desc in test_cases:
        print(f"\nTesting: {city} - '{date_desc}'")
        print("-" * 30)

        result = parse_and_predict_weather.invoke({"city": city, "date_description": date_desc})

        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Type: {result['type']}")
            print(f"Recommended tool: {result['recommended_tool']}")
            print(f"Description: {result.get('description', 'N/A')}")

            # 如果是预测类型，测试预测功能
            if result['type'] == 'prediction':
                target_date = result.get('target_date')
                if target_date:
                    pred_result = predict_weather_trend.invoke({"city": city, "target_date": target_date})
                    if "error" in pred_result:
                        print(f"Prediction error: {pred_result['error']}")
                    else:
                        print(f"Predicted temp: {pred_result['prediction']['predicted_temperature']}°C")
                        print(f"Confidence: {pred_result['confidence']}")

if __name__ == "__main__":
    test_final()