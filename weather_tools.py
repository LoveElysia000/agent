import os
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"

# Chinese city name to English mapping
CITY_MAPPING = {
    # 直辖市
    "北京": "Beijing",
    "上海": "Shanghai", 
    "天津": "Tianjin",
    "重庆": "Chongqing",
    
    # 省会城市
    "广州": "Guangzhou",
    "杭州": "Hangzhou",
    "成都": "Chengdu",
    "武汉": "Wuhan",
    "西安": "Xi'an",
    "南京": "Nanjing",
    "沈阳": "Shenyang",
    "长春": "Changchun",
    "哈尔滨": "Harbin",
    "石家庄": "Shijiazhuang",
    "太原": "Taiyuan",
    "济南": "Jinan",
    "郑州": "Zhengzhou",
    "合肥": "Hefei",
    "长沙": "Changsha",
    "南昌": "Nanchang",
    "福州": "Fuzhou",
    "贵阳": "Guiyang",
    "昆明": "Kunming",
    "兰州": "Lanzhou",
    "西宁": "Xining",
    "银川": "Yinchuan",
    "乌鲁木齐": "Urumqi",
    "拉萨": "Lhasa",
    "海口": "Haikou",
    "呼和浩特": "Hohhot",
    "南宁": "Nanning",
    
    # 经济特区/计划单列市
    "深圳": "Shenzhen",
    "厦门": "Xiamen",
    "大连": "Dalian",
    "青岛": "Qingdao",
    "宁波": "Ningbo",
    "珠海": "Zhuhai",
    "汕头": "Shantou",
    "湛江": "Zhanjiang",
    
    # 其他主要城市
    "苏州": "Suzhou",
    "无锡": "Wuxi",
    "常州": "Changzhou",
    "南通": "Nantong",
    "扬州": "Yangzhou",
    "镇江": "Zhenjiang",
    "徐州": "Xuzhou",
    "温州": "Wenzhou",
    "绍兴": "Shaoxing",
    "台州": "Taizhou",
    "金华": "Jinhua",
    "嘉兴": "Jiaxing",
    "湖州": "Huzhou",
    "舟山": "Zhoushan",
    "泉州": "Quanzhou",
    "漳州": "Zhangzhou",
    "莆田": "Putian",
    "三明": "Sanming",
    "龙岩": "Longyan",
    "南平": "Nanping",
    "宁德": "Ningde",
    "佛山": "Foshan",
    "东莞": "Dongguan",
    "中山": "Zhongshan",
    "江门": "Jiangmen",
    "肇庆": "Zhaoqing",
    "惠州": "Huizhou",
    "茂名": "Maoming",
    "阳江": "Yangjiang",
    "韶关": "Shaoguan",
    "清远": "Qingyuan",
    "潮州": "Chaozhou",
    "揭阳": "Jieyang",
    "云浮": "Yunfu",
    "烟台": "Yantai",
    "潍坊": "Weifang",
    "淄博": "Zibo",
    "济宁": "Jining",
    "泰安": "Tai'an",
    "临沂": "Linyi",
    "菏泽": "Heze",
    "德州": "Dezhou",
    "聊城": "Liaocheng",
    "滨州": "Binzhou",
    "东营": "Dongying",
    "威海": "Weihai",
    "日照": "Rizhao",
    "枣庄": "Zaozhuang",
    "莱芜": "Laiwu",
    "洛阳": "Luoyang",
    "开封": "Kaifeng",
    "新乡": "Xinxiang",
    "焦作": "Jiaozuo",
    "安阳": "Anyang",
    "濮阳": "Puyang",
    "许昌": "Xuchang",
    "漯河": "Luohe",
    "三门峡": "Sanmenxia",
    "南阳": "Nanyang",
    "商丘": "Shangqiu",
    "信阳": "Xinyang",
    "周口": "Zhoukou",
    "驻马店": "Zhumadian",
    "平顶山": "Pingdingshan",
    "鹤壁": "Hebi",
    "宜昌": "Yichang",
    "襄阳": "Xiangyang",
    "荆州": "Jingzhou",
    "黄石": "Huangshi",
    "十堰": "Shiyan",
    "孝感": "Xiaogan",
    "荆门": "Jingmen",
    "鄂州": "Ezhou",
    "黄冈": "Huanggang",
    "咸宁": "Xianning",
    "随州": "Suizhou",
    "恩施": "Enshi",
    "株洲": "Zhuzhou",
    "湘潭": "Xiangtan",
    "衡阳": "Hengyang",
    "邵阳": "Shaoyang",
    "岳阳": "Yueyang",
    "常德": "Changde",
    "张家界": "Zhangjiajie",
    "益阳": "Yiyang",
    "郴州": "Chenzhou",
    "永州": "Yongzhou",
    "怀化": "Huaihua",
    "娄底": "Loudi",
    "湘西": "Xiangxi",
    "九江": "Jiujiang",
    "赣州": "Ganzhou",
    "吉安": "Ji'an",
    "宜春": "Yichun",
    "抚州": "Fuzhou",
    "上饶": "Shangrao",
    "景德镇": "Jingdezhen",
    "萍乡": "Pingxiang",
    "新余": "Xinyu",
    "鹰潭": "Yingtan",
    "芜湖": "Wuhu",
    "蚌埠": "Bengbu",
    "淮南": "Huainan",
    "马鞍山": "Ma'anshan",
    "淮北": "Huaibei",
    "铜陵": "Tongling",
    "安庆": "Anqing",
    "黄山": "Huangshan",
    "滁州": "Chuzhou",
    "阜阳": "Fuyang",
    "宿州": "Suzhou",
    "六安": "Lu'an",
    "亳州": "Bozhou",
    "池州": "Chizhou",
    "宣城": "Xuancheng",
    "莆田": "Putian",
    "三明": "Sanming",
    "泉州": "Quanzhou",
    "漳州": "Zhangzhou",
    "南平": "Nanping",
    "龙岩": "Longyan",
    "宁德": "Ningde",
    "桂林": "Guilin",
    "柳州": "Liuzhou",
    "梧州": "Wuzhou",
    "北海": "Beihai",
    "防城港": "Fangchenggang",
    "钦州": "Qinzhou",
    "贵港": "Guigang",
    "玉林": "Yulin",
    "百色": "Baise",
    "贺州": "Hezhou",
    "河池": "Hechi",
    "来宾": "Laibin",
    "崇左": "Chongzuo",
    "三亚": "Sanya",
    "海口": "Haikou",
    "儋州": "Danzhou",
    "万宁": "Wanning",
    "东方": "Dongfang",
    "五指山": "Wuzhishan",
    "琼海": "Qionghai",
    "文昌": "Wenchang",
    "定安": "Ding'an",
    "屯昌": "Tunchang",
    "澄迈": "Chengmai",
    "临高": "Lingao",
    "白沙": "Baisha",
    "昌江": "Changjiang",
    "乐东": "Ledong",
    "陵水": "Lingshui",
    "保亭": "Baoting",
    "琼中": "Qiongzhong",
    "绵阳": "Mianyang",
    "德阳": "Deyang",
    "南充": "Nanchong",
    "宜宾": "Yibin",
    "达州": "Dazhou",
    "广安": "Guang'an",
    "遂宁": "Suining",
    "内江": "Neijiang",
    "乐山": "Leshan",
    "自贡": "Zigong",
    "泸州": "Luzhou",
    "攀枝花": "Panzhihua",
    "广元": "Guangyuan",
    "巴中": "Bazhong",
    "雅安": "Ya'an",
    "眉山": "Meishan",
    "资阳": "Ziyang",
    "阿坝": "Aba",
    "甘孜": "Ganzi",
    "凉山": "Liangshan",
    "遵义": "Zunyi",
    "安顺": "Anshun",
    "毕节": "Bijie",
    "铜仁": "Tongren",
    "六盘水": "Liupanshui",
    "黔东南": "Qiandongnan",
    "黔南": "Qiannan",
    "黔西南": "Qianxinan",
    "曲靖": "Qujing",
    "玉溪": "Yuxi",
    "保山": "Baoshan",
    "昭通": "Zhaotong",
    "丽江": "Lijiang",
    "普洱": "Pu'er",
    "临沧": "Lincang",
    "楚雄": "Chuxiong",
    "红河": "Honghe",
    "文山": "Wenshan",
    "西双版纳": "Xishuangbanna",
    "大理": "Dali",
    "德宏": "Dehong",
    "怒江": "Nujiang",
    "迪庆": "Diqing",
    "咸阳": "Xianyang",
    "宝鸡": "Baoji",
    "渭南": "Weinan",
    "汉中": "Hanzhong",
    "安康": "Ankang",
    "商洛": "Shangluo",
    "延安": "Yan'an",
    "榆林": "Yulin",
    "铜川": "Tongchuan",
    "嘉峪关": "Jiayuguan",
    "金昌": "Jinchang",
    "白银": "Baiyin",
    "天水": "Tianshui",
    "武威": "Wuwei",
    "张掖": "Zhangye",
    "平凉": "Pingliang",
    "酒泉": "Jiuquan",
    "庆阳": "Qingyang",
    "定西": "Dingxi",
    "陇南": "Longnan",
    "临夏": "Linxia",
    "甘南": "Gannan",
    "西宁": "Xining",
    "海东": "Haidong",
    "海北": "Haibei",
    "黄南": "Huangnan",
    "海南": "Hainan",
    "果洛": "Golog",
    "玉树": "Yushu",
    "海西": "Haixi",
    "银川": "Yinchuan",
    "石嘴山": "Shizuishan",
    "吴忠": "Wuzhong",
    "固原": "Guyuan",
    "中卫": "Zhongwei",
    "乌鲁木齐": "Urumqi",
    "克拉玛依": "Karamay",
    "吐鲁番": "Turpan",
    "哈密": "Hami",
    "昌吉": "Changji",
    "博尔塔拉": "Bortala",
    "巴音郭楞": "Bayingolin",
    "阿克苏": "Aksu",
    "克孜勒苏": "Kizilsu",
    "喀什": "Kashgar",
    "和田": "Hotan",
    "伊犁": "Ili",
    "塔城": "Tacheng",
    "阿勒泰": "Altay",
    "石河子": "Shihezi",
    "阿拉尔": "Alar",
    "图木舒克": "Tumxuk",
    "五家渠": "Wujiaqu",
    "北屯": "Beitun",
    "铁门关": "Tiemenguan",
    "双河": "Shuanghe",
    "可克达拉": "Kokdala",
    "昆玉": "Kunyu",
    "胡杨河": "Huyanghe",
    "新星": "Xinxing",
    "拉萨": "Lhasa",
    "日喀则": "Shigatse",
    "昌都": "Qamdo",
    "林芝": "Nyingchi",
    "山南": "Shannan",
    "那曲": "Nagqu",
    "阿里": "Ngari",
    "香港": "Hong Kong",
    "澳门": "Macau",
    "台湾": "Taiwan",
    "台北": "Taipei",
    "高雄": "Kaohsiung",
    "台中": "Taichung",
    "台南": "Tainan",
    "基隆": "Keelung",
    "新竹": "Hsinchu",
    "嘉义": "Chiayi",
    "桃园": "Taoyuan",
    "苗栗": "Miaoli",
    "彰化": "Changhua",
    "南投": "Nantou",
    "云林": "Yunlin",
    "屏东": "Pingtung",
    "宜兰": "Yilan",
    "花莲": "Hualien",
    "台东": "Taitung",
    "澎湖": "Penghu",
    "金门": "Kinmen",
    "马祖": "Matsu",
    "连江": "Lienchiang"
}

