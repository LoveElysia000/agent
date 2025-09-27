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

@tool
def get_hourly_weather_forecast(city: str, hours: int) -> Dict[str, Any]:
    """获取指定城市未来指定小时数的天气预报，以1小时为间隔

    Args:
        city: 城市名称
        hours: 小时数（如6表示未来6小时，最大不超过48小时）

    Returns:
        包含每小时天气预报的字典
    """
    if not API_KEY:
        return {"error": "OpenWeatherMap API key not configured"}

    # 限制小时数不超过48小时（OpenWeatherMap API的限制）
    hours = min(max(1, hours), 48)

    try:
        english_city = translate_city_name(city)
        url = f"{BASE_URL}/forecast?q={english_city}&appid={API_KEY}&units=metric&lang=zh_cn"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # 获取当前时间
        current_time = datetime.now()

        # 获取预测数据
        hourly_forecast = []
        for item in data["list"]:
            forecast_time = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S")
            time_diff = (forecast_time - current_time).total_seconds() / 3600  # 转换为小时

            # 只获取未来指定小时内的数据
            if 0 <= time_diff <= hours:
                hourly_forecast.append({
                    "datetime": item["dt_txt"],
                    "hours_from_now": round(time_diff, 1),
                    "temperature": item["main"]["temp"],
                    "feels_like": item["main"]["feels_like"],
                    "description": item["weather"][0]["description"],
                    "humidity": item["main"]["humidity"],
                    "wind_speed": item["wind"]["speed"],
                    "pressure": item["main"]["pressure"]
                })

        return {
            "city": data["city"]["name"],
            "hours": hours,
            "hourly_forecast": hourly_forecast,
            "available_hours": len(hourly_forecast)
        }
    except requests.exceptions.RequestException as e:
        if "404" in str(e):
            return {"error": f"城市 '{city}' 未找到，请检查城市名称是否正确"}
        else:
            return {"error": f"天气预报API请求失败: {str(e)}"}
    except KeyError as e:
        return {"error": f"无效的响应格式: {str(e)}"}

@tool
def parse_and_predict_weather(city: str, date_description: str) -> Dict[str, Any]:
    """根据日期描述解析并选择最适合的天气查询工具

    Args:
        city: 城市名称
        date_description: 日期描述（如"未来6小时"、"明天"、"2025-10-01"）

    Returns:
        包含解析结果和推荐工具的信息
    """
    from datetime import datetime, timedelta

    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")

    # 解析日期描述
    if "小时" in date_description:
        # 小时间隔查询
        try:
            hours = int(''.join(filter(str.isdigit, date_description)))
            hours = min(max(1, hours), 48)
            return {
                "type": "hourly",
                "hours": hours,
                "recommended_tool": "get_hourly_weather_forecast",
                "description": f"未来{hours}小时天气"
            }
        except:
            return {"error": f"无法解析小时数: {date_description}"}

    elif "天" in date_description and not date_description.startswith("星期"):
        # 天数查询
        try:
            days = int(''.join(filter(str.isdigit, date_description)))
            if days <= 5:  # 在预报范围内
                return {
                    "type": "days_forecast",
                    "days": days,
                    "recommended_tool": "get_weather_forecast",
                    "description": f"未来{days}天天气"
                }
            else:  # 超出预报范围
                target_date = (today + timedelta(days=days)).strftime("%Y-%m-%d")
                return {
                    "type": "prediction",
                    "days": days,
                    "target_date": target_date,
                    "recommended_tool": "predict_weather_trend",
                    "description": f"基于趋势预测{days}天后天气"
                }
        except:
            return {"error": f"无法解析天数: {date_description}"}

    elif date_description in ["明天", "后天", "大后天"]:
        # 特定日期查询
        day_desc_map = {"明天": 1, "后天": 2, "大后天": 3}
        days = day_desc_map.get(date_description, 1)
        return {
            "type": "specific_day",
            "days": days,
            "description": date_description,
            "recommended_tool": "get_specific_day_weather"
        }

    elif "202" in date_description and "-" in date_description:
        # 可能是一个具体的日期
        try:
            target_dt = datetime.strptime(date_description, "%Y-%m-%d")
            days_diff = (target_dt - today).days

            if days_diff <= 0:
                return {"error": f"日期 '{date_description}' 是过去日期"}
            elif days_diff <= 5:
                return {
                    "type": "specific_date_forecast",
                    "target_date": date_description,
                    "days_ahead": days_diff,
                    "recommended_tool": "get_weather_forecast"
                }
            else:
                return {
                    "type": "prediction",
                    "target_date": date_description,
                    "days_ahead": days_diff,
                    "recommended_tool": "predict_weather_trend",
                    "description": f"基于趋势预测{date_description}的天气"
                }
        except ValueError:
            pass

    return {"error": f"无法理解的日期描述: {date_description}"}

