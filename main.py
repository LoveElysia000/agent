#!/usr/bin/env python3
"""
天气预报Agent主应用程序
使用Qwen3-Max模型和OpenWeatherMap API

Usage:
    python3 main.py [城市名称]                     # 查询指定城市的当前天气
    python3 main.py --days [天数] [城市名称]        # 查询城市的多天天气预报
    python3 main.py --compare [城市1] [城市2]       # 比较两个城市的天气
    python3 main.py --query "[问题]" [城市名称]     # 根据天气给出建议或回答
    python3 main.py --interactive                 # 进入交互模式(默认)
"""
import os
import sys
import argparse
from typing import Dict, Any
from dotenv import load_dotenv

from model_config import get_qwen_model
from weather_agent import WeatherAgent
from weather_tools import get_current_weather, get_weather_forecast

def setup_argparse():
    """设置命令行参数解析"""
    parser = argparse.ArgumentParser(description="天气预报Agent")
    
    parser.add_argument("city", nargs="?", help="城市名称（当使用交互模式时不需要）")
    parser.add_argument("--days", type=int, help="查询未来多少天的天气预报")
    parser.add_argument("--compare", nargs=2, metavar=("CITY1", "CITY2"), 
                       help="比较两个城市的天气")
    parser.add_argument("--query", nargs=2, metavar=("QUESTION", "CITY"),
                       help="根据天气给出建议或回答特定问题")
    parser.add_argument("--interactive", action="store_true", 
                       help="进入交互模式（默认）")
    
    return parser

def get_weather_data(city: str) -> Dict[str, Any]:
    """获取天气数据"""
    return get_current_weather(city)

def get_weather_forecast_data(city: str, days: int = 3) -> Dict[str, Any]:
    """获取天气预报数据"""
    return get_weather_forecast(city)

def compare_cities(agent: WeatherAgent, city1: str, city2: str) -> str:
    """比较两个城市的天气"""
    query = f"请比较{city1}和{city2}的天气情况，包括温度、天气状况、湿度、风速等，并给出总结"
    return agent.query(query)

def ask_weather_advice(agent: WeatherAgent, question: str, city: str) -> str:
    """根据天气情况给出建议"""
    query = f"对于{city}的天气情况，{question}"
    return agent.query(query)

def interactive_mode(agent: WeatherAgent):
    """交互模式"""
    print("\n请输入城市名称查询天气 (输入'quit'退出):")
    
    while True:
        user_input = input("\n🌤️  Ein: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("👋 感谢使用天气预报Agent，再见！")
            break
        
        if not user_input:
            continue
        
        # 处理用户查询
        try:
            response = agent.query(user_input)
            print("\n" + "=" * 50)
            print("📊 天气预报结果:")
            print(response)
            print("=" * 50)
        except Exception as e:
            print(f"❌ 查询失败: {e}")

def main():
    """主函数"""
    print("=== 天气预报Agent ===")
    print("基于Qwen3-Max模型和OpenWeatherMap API")
    print("=" * 30)
    
    # 加载环境变量
    load_dotenv()
    
    # 检查必要的配置
    if not os.getenv("OPENWEATHERMAP_API_KEY"):
        print("❌ 请在.env文件中配置OpenWeatherMap API密钥")
        print("请创建OpenWeatherMap账号并获取API密钥：https://openweathermap.org/api")
        sys.exit(1)
    
    if not os.getenv("QWEN_API_KEY"):
        print("❌ 请在.env文件中配置Qwen API密钥")
        print("请访问Alibaba Cloud DashScope获取API密钥")
        sys.exit(1)
    
    # 解析命令行参数
    parser = setup_argparse()
    args = parser.parse_args()
    
    # 初始化天气预报Agent
    try:
        agent = WeatherAgent()
        print("✅ 天气预报Agent初始化成功")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        sys.exit(1)
    
    # 根据参数选择模式
    if args.compare:
        # 城市比较模式
        city1, city2 = args.compare
        print(f"\n📊 正在比较 {city1} 和 {city2} 的天气情况...")
        
        result = compare_cities(agent, city1, city2)
        print("\n" + "=" * 60)
        print("🏙️  城市天气比较结果:")
        print(result)
        print("=" * 60)
        
    elif args.query:
        # 问答模式
        question, city = args.query
        print(f"\n🤔 正在针对{city}的天气情况回答问题: {question}")
        
        result = ask_weather_advice(agent, question, city)
        print("\n" + "=" * 60)
        print("💡 天气建议/回答:")
        print(result)
        print("=" * 60)
        
    elif args.days and args.city:
        # 多天预报模式
        print(f"\n📅 正在获取{args.city}未来{args.days}天的天气预报...")
        
        result = agent.query(f"请提供{args.city}未来{args.days}天的详细天气预报")
        print("\n" + "=" * 60)
        print(f"📊 {args.city}未来{args.days}天天气预报:")
        print(result)
        print("=" * 60)
        
    elif args.city:
        # 单城市模式
        print(f"\n🌤️  正在获取{args.city}的天气信息...")
        
        result = agent.query(f"{args.city}现在的天气怎么样？")
        print("\n" + "=" * 60)
        print(f"📊 {args.city}天气信息:")
        print(result)
        print("=" * 60)
        
    else:
        # 默认交互模式
        interactive_mode(agent)

def print_help():
    """打印帮助信息"""
    print("\n使用说明:")
    print("1. python3 main.py [城市名称]                    # 查询指定城市的当前天气")
    print("2. python3 main.py --days [天数] [城市名称]       # 查询城市的多天天气预报")
    print("3. python3 main.py --compare [城市1] [城市2]      # 比较两个城市的天气")
    print("4. python3 main.py --query \"[问题]\" [城市名称]    # 根据天气给出建议或回答")
    print("5. python3 main.py --interactive                # 进入交互模式(默认)")
    print("\n示例:")
    print("  • python3 main.py 北京")
    print("  • python3 main.py --days 3 上海")
    print("  • python3 main.py --compare 广州 北京")
    print("  • python3 main.py --query \"今天适合户外运动吗？\" 北京")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 程序被用户中断，再见！")
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")
        print_help()