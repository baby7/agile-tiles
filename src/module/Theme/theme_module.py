from src.module.UserData.DataBase import user_data_common


def init_theme(main_window):
    """
    初始化主题
    :param main_window: 主窗口
    """
    # 先加载初始值
    load_data(main_window)


def load_data(main_window):
    """
    加载初始值
    :param main_window: 主窗口
    """
    if (main_window.main_data is None or main_window.main_data["data"] is None
            or main_window.main_data["data"]["SettingCard"] is None):
        return
    if main_window.hardware_id not in main_window.main_data["data"]["SettingCard"]:
        main_window.main_data["data"]["SettingCard"][main_window.hardware_id] = user_data_common.setting_config
    setting_data = main_window.main_data["data"]["SettingCard"][main_window.hardware_id]
    # 主题色
    main_window.form_theme = setting_data["theme"]
    if main_window.form_theme == 'Light':
        main_window.is_dark = False
    else:
        main_window.is_dark = True
    # 图标颜色
    if 'themeIcon' not in setting_data:
        setting_data["themeIcon"] = "Black"
    main_window.form_theme_icon = setting_data["themeIcon"]
    # 主题模式
    main_window.form_theme_mode = setting_data["themeMode"]
    # 透明度
    main_window.form_theme_transparency = setting_data["themeTransparency"]

def change_theme_data(main_window):
    if (main_window.main_data is None or main_window.main_data["data"] is None
            or main_window.main_data["data"]["SettingCard"] is None):
        return
    if main_window.hardware_id not in main_window.main_data["data"]["SettingCard"]:
        main_window.main_data["data"]["SettingCard"][main_window.hardware_id] = user_data_common.setting_config
    if main_window.is_dark:
        main_window.form_them = "Light"
        main_window.is_dark = False
    else:
        main_window.form_them = "Dark"
        main_window.is_dark = True
    setting_data = main_window.main_data["data"]["SettingCard"][main_window.hardware_id]
    setting_data["theme"] = main_window.form_them