# Weather icons mapping
WEATHER_ICONS = {
    "temperature": "🌡️",
    "feels_like": "🤒", 
    "description": "☁️",
    "humidity": "💧",
    "wind_speed": "💨",
    "pressure": "⏲️",
    "sunny": "☀️",
    "cloudy": "☁️",
    "rainy": "🌧️",
    "snow": "❄️",
    "thunderstorm": "⛈️",
    "drizzle": "🌦️",
    "fog": "🌫️",
    "clear": "☀️"
}

def translate_city_name(city: str) -> str:
    """将中文城市名翻译为英文"""
    return CITY_MAPPING.get(city, city)

def get_weather_icon(weather_type: str, description: str = None) -> str:
    """获取天气图标"""
    if weather_type == "description" and description:
        # 根据天气描述返回对应图标
        if "晴" in description or "clear" in description:
            return WEATHER_ICONS["sunny"]
        elif "多云" in description or "cloud" in description:
            return WEATHER_ICONS["cloudy"]
        elif "雨" in description or "rain" in description:
            return WEATHER_ICONS["rainy"]
        elif "雪" in description or "snow" in description:
            return WEATHER_ICONS["snow"]
        elif "雷" in description or "thunder" in description:
            return WEATHER_ICONS["thunderstorm"]
        elif "雾" in description or "fog" in description:
            return WEATHER_ICONS["fog"]
        elif "毛毛雨" in description or "drizzle" in description:
            return WEATHER_ICONS["drizzle"]
    
    return WEATHER_ICONS.get(weather_type, "🌤️")