@tool
def predict_weather_trend(city: str, target_date: str) -> Dict[str, Any]:
    """根据历史天气数据预测指定日期的天气趋势，包括天气类型概率预测

    Args:
        city: 城市名称
        target_date: 目标日期 (格式: YYYY-MM-DD)

    Returns:
        包含预测结果、天气概率和置信度的字典
    """
    from datetime import datetime, timedelta

    try:
        # 解析目标日期
        target_dt = datetime.strptime(target_date, "%Y-%m-%d")
        today = datetime.now()

        # 计算天数差
        days_diff = (target_dt - today).days

        if days_diff <= 0:
            return {"error": f"目标日期 '{target_date}' 是过去或今天的日期，无法预测"}

        # 获取可用的天气预报数据（最多5天）
        forecast_data = get_weather_forecast.invoke({"city": city, "days": min(days_diff, 5)})
        if "error" in forecast_data:
            return forecast_data

        # 获取历史天气数据（最近几天）
        current_weather = get_current_weather.invoke({"city": city})
        if "error" in current_weather:
            return current_weather

        # 分析天气趋势
        trend_analysis = analyze_weather_trend(forecast_data, current_weather, days_diff)

        # 计算预测置信度
        confidence_level = calculate_confidence_level(days_diff, len(forecast_data.get("forecast", [])))

        return {
            "city": city,
            "target_date": target_date,
            "days_ahead": days_diff,
            "prediction": trend_analysis,
            "confidence": confidence_level,
            "data_source": "基于最近天气趋势、季节模式和概率分析",
            "limitation": "预测和概率仅供参考，实际天气可能有所不同"
        }

    except ValueError:
        return {"error": f"无效的日期格式: {target_date}，请使用 YYYY-MM-DD 格式"}
    except Exception as e:
        return {"error": f"预测过程中出错: {str(e)}"}

def calculate_confidence_level(days_ahead: int, data_points: int) -> str:
    """根据天数和数据点计算预测置信度"""
    if data_points <= 2:
        base_confidence = 0.3
    elif data_points <= 5:
        base_confidence = 0.6
    else:
        base_confidence = 0.8

    # 根据天数调整置信度
    if days_ahead <= 3:
        day_factor = 0.9
    elif days_ahead <= 7:
        day_factor = 0.7
    elif days_ahead <= 15:
        day_factor = 0.5
    else:
        day_factor = 0.3

    final_confidence = base_confidence * day_factor

    if final_confidence >= 0.7:
        return "高"
    elif final_confidence >= 0.5:
        return "中等"
    else:
        return "低"

