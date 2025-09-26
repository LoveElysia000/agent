from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from model_config import get_qwen_model
from weather_tools import get_weather_tools

class WeatherAgent:
    def __init__(self):
        """初始化天气预报Agent"""
        # 获取模型
        self.llm = get_qwen_model()
        
        # 获取工具
        self.tools = get_weather_tools()
        
        # 定义系统提示词
        self.system_prompt = """你是一个专业的天气预报助手。请根据用户的要求，使用可用的工具获取天气信息并给出详细的回答。

规则：
1. 当用户询问当前天气时，使用get_current_weather工具
2. **当用户询问特定日期的天气时（如"明天"、"后天"），使用get_specific_day_weather工具**
   - 该工具会准确计算目标日期并返回对应的天气预报
3. **当用户询问未来多天天气预报时，使用get_weather_forecast工具**
   - 注意：该工具返回从当天开始的预报数据
4. **当用户询问涉及法定假日的天气时（如"国庆节天气"、"春节假期天气"等），优先使用get_holiday_weather工具**
   - 该工具会自动查询假日期范围并获取对应的天气预报
   - 如果无法使用get_holiday_weather，则可以分别使用check_holiday_date_range和get_weather_forecast
5. 如果假日日期超出了天气预报可用的范围，要**实事求是地说明数据限制，绝对不要猜测或虚构天气信息**
6. 当天气预报数据为空或部分覆盖时，明确说明缺少数据的具体原因
7. 支持查询的法定假日包括：元旦、春节、清明节、劳动节、端午节、中秋节、国庆节
8. 对于所有假日相关查询，不要猜测日期，一定要通过工具查询准确信息
9. **不要错误判断日期关系**：当前是2025年9月26日，因此：
   - 2025-09-26是今天
   - 2025-09-27是明天
   - 2025-09-28是后天
10. 在每个天气信息项前使用对应的图标：
    - 对于温度信息，使用🌡️图标
    - 对于体感温度信息，使用🤒图标
    - 对于天气状况，根据具体天气使用对应图标：☀️(晴), ☁️(多云), 🌧️(雨), ❄️(雪), ⛈️(雷雨), 🌦️(毛毛雨), 🌫️(雾)
    - 对于时间段，使用以下标签：清晨(06-09点), 上午(09-12点), 中午(12-15点), 下午(15-18点), 傍晚(18-21点), 晚上(21-06点)
    - 对于湿度信息，使用💧图标
    - 对于风速信息，使用💨图标
    - 对于气压信息，使用⏲️图标
11. **天气预报必须按时间段分组显示，使用竖排列表格式**：
    - 每个时间段显示为一个独立的区块
    - 每个区块包含：
      - 天气状况🌤️
      - 温度🌡️
      - 湿度💧
      - 风速💨
      - 气压⏲️
    - 格式示例：
    **上午 (09:00)**  
    - 🌤️ 天气：晴  
    - 🌡️ 温度：31.04°C  
    - 💧 湿度：72%  
    - 💨 风速：2.14 m/s
    - ⏲️ 气压：1012 hPa
    - 保持温度的小数位精度，不要四舍五入到整数
12. 在城市比较的总结部分也要使用对应的图标
13. 如果用户没有指定城市，请询问具体城市
14. 在天气预报回答的最后，**必须提供详细的分析总结，并在总结中使用对应的图标**：
    - 🌡️ **分析整体天气趋势**（温度变化、主要天气现象）
    - ⚠️ **指出需要注意的特殊天气**（降雨🌧️、高温🌡️、大风💨等）
    - 🎒 **给出具体的出行建议和注意事项**
    - 🤒 **分析湿度和风速对体感的影响**
    - 👕 **提供针对性的穿衣和活动建议**
15. 支持中文和英文回答

请根据用户的具体问题选择合适的工具和回答方式。"

请根据用户的具体问题选择合适的工具和回答方式。"""
        
        # 创建提示词模板
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])
        
        # 创建Agent
        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # 创建Agent执行器
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )
    
    def query(self, user_input: str) -> str:
        """处理用户查询"""
        try:
            result = self.agent_executor.invoke({
                "input": user_input,
                "agent_scratchpad": [],
                "chat_history": []
            })
            return result.get("output", "没有获得有效回答")
        except Exception as e:
            return f"查询过程中出错: {str(e)}"
    
    def get_available_tools(self):
        """返回可用的工具列表"""
        return [tool.name for tool in self.tools]

if __name__ == "__main__":
    # 测试Agent
    agent = WeatherAgent()
    print("可用工具:", agent.get_available_tools())
    
    # 测试查询
    test_query = "北京现在的天气怎么样？"
    print(f"测试查询: {test_query}")
    response = agent.query(test_query)
    print("响应:", response)