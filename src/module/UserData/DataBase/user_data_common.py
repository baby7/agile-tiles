import copy


setting_config = {
    "theme": "Light",                   # 主题颜色
    "themeMode": "Acrylic",             # 窗口主题
    "themeTransparency": 100,           # 窗口透明度

    "wakeUpByKeyboard": True,           # 是否启用快捷唤醒
    "wakeUpByKeyboardType": "Alt+1",    # 唤醒快捷键

    "screenName": None,                 # 屏幕名称
    "windowPosition": "Right",          # 窗口位置
    "formAnimationType": "Elastic",     # 窗口动画类型
    "formAnimationTime": 200,           # 窗口动画时间
    "wakeUpByMouse": True,              # 是否启用鼠标唤醒
    "wakeUpByMouseTime": 200,           # 鼠标唤醒时间
    "wakeUpByMouseHide": "OnlyMouse",   # 鼠标唤醒隐藏
    "menuPosition": "Right",            # 菜单位置
    "fontName": "微软雅黑",              # 字体名称

    "messageNotification": True,        # 消息通知
    "powerOn": True,                    # 开机自启动
    "autoUpdate": True,                 # 自动更新

    "width": 6,                         # 宽度
    "height": 13,                       # 高度
}
todo_config = {
    "typeList": [
        {
            "title": "工作"
        },
        {
            "title": "生活"
        },
        {
            "title": "今日计划"
        },
        {
            "title": "本周计划"
        },
        {
            "title": "本月计划"
        }
    ],
    "todoList": []
}
drinking_config = {
    "setting": {
        "drinkingCount": 8,
        "viewMessage": "positive"
    },
    "records": []
}

DEFAULT_DATA_MODEL = {
    "timestamp": 1716426823229,
    "card": [
        {
            "name": "FlipClockCard",
            "x": 1,
            "y": 1,
            "size": "2_1",
            "data": {}
        },
        {
            "name": "DrinkingCard",
            "x": 3,
            "y": 4,
            "size": "2_2",
            "data": {}
        },
        {
            "name": "WorkdayCard",
            "x": 5,
            "y": 4,
            "size": "2_2",
            "data": {}
        },
        {
            "size": "6_8",
            "data": {},
            "name": "MainCard",
            "x": 1,
            "y": 6
        },
        {
            "name": "WeatherCard",
            "data": {},
            "size": "4_2",
            "x": 3,
            "y": 2
        },
        {
            "name": "CalendarCard",
            "data": {},
            "size": "2_2",
            "x": 1,
            "y": 2
        },
        {
            "name": "SearchCard",
            "data": {},
            "size": "4_1",
            "x": 3,
            "y": 1
        },
        {
            "name": "WoodenFishCard",
            "data": {},
            "size": "2_2",
            "x": 1,
            "y": 4
        }
    ],
    "bigCard": [],
    "data": {}
}
big_card_name_list = ["GameCard", "BookCard", "ToolCard", "TodoCard", "ChatCard", "MusicCard", "SettingCard", "TopSearchCard", "InformationCard"]

def get_data(hardware_id):
    data = copy.deepcopy(DEFAULT_DATA_MODEL)
    # 大卡片数据补全
    if "bigCard" not in data:
        data["bigCard"] = []
    for big_card in big_card_name_list:
        # 判断该卡片是否已存在
        has_tag = False
        for big_card_data in data["bigCard"]:
            if big_card_data["name"] == big_card:
                has_tag = True
                break
        if has_tag:
            continue
        # 不存在就新增
        data["bigCard"].append({
            "name": big_card,
            "size": "Big",
            "data": {}
        })
    # hardware_id是为了区分不同设备
    complete_setting_config = {
        hardware_id: setting_config
    }
    # 默认数据补全
    if "data" not in data:
        data["data"] = {
            "SettingCard": complete_setting_config,
            "TodoCard": todo_config,
            "DrinkingCard": drinking_config
        }
    else:
        if "SettingCard" not in data["data"]:
            data["data"]["SettingCard"] = complete_setting_config
        if "TodoCard" not in data["data"]:
            data["data"]["TodoCard"] = todo_config
        if "DrinkingCard" not in data["data"]:
            data["data"]["DrinkingCard"] = drinking_config
    return data