def analyze_weather_trend(forecast_data: Dict[str, Any], current_weather: Dict[str, Any], days_ahead: int) -> Dict[str, Any]:
    """分析天气趋势并生成预测，包括天气类型概率和具体天气描述"""
    # 提取温度趋势和天气数据
    temperatures = []
    weather_descriptions = []
    humidities = []
    wind_speeds = []

    if "forecast" in forecast_data:
        for item in forecast_data["forecast"]:
            temperatures.append(item["temperature"])
            weather_descriptions.append(item["description"])
            humidities.append(item["humidity"])
            wind_speeds.append(item["wind_speed"])

    # 添加当前天气数据
    if "temperature" in current_weather:
        temperatures.insert(0, current_weather["temperature"])
    if "description" in current_weather:
        weather_descriptions.insert(0, current_weather["description"])
    if "humidity" in current_weather:
        humidities.insert(0, current_weather["humidity"])
    if "wind_speed" in current_weather:
        wind_speeds.insert(0, current_weather["wind_speed"])

    # 温度趋势预测
    predicted_temp = predict_temperature(temperatures, days_ahead)

    # 湿度预测
    predicted_humidity = predict_humidity(humidities, days_ahead)

    # 风速预测
    predicted_wind_speed = predict_wind_speed(wind_speeds, days_ahead)

    # 天气类型概率预测
    weather_probabilities = predict_weather_probabilities(weather_descriptions, days_ahead)

    # 预测具体天气状况
    predicted_weather = predict_detailed_weather(weather_descriptions, predicted_temp, predicted_humidity, wind_speeds, days_ahead)

    # 为每种天气类型预测独立的温度和条件
    weather_type_predictions = predict_conditions_for_weather_types(
        weather_descriptions, temperatures, humidities, wind_speeds, days_ahead, weather_probabilities
    )

    # 基于季节和位置的预测
    month = datetime.now().month
    season = get_season(month)

    return {
        "predicted_temperature": predicted_temp,
        "predicted_humidity": predicted_humidity,
        "predicted_wind_speed": predicted_wind_speed,
        "predicted_weather_description": predicted_weather,
        "temperature_trend": "稳定" if len(set(temperatures)) <= 2 else "变化",
        "season": season,
        "typical_weather": get_typical_weather(season, city=forecast_data.get("city", "")),
        "weather_probabilities": weather_probabilities,
        "weather_type_predictions": weather_type_predictions,  # 新增：每种天气类型的预测
        "recommendation": get_seasonal_recommendation(season, predicted_temp)
    }

def predict_humidity(humidities: List[float], days_ahead: int) -> float:
    """预测未来的湿度"""
    if len(humidities) == 0:
        return None

    # 使用最近的湿度值，考虑季节性变化
    if len(humidities) >= 2:
        avg_humidity = sum(humidities) / len(humidities)
    else:
        avg_humidity = humidities[-1]

    # 根据季节微调
    month = datetime.now().month
    season = get_season(month)

    # 不同季节的湿度调整
    season_adjustment = {
        "夏季": 0.95,  # 夏季湿度可能略高
        "冬季": 1.05,  # 冬季湿度可能略低
        "春季": 1.0,
        "秋季": 1.0
    }

    return round(avg_humidity * season_adjustment.get(season, 1.0), 1)

def predict_wind_speed(wind_speeds: List[float], days_ahead: int) -> float:
    """预测未来的风速"""
    if len(wind_speeds) == 0:
        return None

    # 使用平均风速
    if len(wind_speeds) >= 3:
        recent_winds = wind_speeds[-3:]  # 取最近3个风速
        avg_wind = sum(recent_winds) / len(recent_winds)
    else:
        avg_wind = sum(wind_speeds) / len(wind_speeds)

    return round(avg_wind, 1)

def predict_detailed_weather(weather_descriptions: List[str], temperature: float, humidity: float, wind_speeds: List[float], days_ahead: int) -> str:
    """生成详细的天气状况描述"""
    if not weather_descriptions:
        return "无法获取详细的天气状况"

    # 分析最常见天气类型
    from collections import Counter
    category_counts = Counter(categorize_weather(weather_descriptions))

    if category_counts:
        most_common = category_counts.most_common(1)[0][0]
    else:
        most_common = "多云"  # 默认值

    # 根据天气类型生成描述
    weather_descriptions_map = {
        "晴天": generate_sunny_description(temperature, humidity, wind_speeds),
        "多云": generate_cloudy_description(temperature, humidity, wind_speeds),
        "雨天": generate_rainy_description(temperature, humidity, wind_speeds),
        "雪天": generate_snowy_description(temperature, humidity, wind_speeds),
        "雷雨": generate_thunderstorm_description(temperature, humidity, wind_speeds),
        "雾天": generate_foggy_description(temperature, humidity, wind_speeds)
    }

    return weather_descriptions_map.get(most_common, generate_general_description(temperature, humidity, wind_speeds))