@tool
def get_current_weather(city: str) -> Dict[str, Any]:
    """获取指定城市的当前天气信息"""
    if not API_KEY:
        return {"error": "OpenWeatherMap API key not configured"}
    
    try:
        english_city = translate_city_name(city)
        url = f"{BASE_URL}/weather?q={english_city}&appid={API_KEY}&units=metric&lang=zh_cn"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "pressure": data["main"]["pressure"]
        }
    except requests.exceptions.RequestException as e:
        if "404" in str(e):
            return {"error": f"城市 '{city}' 未找到，请检查城市名称是否正确"}
        else:
            return {"error": f"天气API请求失败: {str(e)}"}
    except KeyError as e:
        return {"error": f"无效的响应格式: {str(e)}"}

@tool
def get_weather_forecast(city: str, days: int = 3) -> Dict[str, Any]:
    """获取指定城市的天气预报，每天返回三个主要时间段"""
    if not API_KEY:
        return {"error": "OpenWeatherMap API key not configured"}
    
    try:
        english_city = translate_city_name(city)
        url = f"{BASE_URL}/forecast?q={english_city}&appid={API_KEY}&units=metric&lang=zh_cn"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # 获取所有可用的预报数据，不再限制特定时间点
        forecast_by_date = {}
        for item in data["list"]:
            date = item["dt_txt"].split(" ")[0]  # 提取日期
            time = item["dt_txt"].split(" ")[1]  # 提取时间
            
            # 为每个时间点分配标签
            hour = int(time.split(":")[0])
            if 6 <= hour < 9:
                time_label = "清晨"
            elif 9 <= hour < 12:
                time_label = "上午"
            elif 12 <= hour < 15:
                time_label = "中午"
            elif 15 <= hour < 18:
                time_label = "下午"
            elif 18 <= hour < 21:
                time_label = "傍晚"
            else:
                time_label = "晚上"
            
            if date not in forecast_by_date:
                forecast_by_date[date] = []
            
            forecast_by_date[date].append({
                "datetime": item["dt_txt"],
                "time_label": time_label,
                "temperature": item["main"]["temp"],
                "description": item["weather"][0]["description"],
                "humidity": item["main"]["humidity"],
                "wind_speed": item["wind"]["speed"],
                "pressure": item["main"]["pressure"]
            })
        
        # 转换为列表格式，限制天数
        forecast = []
        dates = sorted(forecast_by_date.keys())[:days]
        for date in dates:
            forecast.extend(forecast_by_date[date])
        
        return {
            "city": data["city"]["name"],
            "forecast": forecast
        }
    except requests.exceptions.RequestException as e:
        if "404" in str(e):
            return {"error": f"城市 '{city}' 未找到，请检查城市名称是否正确"}
        else:
            return {"error": f"天气预报API请求失败: {str(e)}"}
    except KeyError as e:
        return {"error": f"无效的响应格式: {str(e)}"}

