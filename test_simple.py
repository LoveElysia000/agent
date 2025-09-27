#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from weather_tools import get_hourly_weather_forecast

def test_simple():
    """简单测试"""
    print("Testing hourly weather forecast")
    print("=" * 40)

    # 测试小时间隔查询
    result = get_hourly_weather_forecast.invoke({"city": "北京", "hours": 6})

    if "error" in result:
        print("Error:", result['error'])
    else:
        print(f"Success: Got {result['city']} weather for {result['hours']} hours")
        print(f"Available data points: {result['available_hours']}")

        # 显示第一个小时的数据
        if result['hourly_forecast']:
            first = result['hourly_forecast'][0]
            print("\nFirst hour data:")
            print(f"  Time: {first['datetime']}")
            print(f"  Hours from now: {first['hours_from_now']}")
            print(f"  Temperature: {first['temperature']}°C")
            print(f"  Weather: {first['description']}")

if __name__ == "__main__":
    test_simple()