def generate_sunny_description(temperature: float, humidity: float, wind_speeds: List[float]) -> str:
    """生成晴天描述"""
    avg_wind = sum(wind_speeds) / len(wind_speeds) if wind_speeds else 0

    if temperature >= 30:
        return "晴朗炎热，适合防晒和室内活动"
    elif temperature >= 25:
        return f"晴朗温暖，微风{avg_wind}米/秒，适合户外活动"
    else:
        return f"晴朗凉爽，风力{avg_wind}米/秒，适宜外出"

def generate_cloudy_description(temperature: float, humidity: float, wind_speeds: List[float]) -> str:
    """生成多云描述"""
    avg_wind = sum(wind_speeds) / len(wind_speeds) if wind_speeds else 0

    if humidity > 80:
        return f"多云闷热，湿度较高，有短时小雨可能"
    elif temperature >= 25:
        return f"多云天气，温度适中，风力{avg_wind}米/秒"
    else:
        return f"多云凉爽，适宜各种活动"

def generate_rainy_description(temperature: float, humidity: float, wind_speeds: List[float]) -> str:
    """生成雨天描述"""
    avg_wind = sum(wind_speeds) / len(wind_speeds) if wind_speeds else 0

    if temperature > 25:
        return f"阵雨或雷阵雨，温度较高，建议携带雨具，风力{avg_wind}米/秒"
    else:
        return f"降雨天气，温度适中，建议穿戴防水衣物，风力{avg_wind}米/秒"

def generate_snowy_description(temperature: float, humidity: float, wind_speeds: List[float]) -> str:
    """生成雪天描述"""
    avg_wind = sum(wind_speeds) / len(wind_speeds) if wind_speeds else 0

    if temperature <= -5:
        return f"降雪天气，寒冷，道路可能结冰，风力{avg_wind}米/秒"
    else:
        return f"降雪或雨夹雪，温度较低，注意防滑，风力{avg_wind}米/秒"

def generate_thunderstorm_description(temperature: float, humidity: float, wind_speeds: List[float]) -> str:
    """生成雷雨描述"""
    avg_wind = sum(wind_speeds) / len(wind_speeds) if wind_speeds else 0

    if avg_wind > 8:
        return f"雷雨伴有大风，建议避免外出，注意安全"
    else:
        return f"雷阵雨天气，可能有短时强降水"

def generate_foggy_description(temperature: float, humidity: float, wind_speeds: List[float]) -> str:
    """生成雾天描述"""
    return "有雾或轻雾，能见度较低，出行注意安全"

def generate_general_description(temperature: float, humidity: float, wind_speeds: List[float]) -> str:
    """生成一般描述"""
    avg_wind = sum(wind_speeds) / len(wind_speeds) if wind_speeds else 0

    if temperature >= 30:
        return f"天气炎热，湿度{humidity}%，建议适当降温"
    elif temperature <= 10:
        return f"天气较冷，风力{avg_wind}米/秒，注意保暖"
    else:
        return f"天气舒适，适合各种户外活动"

