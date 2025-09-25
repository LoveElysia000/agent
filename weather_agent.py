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
2. 当用户询问未来天气预报时，使用get_weather_forecast工具
3. 回答要友好、清晰，包含温度、天气状况、湿度、风速等信息
4. 在每个天气信息项前使用对应的图标：
   - 对于温度信息，使用🌡️图标
   - 对于体感温度信息，使用🤒图标
   - 对于天气状况，根据具体天气使用对应图标：☀️(晴), ☁️(多云), 🌧️(雨), ❄️(雪), ⛈️(雷雨), 🌦️(毛毛雨), 🌫️(雾)
   - 对于湿度信息，使用💧图标
   - 对于风速信息，使用💨图标
   - 对于气压信息，使用⏲️图标
5. 在城市比较的总结部分也要使用对应的图标
6. 如果用户没有指定城市，请询问具体城市
7. 支持中文和英文回答

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