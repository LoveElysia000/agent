#!/usr/bin/env python3
"""
完整测试天气预测和解析功能
"""
import os
import sys
from dotenv import load_dotenv

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from weather_tools import parse_and_predict_weather, predict_weather_trend

def test_complete():
    """完整测试所有功能"""
    print("Complete Weather System Test")
    print("=" * 60)

    # 测试场景：各种日期描述
    test_cases = [
        ("北京", "未来6小时"),
        ("上海", "明天"),
        ("广州", "后天"),
        ("深圳", "未来3天"),
        ("北京", "未来10天"),
        ("上海", "2025-10-01"),
        ("广州", "大后天"),
        ("深圳", "2025-12-25")
    ]

    for city, date_desc in test_cases:
        print(f"\n测试: {city} - '{date_desc}'")
        print("-" * 40)

        # 智能解析
        result = parse_and_predict_weather.invoke({"city": city, "date_description": date_desc})

        if "error" in result:
            print(f"❌ 解析失败: {result['error']}")
            continue

        print(f"✅ 解析成功")
        print(f"类型: {result.get('type', 'N/A')}")
        print(f"描述: {result.get('description', 'N/A')}")
        print(f"推荐工具: {result.get('recommended_tool', 'N/A')}")

        # 如果是预测类型，执行预测
        if result.get('type') == 'prediction':
            target_date = result.get('target_date')
            if target_date:
                print(f"执行预测: {target_date}")
                pred_result = predict_weather_trend.invoke({"city": city, "target_date": target_date})
                if "error" not in pred_result:
                    pred = pred_result.get('prediction', {})
                    temp = pred.get('predicted_temperature')
                    if temp:
                        print(f"预测温度: {temp}°C")
                    print(f"季节: {pred.get('season', 'N/A')}")
                    print(f"趋势: {pred.get('temperature_trend', 'N/A')}")

        print("-" * 40)

    # 测试超出范围预测的准确性
    print("\n引入测试: 超出预报范围的预测")
    print("=" * 60)

    # 测试15天后的天气
    import datetime
    target_date = (datetime.datetime.now() + datetime.timedelta(days=15)).strftime("%Y-%m-%d")
    print(f"测试日期: {target_date}")

    result = predict_weather_trend.invoke({"city": "北京", "target_date": target_date})
    if "error" in result:
        print(f"❌ 预测失败: {result['error']}")
    else:
        print(f"✅ 预测成功")
        print(f"天数: {result['days_ahead']}")
        print(f"置信度: {result['confidence']}")
        print(f"数据源: {result['data_source']}")
        print(f"限制: {result['limitation']}")

        pred = result.get('prediction', {})
        print(f"预测温度: {pred.get('predicted_temperature', 'N/A')}°C")
        print(f"季节: {pred.get('season', 'N/A')}")
        print(f"典型天气: {pred.get('typical_weather', 'N/A')}")
        print(f"建议: {pred.get('recommendation', 'N/A')}")

if __name__ == "__main__":
    test_complete()