def predict_conditions_for_weather_types(weather_descriptions: List[str], temperatures: List[float],
                                       humidities: List[float], wind_speeds: List[float],
                                       days_ahead: int, weather_probabilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """为每种可能的天气类型预测独立的温度和条件"""
    if not weather_probabilities:
        return []

    weather_type_predictions = []
    month = datetime.now().month
    season = get_season(month)

    for prob_data in weather_probabilities:
        weather_type = prob_data["weather"]
        probability = prob_data["probability"] / 100.0  # 转换为小数

        # 根据天气类型调整温度预测
        predicted_temp = adjust_temperature_for_weather_type(
            predict_temperature(temperatures, days_ahead), weather_type, season, probability
        )

        # 预测湿度和风速
        predicted_humidity = adjust_humidity_for_weather_type(
            predict_humidity(humidities, days_ahead), weather_type, season
        )

        predicted_wind_speed = adjust_wind_speed_for_weather_type(
            predict_wind_speed(wind_speeds, days_ahead), weather_type, season
        )

        # 生成特定天气类型的描述
        weather_description = generate_weather_specific_description(
            weather_type, predicted_temp, predicted_humidity, predicted_wind_speed
        )

        # 生成建议
        suggestion = generate_weather_specific_suggestion(
            weather_type, predicted_temp, predicted_humidity, predicted_wind_speed
        )

        weather_type_predictions.append({
            "weather_type": weather_type,
            "probability": prob_data["probability"],
            "icon": prob_data["icon"],
            "predicted_temperature": predicted_temp,
            "predicted_humidity": predicted_humidity,
            "predicted_wind_speed": predicted_wind_speed,
            "weather_description": weather_description,
            "suggestion": suggestion,
            "typical_conditions": get_typical_conditions_by_weather_type(weather_type, season)
        })

    return weather_type_predictions

def adjust_temperature_for_weather_type(base_temp: float, weather_type: str, season: str, probability: float) -> float:
    """根据天气类型调整温度预测"""
    if base_temp is None:
        return None

    # 不同天气类型对温度的影响
    weather_adjustments = {
        "晴天": 1.0,  # 晴天通常温度稍高
        "多云": -0.5,  # 多云可能温度略低
        "雨天": -1.5,  # 雨天温度会降低
        "雪天": -3.0,  # 雪天温度显著降低
        "雷雨": -1.0,  # 雷雨伴随降温
        "雾天": -0.5,  # 雾天温度稍低
        "其他": 0.0
    }

    adjustment = weather_adjustments.get(weather_type, 0.0)
    # 考虑概率权重，高概率的天气类型调整幅度更大
    adjustment *= (0.5 + probability * 0.5)  # 在0.5-1.0之间调整

    return round(base_temp + adjustment, 1)

def adjust_humidity_for_weather_type(base_humidity: float, weather_type: str, season: str) -> float:
    """根据天气类型调整湿度预测"""
    if base_humidity is None:
        return None

    # 不同天气类型的湿度特征
    humidity_multipliers = {
        "雨天": 1.2,   # 雨天湿度高
        "雷雨": 1.3,   # 雷雨湿度更高
        "雾天": 1.4,   # 雾天湿度很高
        "多云": 1.1,   # 多云可能湿度稍高
        "雪天": 0.9,   # 雪天湿度可能较低
        "晴天": 0.8,   # 晴天湿度通常较低
        "其他": 1.0
    }

    multiplier = humidity_multipliers.get(weather_type, 1.0)
    return round(base_humidity * multiplier, 1)

def adjust_wind_speed_for_weather_type(base_wind_speed: float, weather_type: str, season: str) -> float:
    """根据天气类型调整风速预测"""
    if base_wind_speed is None:
        return None

    # 不同天气类型的风速特征
    wind_speed_multipliers = {
        "雷雨": 1.5,   # 雷雨风速较大
        "雨天": 1.2,   # 雨天可能有风
        "雪天": 0.8,   # 雪天风速可能较小
        "雾天": 0.5,   # 雾天风速小
        "晴天": 1.0,   # 晴天气候适宜
        "多云": 1.1,   # 多云常见有风
        "其他": 1.0
    }

    multiplier = wind_speed_multipliers.get(weather_type, 1.0)
    return round(base_wind_speed * multiplier, 1)

def generate_weather_specific_description(weather_type: str, temperature: float, humidity: float, wind_speed: float) -> str:
    """生成特定天气类型的详细描述"""
    descriptions = {
        "晴天": f"晴朗天气，温度{temperature}度，风力{wind_speed}米/秒，湿度{humidity}%",
        "多云": f"多云天气，温度{temperature}度，风力{wind_speed}米/秒，湿度{humidity}%",
        "雨天": f"降雨天气，温度{temperature}度，风力{wind_speed}米/秒，湿度{humidity}%较高",
        "雪天": f"降雪天气，温度{temperature}度较低，风力{wind_speed}米/秒，湿度{humidity}%",
        "雷雨": f"雷阵雨天气，温度{temperature}度，风力{wind_speed}米/秒可能较强",
        "雾天": f"有雾天气，温度{temperature}度，风力{wind_speed}米/秒较小，能见度低",
        "其他": f"特殊天气，温度{temperature}度，风力{wind_speed}米/秒，湿度{humidity}%"
    }

    return descriptions.get(weather_type, f"{weather_type}天气，温度{temperature}度，风力{wind_speed}米/秒，湿度{humidity}%")

def generate_weather_specific_suggestion(weather_type: str, temperature: float, humidity: float, wind_speed: float) -> str:
    """生成特定天气类型的建议"""
    suggestions = {
        "晴天": "晴天适合户外活动，注意防晒和补水",
        "多云": "多云天气适宜出行，可适当安排户外活动",
        "雨天": "建议携带雨具，注意地面湿滑",
        "雪天": "注意保暖和防滑，避免户外活动",
        "雷雨": "雷雨天气避免外出，注意安全",
        "雾天": "雾天出行注意安全，避免高速驾驶",
        "其他": "根据天气情况合理安排活动"
    }

    return suggestions.get(weather_type, "请根据具体天气情况安排活动")

def get_typical_conditions_by_weather_type(weather_type: str, season: str) -> str:
    """根据天气类型和季节获取典型条件"""
    typical_conditions = {
        "晴天": {
            "夏季": "炎热干燥，阳光强烈",
            "冬季": "寒冷但晴朗，紫外线较强",
            "春季": "温暖舒适，适宜户外",
            "秋季": "凉爽宜人，空气清新"
        },
        "多云": {
            "夏季": "相对凉爽，避免酷暑",
            "冬季": "阻挡冷风，体感较暖",
            "春季": "温度适中，变化较多",
            "秋季": "天高云淡，气候宜人"
        },
        "雨天": {
            "夏季": "阵雨或暴雨，湿度大",
            "冬季": "寒冷潮湿，需防寒",
            "春季": "春雨绵绵，助长作物",
            "秋季": "秋雨带凉，注意保湿"
        },
        "雪天": {
            "夏季": "罕见，高山地区可能",
            "冬季": "常见，需注意防寒除雪",
            "春季": "春雪短暂，道路湿滑",
            "秋季": "罕见，寒流来临前"
        }
    }

    if weather_type in typical_conditions:
        return typical_conditions[weather_type].get(season, "该季节典型的天气条件")
    return "典型天气条件"

def predict_temperature(temperatures: List[float], days_ahead: int) -> float:
    """预测未来的温度"""
    if len(temperatures) == 0:
        return None

    # 简单线性趋势预测
    if len(temperatures) >= 2:
        temp_changes = []
        for i in range(1, len(temperatures)):
            temp_changes.append(temperatures[i] - temperatures[i-1])

        avg_change = sum(temp_changes) / len(temp_changes) if temp_changes else 0
        predicted_temp = temperatures[-1] + avg_change * (days_ahead - len(temperatures) + 1)
    else:
        predicted_temp = temperatures[-1]

    return round(predicted_temp, 1) if predicted_temp else None

def predict_weather_probabilities(weather_descriptions: List[str], days_ahead: int) -> List[Dict[str, Any]]:
    """预测未来天气类型的概率，按概率从高到低排序"""
    if len(weather_descriptions) == 0:
        return []

    # 天气类型分类映射
    weather_categories = categorize_weather(weather_descriptions)

    # 计算各个类型的频率（基础概率）
    category_counts = {}
    for category in weather_categories:
        category_counts[category] = category_counts.get(category, 0) + 1

    # 计算基础概率
    total = len(weather_categories)
    base_probabilities = {category: count/total for category, count in category_counts.items()}

    # 考虑季节因素调整概率
    month = datetime.now().month
    season = get_season(month)
    adjusted_probabilities = adjust_probabilities_by_season(base_probabilities, season)

    # 考虑天数差影响（越远不确定性越大）
    final_probabilities = adjust_probabilities_by_days(adjusted_probabilities, days_ahead)

    # 转换为有序列表，按概率从高到低排序
    sorted_probabilities = [
        {"weather": category, "probability": round(prob * 100, 1), "icon": get_weather_icon("description", category)}
        for category, prob in sorted(final_probabilities.items(), key=lambda x: x[1], reverse=True)
    ]

    return sorted_probabilities

def categorize_weather(descriptions: List[str]) -> List[str]:
    """将天气描述分类为主要的天气类型"""
    categories = []
    for desc in descriptions:
        if any(word in desc for word in ["晴", "clear", "sunny"]):
            categories.append("晴天")
        elif any(word in desc for word in ["多云", "cloud", "阴"]):
            categories.append("多云")
        elif any(word in desc for word in ["雨", "rain", "降水"]):
            categories.append("雨天")
        elif any(word in desc for word in ["雪", "snow"]):
            categories.append("雪天")
        elif any(word in desc for word in ["雷", "thunder"]):
            categories.append("雷雨")
        elif any(word in desc for word in ["雾", "fog"]):
            categories.append("雾天")
        else:
            categories.append("其他")
    return categories

def adjust_probabilities_by_season(probabilities: Dict[str, float], season: str) -> Dict[str, float]:
    """根据季节调整天气概率"""
    # 季节权重（基于经验）
    season_weights = {
        "夏季": {"晴天": 1.2, "多云": 0.8, "雨天": 1.5, "雷雨": 1.3, "雪天": 0.1, "雾天": 0.5},
        "冬季": {"晴天": 0.8, "多云": 1.0, "雨天": 0.3, "雷雨": 0.1, "雪天": 1.8, "雾天": 1.2},
        "春季": {"晴天": 1.0, "多云": 1.2, "雨天": 1.1, "雷雨": 0.8, "雪天": 0.4, "雾天": 0.9},
        "秋季": {"晴天": 1.1, "多云": 1.0, "雨天": 0.9, "雷雨": 0.5, "雪天": 0.2, "雾天": 1.0}
    }

    weights = season_weights.get(season, {})
    adjusted = {}

    for weather, prob in probabilities.items():
        weight = weights.get(weather, 1.0)
        adjusted[weather] = prob * weight

    # 重新标准化概率
    total = sum(adjusted.values())
    if total > 0:
        adjusted = {k: v/total for k, v in adjusted.items()}

    return adjusted

def adjust_probabilities_by_days(probabilities: Dict[str, float], days_ahead: int) -> Dict[str, float]:
    """根据天数调整不确定性"""
    if days_ahead <= 3:
        return probabilities  # 短期预测，不确定性较小

    # 随着天数增加，天气类型预测的不确定性增加
    uncertainty_factor = min(1.0 + (days_ahead - 3) * 0.1, 2.0)

    adjusted = {}
    for weather, prob in probabilities.items():
        # 对不太可能发生的天气类型增加更多的不确定性
        if prob < 0.2:
            adjusted[weather] = prob * uncertainty_factor * 1.5
        else:
            adjusted[weather] = prob * uncertainty_factor

    # 重新标准化
    total = sum(adjusted.values())
    if total > 0:
        adjusted = {k: v/total for k, v in adjusted.items()}

    return adjusted

def get_season(month: int) -> str:
    """根据月份获取季节"""
    if month in [12, 1, 2]:
        return "冬季"
    elif month in [3, 4, 5]:
        return "春季"
    elif month in [6, 7, 8]:
        return "夏季"
    else:
        return "秋季"

def get_typical_weather(season: str, city: str = "") -> str:
    """获取典型天气状况"""
    typical_weather = {
        "冬季": "晴朗或阴天，可能有降雪",
        "春季": "多变，可能有降雨",
        "夏季": "炎热，可能有雷阵雨",
        "秋季": "凉爽，天气稳定"
    }
    return typical_weather.get(season, "天气多变")

def get_seasonal_recommendation(season: str, temperature: float = None) -> str:
    """获取季节性建议"""
    if temperature is None:
        return "建议关注最新天气预报"

    if season == "冬季":
        if temperature < 0:
            return "天气寒冷，注意保暖，可能有结冰"
        else:
            return "天气较冷，建议穿着保暖衣物"
    elif season == "夏季":
        if temperature > 30:
            return "天气炎热，注意防暑降温"
        else:
            return "天气温暖，适合户外活动"
    else:
        return "天气宜人，适合各种活动"

def get_weather_tools():
    """返回天气工具列表"""
    return [get_current_weather, get_weather_forecast, check_holiday_date_range, get_holiday_weather, get_specific_day_weather, get_hourly_weather_forecast, predict_weather_trend, parse_and_predict_weather]