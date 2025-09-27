#!/usr/bin/env python3
"""
测试小时间隔天气查询功能
"""
import os
import sys
from dotenv import load_dotenv
from weather_tools import get_hourly_weather_forecast

def test_hourly_weather():
    """测试小时间隔天气查询"""
    # 加载环境变量
    load_dotenv()

    # 检查API密钥
    if not os.getenv("OPENWEATHERMAP_API_KEY"):
        print("❌ 请在.env文件中配置OpenWeatherMap API密钥")
        return

    # 测试小时间隔查询
    print("🧪 测试小时间隔天气查询功能")
    print("=" * 50)

    # 测试1: 未来6小时天气
    print("\n1. 测试未来6小时天气查询:")
    result = get_hourly_weather_forecast.invoke({"city": "北京", "hours": 6})

    if "error" in result:
        print(f"❌ 错误: {result['error']}")
    else:
        print(f"✅ 成功获取 {result['city']} 未来{result['hours']}小时天气预报")
        print(f"📊 可用数据点: {result['available_hours']} 个")

        # 显示前几个小时的天气数据
        for i, forecast in enumerate(result['hourly_forecast'][:3]):
            print(f"\n  时间: {forecast['datetime']}")
            print(f"  距离现在: {forecast['hours_from_now']} 小时")
            print(f"  🌡️ 温度: {forecast['temperature']}°C")
            print(f"  🤒 体感温度: {forecast['feels_like']}°C")
            print(f"  🌤️ 天气: {forecast['description']}")
            print(f"  💧 湿度: {forecast['humidity']}%")
            print(f"  💨 风速: {forecast['wind_speed']} m/s")
            print(f"  ⏲️ 气压: {forecast['pressure']} hPa")

    # 测试2: 未来12小时天气
    print("\n2. 测试未来12小时天气查询:")
    result = get_hourly_weather_forecast("上海", 12)

    if "error" in result:
        print(f"❌ 错误: {result['error']}")
    else:
        print(f"✅ 成功获取 {result['city']} 未来{result['hours']}小时天气预报")
        print(f"📊 可用数据点: {result['available_hours']} 个")

    # 测试3: 边界情况测试
    print("\n3. 测试边界情况:")

    # 测试小时数限制
    result = get_hourly_weather_forecast("北京", 60)  # 超过48小时
    print(f"输入60小时，实际获取: {result['hours']} 小时")

    result = get_hourly_weather_forecast("北京", 0)   # 小于1小时
    print(f"输入0小时，实际获取: {result['hours']} 小时")

if __name__ == "__main__":
    test_hourly_weather()