# 法定假日数据库 - 2025年固定日期
FIXED_HOLIDAYS_2025 = {
    "元旦": ("2025-01-01", "2025-01-01"),
    "春节": ("2025-01-29", "2025-02-04"),  # 待确认，通常是除夕到初六
    "清明节": ("2025-04-04", "2025-04-06"),
    "劳动节": ("2025-05-01", "2025-05-05"),
    "端午节": ("2025-05-31", "2025-06-02"),
    "中秋节": ("2025-10-01", "2025-10-03"),  # 与国庆节重叠
    "国庆节": ("2025-10-01", "2025-10-07"),
}

# 法定假日别名映射
HOLIDAY_ALIASES = {
    "元旦": ["new year", "新年"],
    "春节": ["春节", "春节假期", "过年", "农历新年"],
    "清明节": ["清明节", "清明"],
    "劳动节": ["劳动节", "五一", "五一假期"],
    "端午节": ["端午节", "端午", "龙舟节"],
    "中秋节": ["中秋节", "中秋", "月饼节"],
    "国庆节": ["国庆节", "国庆", "十一", "国庆假期"],
}

@tool
def check_holiday_date_range(holiday_name: str) -> Dict[str, Any]:
    """查询指定法定假日的准确日期范围，并检查预报数据是否覆盖全假期
    
    Args:
        holiday_name: 假日名称，支持中文常用称呼
        
    Returns:
        包含开始日期、结束日期、天数和数据可用性的字典
    """
    # 查找对应的标准假日名称
    normalized_holiday = None
    for holiday, aliases in HOLIDAY_ALIASES.items():
        if holiday_name in aliases or holiday_name == holiday:
            normalized_holiday = holiday
            break
    
    if not normalized_holiday:
        return {
            "error": f"未找到法定假日 '{holiday_name}'，支持的假日包括：元旦、春节、清明节、劳动节、端午节、中秋节、国庆节"
        }
    
    if normalized_holiday in FIXED_HOLIDAYS_2025:
        start_date, end_date = FIXED_HOLIDAYS_2025[normalized_holiday]
        
        # 计算天数
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        days_count = (end_dt - start_dt).days + 1
        
        # 检查当前日期，判断预报数据是否能覆盖整个假期
        today = datetime.now()
        forecast_end_date = today + timedelta(days=5)  # OpenWeatherMap一般提供5-7天预报
        forecast_start_date = today - timedelta(days=1)  # 通常也能查询过去1天
        forecast_end_date_str = forecast_end_date.strftime("%Y-%m-%d")
        forecast_start_date_str = forecast_start_date.strftime("%Y-%m-%d")
        
        data_coverage = "无法覆盖全假期"
        warning = ""
        
        if start_date > forecast_end_date_str:
            data_coverage = "远未来假期"
            warning = f"注意：{normalized_holiday} ({start_date}) 超出了天气预报的覆盖范围"
        elif end_date > forecast_end_date_str:
            data_coverage = "部分覆盖"
            warning = f"注意：{normalized_holiday} 的部分日期超出了天气预报的覆盖范围"
        elif start_date < forecast_start_date_str:
            data_coverage = "过去假期"
            warning = f"注意：{normalized_holiday} 已经结束，天气预报主要提供未来天气"
        else:
            data_coverage = "完全覆盖"
        
        return {
            "holiday": normalized_holiday,
            "start_date": start_date,
            "end_date": end_date,
            "days": days_count,
            "year": "2025",
            "data_coverage": data_coverage,
            "warning": warning
        }
    
    return {"error": f"法定假日 '{normalized_holiday}' 日期信息缺失"}

