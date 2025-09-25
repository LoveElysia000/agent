# 天气预报Agent

基于LangChain框架构建的智能天气预报助手，使用Qwen3-Max模型和OpenWeatherMap API，提供精准的天气查询和预测服务。

## 🌤️ 功能特性

- **智能对话**: 基于Qwen3-Max大语言模型，理解自然语言查询
- **实时天气**: 集成OpenWeatherMap API，获取全球实时天气数据
- **多语言支持**: 支持中文和英文查询与回复
- **全球覆盖**: 支持全球主要城市天气查询，包括中国300+城市和国际城市
- **天气预报**: 提供当前天气状况和未来天气预报
- **城市比较**: 对比多个城市的天气状况，提供分析总结
- **天气建议**: 基于天气情况给出活动和出行建议
- **命令行接口**: 支持多种命令行模式，脚本化使用
- **视觉输出**: 使用表情图标增强可读性和用户体验
- **结构化预报**: 每天提供上午、下午、晚上三个时段的清晰预报
- **交互式界面**: 友好的终端交互界面（默认模式）

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip包管理器

### 安装依赖

```bash
pip install langchain langchain-community langchain-openai requests python-dotenv openai httpx
```

### API密钥配置

1. **获取OpenWeatherMap API密钥**
   - 访问 [OpenWeatherMap](https://openweathermap.org/api) 注册账号
   - 获取免费的API密钥（免费版支持1000次/天调用）

2. **获取Qwen API密钥**
   - 访问 [Alibaba Cloud DashScope](https://dashscope.aliyuncs.com/) 
   - 创建账户并获取API密钥

3. **配置环境变量**
   **使用 cp 命令复制模板**
      ```bash
      cp .env.example .env
      ```
    然后编辑 `.env` 文件，填入您的实际API密钥。
# 天气预报Agent配置文件

# OpenWeatherMap API密钥
OPENWEATHERMAP_API_KEY=your_openweather_api_key_here

# Qwen3-Max模型配置
QWEN_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
QWEN_API_KEY=your_qwen_api_key_here

# 应用配置
DEFAULT_CITY=Beijing
LANGUAGE=zh
EOF
   ```
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

## 📋 使用方法

### 命令行模式

#### 单城市查询
```bash
# 查询当前天气
python3 main.py 北京

# 查询英文城市
python3 main.py London
```

#### 多天预报
```bash
# 查询未来3天预报
python3 main.py --days 3 上海

# 查询未来5天预报  
python3 main.py --days 5 Beijing
```

#### 城市比较
```bash
# 比较两个城市的天气
python3 main.py --compare 广州 北京
python3 main.py --compare "New York" London
```

#### 天气建议
```bash
# 获取基于天气的建议
python3 main.py --query "今天适合户外运动吗？" 北京
python3 main.py --query "需要带雨伞吗" 上海
python3 main.py --query "What should I wear today?" Tokyo
```

### 交互模式

运行 `python3 main.py` (不添加任何参数) 进入交互模式：

#### 基础查询
```
北京天气
上海现在的天气怎么样
纽约温度
```

#### 高级查询
```
上海今天会下雨吗
北京未来三天的天气预报
东京明天天气如何
```

#### 英文查询
```
What's the weather in London?
Weather forecast for Paris tomorrow
Will it rain in Tokyo next week?
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
- `get_current_weather()`: 获取当前天气
- `get_weather_forecast()`: 获取天气预报

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

### 🌏 支持的城市范围

#### 中国城市 (300+城市)
- **直辖市**: 北京、上海、天津、重庆
- **省会城市**: 广州、杭州、成都、武汉、西安等
- **经济特区**: 深圳、厦门、珠海等
- **其他主要城市**: 苏州、无锡、常州、温州、佛山等
- **地级市全覆盖**: 几乎覆盖所有地级市

#### 国际城市
- **亚洲**: 东京(Tokyo)、新加坡(Singapore)、首尔(Seoul)、曼谷(Bangkok)等
- **欧洲**: 伦敦(London)、巴黎(Paris)、柏林(Berlin)、罗马(Rome)等
- **美洲**: 纽约(New York)、洛杉矶(Los Angeles)、多伦多(Toronto)等
- **大洋洲**: 悉尼(Sydney)、墨尔本(Melbourne)、奥克兰(Auckland)等

### 🔍 城市查询示例

#### 中国城市查询
```bash
python3 main.py 北京
python3 main.py 苏州
python3 main.py "重庆"
```

#### 国际城市查询
```bash
python3 main.py Tokyo
python3 main.py "New York"
python3 main.py London
python3 main.py Paris
python3 main.py Sydney
```

#### 多语言混合查询
```bash
# 中日混合
python3 main.py "东京天气怎么样"

# 中英混合
python3 main.py "What's the weather in 上海"

# 英文查询中文城市
python3 main.py "Beijing weather"
```

### ⚠️ 城市名称注意事项
- 中国城市支持中文名称和拼音名称
- 国际城市建议使用英文名称
- 如果城市包含空格，请使用引号包裹
- 系统会自动识别和翻译城市名称

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

### 命令行模式示例输出

#### 城市比较
```bash
python3 main.py --compare 北京 上海
```

输出：
```
🏙️  城市天气比较结果:
根据当前天气信息，北京和上海的天气情况如下：

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

**总结：**
- 北京的气温比上海低，但湿度较低，风速也较小。
- 上海的气温较高，且湿度较大，体感温度明显高于实际温度，风速也相对较高。
```

#### 天气建议
```bash
python3 main.py --query "今天适合户外运动吗" 北京
```

输出：
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

#### 多天预报
```bash
python3 main.py --days 3 北京
```

输出：
```
📊 北京未来3天天气预报:
以下是北京未来3天的详细天气预报：

### 2025年9月25日（今天）
- **上午**：
  - 🌤️ 天气状况：多云
  - 🌡️ 温度：28.19°C
  - 💧 湿度：29%
  - 💨 风速：0.66 m/s

- **下午**：
  - 🌤️ 天气状况：阴，多云
  - 🌡️ 温度：23.07°C
  - 💧 湿度：43%
  - 💨 风速：0.68 m/s

- **晚上**：
  - 🌤️ 天气状况：阴，多云
  - 🌡️ 温度：20.33°C
  - 💧 湿度：52%
  - 💨 风速：1.64 m/s

---

### 2025年9月26日（明天）
- **上午**：
  - 🌤️ 天气状况：阴，多云
  - 🌡️ 温度：28.23°C
  - 💧 湿度：31%
  - 💨 风速：2.65 m/s

- **下午**：
  - 🌤️ 天气状况：多云
  - 🌡️ 温度：21.87°C
  - 💧 湿度：54%
  - 💨 风速：1.11 m/s

- **晚上**：
  - 🌤️ 天气状况：阴，多云
  - 🌡️ 温度：20.02°C
  - 💧 湿度：57%
  - 💨 风速：0.54 m/s

---

### 2025年9月27日（后天）
- **上午**：
  - 🌧️ 天气状况：小雨
  - 🌡️ 温度：16.59°C
  - 💧 湿度：91%
  - 💨 风速：1.04 m/s

- **下午**：
  - 🌧️ 天气状况：小雨
  - 🌡️ 温度：16.96°C
  - 💧 湿度：90%
  - 💨 风速：1.72 m/s

- **晚上**：
  - 🌤️ 天气状况：多云
  - 🌡️ 温度：15.72°C
  - 💧 湿度：96%
  - 💨 风速：0.71 m/s

请注意，未来几天可能会有降雨，建议外出携带雨具。祝您出行顺利！
```

#### 国际城市预报示例
```bash
python3 main.py --days 3 Paris
```

输出：
```
📊 Paris未来3天天气预报:
以下是巴黎未来3天的详细天气预报：

### 第一天（2025-09-25）
- **上午**：
  🌤️ 天气：阴，多云
  🌡️ 温度：9.87°C
  💧 湿度：86%
  💨 风速：2.51 m/s

- **下午**：
  🌤️ 天气：阴，多云
  🌡️ 温度：10.81°C
  💧 湿度：66%
  💨 风速：3.1 m/s

- **晚上**：
  🌤️ 天气：阴，多云
  🌡️ 温度：10.04°C
  💧 湿度：73%
  💨 风速：2.47 m/s

#### 城市比较示例
```bash
python3 main.py --compare Tokyo London
```

输出：
```
🏙️  城市天气比较结果:
🌡️ **Tokyo当前温度**: 26.85°C  
🤒 **体感温度**: 27.51°C  
☀️ **天气状况**: 晴  
💧 **湿度**: 54%  
💨 **风速**: 6.6 m/s  
⏲️ **气压**: 1017 hPa  

---

🌡️ **London当前温度**: 8.64°C  
🤒 **体感温度**: 6.76°C  
☁️ **天气状况**: 多云  
💧 **湿度**: 77%  
💨 **风速**: 3.19 m/s  
⏲️ **气压**: 1025 hPa  

### 总结：
- **温度对比**：Tokyo的气温明显高于London，目前是温暖的天气，而London则较为凉爽。
- **天气状况**：Tokyo是晴天，适合户外活动；London则是多云，可能有轻微的阴天影响。
- **湿度和风速**：Tokyo的湿度较低，风速较高；London的湿度较高，风速较低。
- **气压**：Tokyo的气压略低于London。

如需更详细的天气信息，请随时告知。
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