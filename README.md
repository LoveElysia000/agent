# 天气预报Agent

基于LangChain框架构建的智能天气预报助手，使用Qwen3-Max模型和OpenWeatherMap API，提供精准的天气查询服务。

## 🌤️ 功能特性

- **智能对话**: 基于Qwen3-Max大语言模型，理解自然语言查询
- **实时天气**: 集成OpenWeatherMap API，获取全球实时天气数据
- **多语言支持**: 支持中文和英文查询与回复
- **全球覆盖**: 支持全球主要城市天气查询
- **完整气象数据**: 提供温度、湿度、风速、气压等数据
- **天气预报**: 提供当前天气状况和未来天气预报
- **城市比较**: 对比多个城市的天气状况
- **天气建议**: 基于天气情况给出活动和出行建议
- **命令行接口**: 支持多种命令行模式

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip包管理器

### 安装依赖

```bash
pip install langchain langchain-community langchain-openai requests python-dotenv openai
```

### API密钥配置

1. **获取OpenWeatherMap API密钥**
   - 访问 [OpenWeatherMap](https://openweathermap.org/api) 注册账号
   - 获取免费的API密钥（免费版支持1000次/天调用）

2. **获取Qwen API密钥**
   - 访问 [Alibaba Cloud DashScope](https://dashscope.aliyuncs.com/) 
   - 创建账户并获取API密钥

3. **配置环境变量**
   使用以下命令复制模板文件：
   ```bash
   cp .env.example .env
   ```
   然后编辑 `.env` 文件，填入您的实际API密钥：
   
   - 打开 `.env` 文件
   - 将 `your_openweather_api_key_here` 替换为您在OpenWeatherMap获取的API密钥
   - 将 `your_qwen_api_key_here` 替换为您在Alibaba DashScope获取的API密钥
   - 可选：修改默认城市和语言设置
   
   **示例 .env 文件内容：**
   ```bash
   # OpenWeatherMap API密钥
   OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
   
   # Qwen3-Max模型配置
   QWEN_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
   QWEN_API_KEY=your_qwen_api_key
   
   # 应用配置（可选）
   DEFAULT_CITY=Beijing
   LANGUAGE=zh
   ```
### 运行应用

#### 交互模式（默认）
```bash
python3 main.py
```

#### 命令行模式
```bash
# 查询单个城市天气
python3 main.py 北京

# 查询多天天气预报
python3 main.py --days 3 上海

# 比较两个城市天气
python3 main.py --compare 广州 北京

# 获取天气建议
python3 main.py --query "今天适合户外运动吗？" 北京

# 显示帮助信息
python3 main.py --help
```

## 📁 项目结构

```
weather/
├── .env                    # 环境配置文件
├── main.py                 # 主应用程序入口
├── model_config.py         # Qwen模型配置
├── weather_tools.py        # OpenWeatherMap API工具
├── weather_agent.py        # LangChain Agent核心逻辑
├── .venv/                  # Python虚拟环境
├── __pycache__/            # Python缓存文件
├── test_weather.py         # 功能测试脚本
└── README.md              # 项目说明文档
```

## 🔧 核心组件

### 命令行接口
新增的命令行接口支持多种模式：
- **单城市模式**: 查询单个城市当前天气 (`main.py 城市名`)
- **多天预报模式**: 查询城市未来天气 (`--days` 参数)
- **城市比较模式**: 比较两个城市的天气 (`--compare` 参数)  
- **问答模式**: 基于天气给出建议 (`--query` 参数)
- **交互模式**: 传统交互界面 (默认模式)

### WeatherAgent
智能天气预报代理，包含：
- 自然语言理解
- 工具调用决策
- 响应生成

### WeatherTools
天气数据工具集：
- `get_current_weather()`: 获取当前天气（包含温度、湿度、风速、气压等）
- `get_weather_forecast()`: 获取天气预报（每时段包含温度、湿度、风速、气压）
- `get_specific_day_weather()`: 获取指定日期天气
- `get_holiday_weather()`: 获取节假日期间天气

### ModelConfig
Qwen3-Max模型配置：
- API端点配置
- 模型参数调优
- 错误处理机制

## 🧪 测试

运行测试脚本验证功能：
```bash
python3 test_weather.py
```

## 🌟 示例输出

```
=== 天气预报Agent ===
基于Qwen3-Max模型和OpenWeatherMap API
==============================
✅ 天气预报Agent初始化成功

请输入城市名称查询天气 (输入'quit'退出):

🌤️  请输入城市: 北京天气

==================================================
📊 天气预报结果:
🌡️ 当前温度：25°C
🤒 体感温度：26°C  
☀️ 天气状况：晴转多云
💧 湿度：65%
💨 风速：3.5 m/s
⏲️ 气压：1012 hPa

建议您根据天气情况适时增减衣物。
==================================================

## 🌍 全球城市覆盖

#### 🌏 全球城市支持

支持全球主要城市天气查询，包括中国和国际城市：
- **中国城市**: 北京、上海、广州、深圳等
- **国际城市**: Tokyo、London、New York、Paris等

城市名称使用提示：
- 中国城市支持中文和拼音名称
- 国际城市建议使用英文名称  
- 包含空格的城市名请使用引号包裹

### 📊 视觉输出与图标系统

天气信息显示现在使用表情图标增强可读性：

| 图标 | 含义 | 描述 |
|------|------|------|
| 🌡️ | 温度 | 当前实际温度 |
| 🤒 | 体感温度 | 人体感觉的温度 |
| 💧 | 湿度 | 空气湿度百分比 |
| 💨 | 风速 | 风力大小 |
| ⏲️ | 气压 | 大气压力 |
| ☀️ | 晴天 | 晴好天气 |
| ☁️ | 多云 | 多云天气 |
| 🌧️ | 雨天 | 下雨天气 |
| ❄️ | 雪天 | 下雪天气 |
| ⛈️ | 雷雨 | 雷雨天气 |

### 示例输出

#### 城市比较示例
```bash
python3 main.py --compare 北京 上海
```

输出示例：
```
🏙️  城市天气比较结果:

**北京：**
🌡️ 温度：27.83°C
🤒 体感温度：27.17°C
☁️ 天气状况：阴，多云
💧 湿度：34%
💨 风速：0.34 m/s
⏲️ 气压：1019 hPa

**上海：**
🌡️ 温度：35.53°C
🤒 体感温度：42.53°C
☁️ 天气状况：多云
💧 湿度：52%
💨 风速：3.02 m/s
⏲️ 气压：1014 hPa
```

#### 天气建议示例
```bash
python3 main.py --query "今天适合户外运动吗" 北京
```

输出示例：
```
💡 天气建议/回答:
🌡️ 当前温度：28.38°C  
🤒 体感温度：27.38°C  
☁️ 天气状况：阴，多云  
💧 湿度：30%  
💨 风速：0.43 m/s  
⏲️ 气压：1018 hPa  

北京现在的天气是阴天，多云，气温适中，湿度较低，风力较小，气压正常。这样的天气条件适合进行户外运动。
```

## 🔍 技术架构

```
用户输入 → WeatherAgent → 工具选择 → OpenWeatherMap API → 数据处理 → 智能回复
                             ↳ Qwen3-Max模型
```

## 📝 开发说明

### 扩展新工具
在 `weather_tools.py` 中添加新的工具函数：
```python
@tool
def new_weather_tool(self, params):
    """工具描述"""
    # 实现逻辑
    return result
```

### 自定义模型配置
编辑 `model_config.py` 调整模型参数：
```python
def get_qwen_model():
    return ChatOpenAI(
        model="qwen-turbo",
        temperature=0.1,    # 调整创作性
        max_tokens=2000     # 调整响应长度
    )
```

## ⚠️ 注意事项

1. **API限制**: OpenWeatherMap免费版有调用限制，请合理使用
2. **密钥安全**: 不要将API密钥提交到版本控制系统
3. **网络要求**: 需要稳定的网络连接访问API服务
4. **地域限制**: 某些地区可能需要VPN访问外部服务


## 🙏 致谢

- [LangChain](https://github.com/langchain-ai/langchain) - 优秀的LLM应用框架
- [OpenWeatherMap](https://openweathermap.org/) - 提供准确的天气数据
- [Alibaba Cloud DashScope](https://dashscope.aliyuncs.com/) - 强大的Qwen模型服务

---

**开始使用智能天气预报Agent，让天气查询更便捷！** 🌈