@tool
def get_holiday_weather(city: str, holiday_name: str) -> Dict[str, Any]:
    """获取指定城市在法定假日期间的天气预报
    
    Args:
        city: 城市名称
        holiday_name: 假日名称
        
    Returns:
        包含假日信息和对应天气预报的字典
    """
    # 先查询假日日期范围
    holiday_info_resp = check_holiday_date_range.run({"holiday_name": holiday_name})
    if "error" in holiday_info_resp:
        return holiday_info_resp
    
    # 获取天气预报 - 使用较大的天数确保覆盖可能的假期
    weather_data_resp = get_weather_forecast.run({"city": city, "days": 7})  # 获取最大可用预报
    if "error" in weather_data_resp:
        return weather_data_resp
    
    # 过滤出假日期间的天气预报
    holiday_forecast = []
    start_date = holiday_info_resp["start_date"]
    end_date = holiday_info_resp["end_date"]
    
    for forecast_item in weather_data_resp["forecast"]:
        forecast_date = forecast_item["datetime"].split(" ")[0]
        if start_date <= forecast_date <= end_date:
            holiday_forecast.append(forecast_item)
    
    return {
        "holiday_info": holiday_info_resp,
        "city": weather_data_resp["city"],
        "holiday_forecast": holiday_forecast,
        "available_days": len(set(item["datetime"].split()[0] for item in holiday_forecast)),  # 实际可用的不同日期数量
        "total_holiday_days": holiday_info_resp["days"]
    }

@tool
def get_specific_day_weather(city: str, day_desc: str) -> Dict[str, Any]:
    """获取指定城市在特定日期的天气预报
    
    Args:
        city: 城市名称
        day_desc: 日期描述（如'明天'、'后天'）
        
    Returns:
        包含特定日期天气预报的字典
    """
    from datetime import datetime, timedelta
    
    # 计算目标日期
    today = datetime.now()
    if day_desc == "明天":
        target_date = today + timedelta(days=1)
    elif day_desc == "后天":
        target_date = today + timedelta(days=2)
    elif day_desc == "大后天":
        target_date = today + timedelta(days=3)
    else:
        return {"error": f"不支持的时间描述：{day_desc}，支持：明天、后天、大后天"}
    
    target_date_str = target_date.strftime("%Y-%m-%d")
    
    # 计算需要的预报天数
    days_needed = (target_date - today).days + 1  # 包含当天
    
    # 获取天气预报
    weather_data_resp = get_weather_forecast.run({"city": city, "days": days_needed})
    if "error" in weather_data_resp:
        return weather_data_resp
    
    # 过滤出目标日期的天气预报
    target_day_forecast = []
    for forecast_item in weather_data_resp["forecast"]:
        forecast_date = forecast_item["datetime"].split(" ")[0]
        if forecast_date == target_date_str:
            target_day_forecast.append(forecast_item)
    
    return {
        "city": weather_data_resp["city"],
        "target_date": target_date_str,
        "day_description": day_desc,
        "forecast": target_day_forecast,
        "forecast_found": len(target_day_forecast) > 0
    }

def get_weather_tools():
    """返回天气工具列表"""
    return [get_current_weather, get_weather_forecast, check_holiday_date_range, get_holiday_weather, get_specific_day_weather]