#!/usr/bin/env python3
"""
对比测试：展示改进前后的天气预测
"""
import sys
import os
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from weather_tools import predict_weather_trend

def test_comparison():
    """对比测试改进的效果"""
    print("Enhanced Weather Prediction Features")
    print("=" * 60)

    # 测试不同城市的预测
    test_cases = [
        ("北京", "2025-10-15"),
        ("上海", "2025-10-12"),
        ("广州", "2025-10-20")
    ]

    for city, target_date in test_cases:
        print(f"\n{city} - {target_date} 预测结果:")
        print("-" * 40)

        result = predict_weather_trend.invoke({"city": city, "target_date": target_date})

        if "error" in result:
            print(f"  错误: {result['error']}")
            continue

        pred = result['prediction']
        print(f"  🌡️ 温度: {pred['predicted_temperature']}度")
        print(f"  💧 湿度: {pred['predicted_humidity']}%")
        print(f"  💨 风速: {pred['predicted_wind_speed']}米/秒")
        print(f"  ☁️ 天气: {pred['predicted_weather_description']}")
        print(f"  📊 趋势: {pred['temperature_trend']}")
        print(f"  🍂 季节: {pred['season']}")

        if pred['weather_probabilities']:
            print("  🎯 最可能天气:", end="")
            for i, prob in enumerate(pred['weather_probabilities'][:2]):
                if i > 0:
                    print(" ,", end="")
                print(f" {prob['weather']}({prob['probability']}%)", end="")
            print()

        print(f"  💡 建议: {pred['recommendation']}")
        print(f"  📈 置信度: {result['confidence']}")

        print("-" * 40)

if __name__ == "__main__":
    test_comparison()