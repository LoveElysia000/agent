#!/usr/bin/env python3
"""
测试Agent对小时间隔天气查询的理解和响应
"""
import os
import sys
from dotenv import load_dotenv
from weather_agent import WeatherAgent

def test_agent_hourly():
    """测试Agent对小时间隔天气查询的响应"""
    # 加载环境变量
    load_dotenv()

    # 检查API密钥
    if not os.getenv("OPENWEATHERMAP_API_KEY"):
        print("❌ 请在.env文件中配置OpenWeatherMap API密钥")
        return

    if not os.getenv("QWEN_API_KEY"):
        print("❌ 请在.env文件中配置Qwen API密钥")
        return

    # 初始化Agent
    try:
        agent = WeatherAgent()
        print("✅ 天气预报Agent初始化成功")
        print("可用工具:", agent.get_available_tools())
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return

    print("\n🧪 测试小时间隔天气查询理解能力")
    print("=" * 60)

    # 测试用例数组
    test_cases = [
        "北京未来6小时天气",
        "上海未来12小时天气情况",
        "广州未来3小时的天气预报",
        "深圳未来24小时天气",
        "未来8小时天气 北京"
    ]

    for i, query in enumerate(test_cases, 1):
        print(f"\n{i}. 测试查询: {query}")
        print("-" * 40)

        try:
            response = agent.query(query)
            print("🤖 Agent响应:")
            print(response)
            print("-" * 40)
        except Exception as e:
            print(f"❌ 查询失败: {e}")

    print("\n✅ 测试完成")

if __name__ == "__main__":
    test_agent_hourly()