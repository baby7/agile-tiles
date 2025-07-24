# coding:utf-8
# 基础包
import json
from functools import partial

from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QFileDialog

from src.constant import data_save_constant
# 初始化日志
import src.ui.style_util as style_util
import src.module.Box.message_box_util as message_box_util
from src.module.UserData.HistoryRecover.user_data_history_recover import UserServerRecoverWindow


def init_module(main_object):
    """
    初始化用户模块
    :param main_object:
    :return:
    """
    # 初始化样式
    init_style(main_object)
    # 初始化点击事件
    # if main_object.is_first:
    init_click_connect(main_object)
    # 刷新界面
    update_user_view(main_object)


def init_style(main_object):
    """
    初始化样式
    :param main_object:
    :return:
    """
    # 位置和显隐
    main_object.tab_widget_user.show()
    main_object.tab_widget_user.raise_()
    main_object.tab_widget_user.move(0, 0)
    # 主题
    refresh_theme(main_object)


def init_click_connect(main_object):
    """
    初始化点击事件
    :param main_object:
    :return:
    """
    main_object.push_button_area_user_message_logout.clicked.connect(main_object.logout)
    main_object.push_button_area_user_vip_subscription.clicked.connect(partial(push_button_area_user_vip_subscription_click, main_object))
    main_object.push_button_area_user_data_export.clicked.connect(partial(push_button_export_data_to_windows_click, main_object))
    main_object.push_button_area_user_data_import.clicked.connect(partial(push_button_import_data_from_windows_click, main_object))
    main_object.push_button_area_user_data_synchronization.clicked.connect(partial(push_button_area_user_data_synchronization_click, main_object))
    main_object.push_button_area_user_data_recover.clicked.connect(partial(push_button_area_user_data_recover_click, main_object))
    main_object.push_button_area_user_data_backup.clicked.connect(partial(push_button_area_user_data_backup_click, main_object))
    main_object.push_button_area_user_join_group.clicked.connect(partial(push_button_area_user_join_group_click, main_object))
    main_object.push_button_area_user_invite_code.clicked.connect(partial(push_button_area_user_invite_code_click, main_object))
    # vip权益提示
    main_object.push_button_area_user_vip_power_1.clicked.connect(partial(push_button_area_user_vip_power_1_click, main_object))
    main_object.push_button_area_user_vip_power_2.clicked.connect(partial(push_button_area_user_vip_power_2_click, main_object))
    main_object.push_button_area_user_vip_power_3.clicked.connect(partial(push_button_area_user_vip_power_3_click, main_object))
    main_object.push_button_area_user_vip_power_4.clicked.connect(partial(push_button_area_user_vip_power_4_click, main_object))
    main_object.push_button_area_user_vip_power_5.clicked.connect(partial(push_button_area_user_vip_power_5_click, main_object))
    main_object.push_button_area_user_vip_power_6.clicked.connect(partial(push_button_area_user_vip_power_6_click, main_object))


def push_button_area_user_vip_power_1_click(main_object):
    try:
        content = "用户可将数据备份至服务器，实现数据备份与恢复。\n功能在菜单->用户->数据页面处哦~"
        main_object.toolkit.text_box_util.show_text_dialog(main_object, "会员权益-云端数据备份", {"content": content, "size": [300, 200]})
    except Exception as e:
        main_object.info_logger.card_error("主程序", "查看会员权益失败,错误信息:{}".format(e))
        message_box_util.box_information(main_object, "错误信息", "查看会员权益失败")

def push_button_area_user_vip_power_2_click(main_object):
    try:
        content = "用户可在多台设备上使用，且数据可在多台设备上同步。\n功能在菜单->用户->数据页面处哦~"
        main_object.toolkit.text_box_util.show_text_dialog(main_object, "会员权益-数据多端同步", {"content": content, "size": [300, 200]})
    except Exception as e:
        main_object.info_logger.card_error("主程序", "查看会员权益失败,错误信息:{}".format(e))
        message_box_util.box_information(main_object, "错误信息", "查看会员权益失败")

def push_button_area_user_vip_power_3_click(main_object):
    try:
        content = "非会员用户可以每天使用三次AI大模型对话，会员用户可以无限制使用。未来会开放更多智能体。\n用户可以在菜单->智能对话处进行对话哦~"
        main_object.toolkit.text_box_util.show_text_dialog(main_object, "会员权益-AI大模型对话", {"content": content, "size": [300, 200]})
    except Exception as e:
        main_object.info_logger.card_error("主程序", "查看会员权益失败,错误信息:{}".format(e))
        message_box_util.box_information(main_object, "错误信息", "查看会员权益失败")

def push_button_area_user_vip_power_4_click(main_object):
    try:
        content = "会员用户可在有问题或意见时，使用设置->会员工单处进行工单提交。我们会在第一时间处理工单。\n会员可以在菜单->设置->会员工单处提交工单哦~"
        main_object.toolkit.text_box_util.show_text_dialog(main_object, "会员权益-专属工单系统", {"content": content, "size": [300, 200]})
    except Exception as e:
        main_object.info_logger.card_error("主程序", "查看会员权益失败,错误信息:{}".format(e))
        message_box_util.box_information(main_object, "错误信息", "查看会员权益失败")

def push_button_area_user_vip_power_5_click(main_object):
    try:
        content = "用户可在多处中看到专属会员头像哦~"
        main_object.toolkit.text_box_util.show_text_dialog(main_object, "会员权益-会员尊享标识", {"content": content, "size": [300, 200]})
    except Exception as e:
        main_object.info_logger.card_error("主程序", "查看会员权益失败,错误信息:{}".format(e))
        message_box_util.box_information(main_object, "错误信息", "查看会员权益失败")

def push_button_area_user_vip_power_6_click(main_object):
    try:
        content = "用户可以自定义主题，未来将会添加更多自定义主题和功能。\n用户可在菜单->设置->主题设置中自定义主题哦~"
        main_object.toolkit.text_box_util.show_text_dialog(main_object, "会员权益-自定义主题", {"content": content, "size": [300, 200]})
    except Exception as e:
        main_object.info_logger.card_error("主程序", "查看会员权益失败,错误信息:{}".format(e))
        message_box_util.box_information(main_object, "错误信息", "查看会员权益失败")


def push_button_area_user_vip_subscription_click(main_object):
    """
    续费或开通会员
    """
    try:
        if not main_object.is_login:
            message_box_util.box_information(main_object, "提示信息", "请先登录")
            return
        main_object.toolkit.qr_code_box_util.show_qr_code_dialog(main_object, "支付宝支付")
    except Exception as e:
        main_object.info_logger.card_error("主程序", "续费或开通会员失败,错误信息:{}".format(e))
        message_box_util.box_information(main_object, "错误信息", "续费或开通会员失败")


def push_button_area_user_invite_code_click(main_object):
    """
    复制邀请码
    """
    try:
        if not main_object.is_login:
            message_box_util.box_information(main_object, "提示信息", "请先登录")
            return
        invite_code = main_object.current_user["inviteCode"]
        main_object.toolkit.text_box_util.show_text_dialog(
            main_object, "邀请码",
            {"content": f"欢迎您体验使用灵卡面板，官网: http://www.baby7blog.com:8787/index.html，下载后，在注册时填写邀请码 {invite_code} 即可获得七天会员权益哦~", "size": [300, 200]}
        )
    except Exception as e:
        main_object.info_logger.card_error("主程序", "复制邀请码失败,错误信息:{}".format(e))
        message_box_util.box_information(main_object, "错误信息", "复制邀请码失败")


def push_button_export_data_to_windows_click(main_object):
    """
    导出main_data的数据到本地，json格式，弹出框选择保存位置
    """
    try:
        file_name = QFileDialog.getSaveFileName(main_object, "导出数据", "", "*.json")
        if file_name[0] == "":
            return
        with open(file_name[0], 'w', encoding='utf-8') as f:
            json.dump(main_object.main_data, f, ensure_ascii=False)
    except Exception as e:
        main_object.info_logger.card_error("主程序", "导出数据失败,错误信息:{}".format(e))
        message_box_util.box_information(main_object, "错误信息", "导出数据失败")


def push_button_import_data_from_windows_click(main_object):
    """
    从本地导入main_data的数据，弹出框选择json文件
    """
    try:
        file_name = QFileDialog.getOpenFileName(main_object, "导入数据", "", "*.json")
        if file_name[0] == "":
            return
        try:
            with open(file_name[0], 'r', encoding='utf-8') as f:
                import_data = json.load(f)
        except UnicodeDecodeError:
            message_box_util.box_information(main_object, "错误", "文件编码不是UTF-8，请使用UTF-8编码的文件导入")
            return
        if import_data is None:
            message_box_util.box_information(main_object, "提醒", "数据为空，导入失败！")
            return
        if 'timestamp' not in import_data or 'data' not in import_data or 'card' not in import_data or 'bigCard' not in import_data:
            message_box_util.box_information(main_object, "提醒", "数据格式不正确，导入失败！")
            return
        if not message_box_util.box_acknowledgement(main_object, "警告", "确定导入该数据吗，这将覆盖现有数据！"):
            return
        main_object.local_trigger_data_update(trigger_type=data_save_constant.TRIGGER_TYPE_DATA_IMPORT, in_data=import_data)
        message_box_util.box_information(main_object, "提示信息", "导入数据成功")
    except Exception as e:
        main_object.info_logger.card_error("主程序", "导入数据失败,错误信息:{}".format(e))

def push_button_area_user_data_synchronization_click(main_object):
    try:
        if main_object.current_user is None or main_object.current_user["username"] is None:
            message_box_util.box_information(main_object, "提醒", f"未知错误，请重新登录")
            return
        if not main_object.is_login:
            message_box_util.box_information(main_object, "提示信息", "请先登录")
            return
        if not main_object.is_vip:
            message_box_util.box_information(main_object, "提示信息", "会员专属功能，请开通会员后使用哦")
            return

        # 使用信号连接
        main_object.user_data_client_by_setting.pull_data(main_object.current_user["username"], main_object.token)
    except Exception as e:
        main_object.info_logger.card_error("主程序", "导入数据失败,错误信息:{}".format(e))

def push_button_area_user_data_recover_click(main_object):
    try:
        if main_object.current_user is None or main_object.current_user["username"] is None:
            message_box_util.box_information(main_object, "提醒", f"未知错误，请重新登录")
            return
        if not main_object.is_login:
            message_box_util.box_information(main_object, "提示信息", "请先登录")
            return
        if not main_object.is_vip:
            message_box_util.box_information(main_object, "提示信息", "会员专属功能，请开通会员后使用哦")
            return
        main_object.toolkit.resolution_util.out_animation(main_object)
        # 关闭并销毁旧窗口（新增部分）
        if hasattr(main_object, 'user_server_recover_win'):
            main_object.user_server_recover_win.close()
            main_object.user_server_recover_win.deleteLater()
            del main_object.user_server_recover_win
        main_object.user_server_recover_win = UserServerRecoverWindow(None, main_object)
        main_object.user_server_recover_win.refresh_geometry(main_object.toolkit.resolution_util.get_screen(main_object))
        main_object.user_server_recover_win.show()
    except Exception as e:
        main_object.info_logger.card_error("主程序", "恢复数据失败,错误信息:{}".format(e))

def push_button_area_user_data_backup_click(main_object):
    try:
        if main_object.current_user is None or main_object.current_user["username"] is None:
            message_box_util.box_information(main_object, "提醒", f"未知错误，请重新登录")
            return
        if not main_object.is_login:
            message_box_util.box_information(main_object, "提示信息", "请先登录")
            return
        if not main_object.is_vip:
            message_box_util.box_information(main_object, "提示信息", "会员专属功能，请开通会员后使用哦")
            return

        # 使用信号连接
        main_object.user_data_client_by_setting.push_data(main_object.current_user["username"], main_object.token, main_object.main_data)
    except Exception as e:
        main_object.info_logger.card_error("主程序", "数据备份失败,错误信息:{}".format(e))

def refresh_theme(main_object):
    is_dark = main_object.is_dark
    # 选项卡样式
    style_util.set_tab_widget_style(main_object.tab_widget_user, is_dark)
    # 注销按钮样式
    main_object.push_button_area_user_message_logout.setIcon(get_icon_park_path("Arrows/logout", is_dark))
    if is_dark:
        main_object.push_button_area_user_message_logout.setStyleSheet("""
            QPushButton {
                border: 1px solid white;
                border-radius: 20px;
                background: transparent;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.3);
            }"""
        )
    else:
        main_object.push_button_area_user_message_logout.setStyleSheet("""
            QPushButton {
                border: 1px solid black;
                border-radius: 20px;
                background: transparent;
            }
            QPushButton:hover {
                background: rgba(0, 0, 0, 0.3);
            }"""
        )
    # 其他按钮样式
    if is_dark:
        main_object.label_area_user_message_logout.setStyleSheet("background: white;color:black;border-radius: 8px; padding:2px;")
        main_object.line_area_user_message.setStyleSheet("color: #FFFFFF;border-color: #FFFFFF;background-color: #FFFFFF;")
        main_object.label_area_user_message_username.setStyleSheet("border: none;background-color: rgba(0, 0, 0, 0);color: rgba(255, 255, 255, 0.5);")
        main_object.label_user_last_backup_time.setStyleSheet("border: none;background-color: rgba(0, 0, 0, 0);color: rgba(255, 255, 255, 0.5);")
        main_object.label_user_last_backup_time_title.setStyleSheet("border: none;background-color: rgba(0, 0, 0, 0);color: rgba(255, 255, 255, 0.5);")
        main_object.widget_area_user_vip_power_content.setStyleSheet("background-color: black;")
        vip_linear_gradient_top = "background-color: qlineargradient(x1:0, y1:1, x2:0, y2:0,stop:0 rgb(34, 34, 34), stop:1 rgb(71, 153, 253));"
        vip_linear_gradient_bottom = "background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 rgb(34, 34, 34), stop:1 rgb(71, 153, 253));"
        invite_linear_gradient = "background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 rgb(34, 34, 34), stop:1 rgb(14, 204, 156));"
        user_data_style = "border-radius: 10px; border: 1px solid black; background-color:rgba(0, 0, 0, 200);"
        title_info_style = "border: 0px solid #FF8D16; border-radius: 0px; background-color: rgba(0, 0, 0, 0); color: rgb(255, 255, 255);"
    else:
        main_object.label_area_user_message_logout.setStyleSheet("background: black;color:white;border-radius: 8px; padding:2px;")
        main_object.line_area_user_message.setStyleSheet("color: #000;border-color: #000;background-color: #000;")
        main_object.label_area_user_message_username.setStyleSheet("border: none;background-color: rgba(0, 0, 0, 0);color: rgba(0, 0, 0, 0.5);")
        main_object.label_user_last_backup_time.setStyleSheet("border: none;background-color: rgba(0, 0, 0, 0);color: rgba(0, 0, 0, 0.5);")
        main_object.label_user_last_backup_time_title.setStyleSheet("border: none;background-color: rgba(0, 0, 0, 0);color: rgba(0, 0, 0, 0.5);")
        main_object.widget_area_user_vip_power_content.setStyleSheet("background-color: white;")
        vip_linear_gradient_top = "background-color: qlineargradient(x1:0, y1:1, x2:0, y2:0,stop:0 rgb(205, 232, 255), stop:1 rgb(71, 153, 253));"
        vip_linear_gradient_bottom = "background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 rgb(205, 232, 255), stop:1 rgb(71, 153, 253));"
        invite_linear_gradient = "background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 rgb(205, 232, 255), stop:1 rgb(14, 204, 156));"
        user_data_style = "border-radius: 10px; border: 1px solid white; background-color:rgba(255, 255, 255, 200);"
        title_info_style = "border: 0px solid #FF8D16; border-radius: 0px; background-color: rgba(0, 0, 0, 0); color: rgb(0, 0, 0);"
    main_object.widget_area_user_vip_power_bg.setStyleSheet(vip_linear_gradient_top)
    main_object.widget_area_user_invite_bg.setStyleSheet(invite_linear_gradient)
    main_object.label_user_login_invite_title.setStyleSheet(title_info_style)
    main_object.label_area_user_invite_info.setStyleSheet(title_info_style)
    # vip按钮图标
    push_button_area_user_vip_power_list = [
        [ main_object.push_button_area_user_vip_power_1, "Connect/link-cloud-sucess"],
        [ main_object.push_button_area_user_vip_power_2, "Arrows/transfer-data"],
        [ main_object.push_button_area_user_vip_power_3, "Abstract/smart-optimization"],
        [ main_object.push_button_area_user_vip_power_4, "Money/transaction"],
        [ main_object.push_button_area_user_vip_power_5, "Character/vip"],
        [ main_object.push_button_area_user_vip_power_6, "Clothes/theme"],
    ]
    # button_linear_gradient = "border: 0px solid white; border-radius: 20px;" + vip_linear_gradient
    for push_button_area_user_vip_power in push_button_area_user_vip_power_list:
        push_button_area_user_vip_power[0].setIcon(get_icon_park_path(push_button_area_user_vip_power[1], is_dark))
        push_button_area_user_vip_power[0].setStyleSheet("""
        QPushButton {
            border: 0px solid white;
            border-radius: 20px;
            {background-color}
        }
        QPushButton:hover {
            {background-color-hover}
        }""".replace("{background-color}", vip_linear_gradient_top)
         .replace("{background-color-hover}", vip_linear_gradient_bottom))
    # vip按钮图标2
    vip_one_icon = get_icon_park_path("Others/vip-one", is_dark, is_yellow=True)
    main_object.push_button_area_user_data_synchronization.setIcon(vip_one_icon)
    main_object.push_button_area_user_data_backup.setIcon(vip_one_icon)
    main_object.push_button_area_user_data_recover.setIcon(vip_one_icon)
    # 其他
    main_object.widget_area_user_data_sync.setStyleSheet(user_data_style)
    main_object.widget_area_user_data_server.setStyleSheet(user_data_style)
    main_object.widget_area_user_data_local.setStyleSheet(user_data_style)
    main_object.widget_area_user_communicate.setStyleSheet(user_data_style)
    # logo
    main_object.label_area_user_vip_icon.setPixmap(get_pixmap_park_path("Others/vip-one", is_dark, is_yellow=True))
    main_object.label_area_user_invite_icon.setPixmap(get_pixmap_park_path("Baby/holding-hands", is_dark))

def get_icon_park_path(icon_position, is_dark, is_yellow=False):
    icon_theme_folder = "light" if is_dark else "dark"
    if is_yellow:
        icon_theme_folder = "yellow"
    return QIcon("./static/img/IconPark/" + icon_theme_folder + "/" + icon_position + ".png")

def get_pixmap_park_path(icon_position, is_dark, is_yellow=False):
    icon_theme_folder = "light" if is_dark else "dark"
    if is_yellow:
        icon_theme_folder = "yellow"
    return QPixmap("./static/img/IconPark/" + icon_theme_folder + "/" + icon_position + ".png")


def update_user_view(main_object):
    # 判断是否登录
    if main_object.is_login:
        main_object.label_area_user_message_nick_name.setText(main_object.current_user['nickName'])
        main_object.label_area_user_message_username.setText(main_object.current_user["username"])
    # 判断会员
    if main_object.is_login and main_object.is_vip:
        main_object.push_button_area_user_vip_subscription.setText("续费会员")
        vip_expire_time = str(main_object.current_user['vipExpireTime'])
        vip_expire_data = vip_expire_time[0:10]
        main_object.label_area_user_vip_info.setText("有效期:" + vip_expire_data)
        main_object.label_user_avatar.setPixmap(QPixmap("./static/img/user/head_vip.png"))
    else:
        main_object.push_button_area_user_vip_subscription.setText("开通会员")
        main_object.label_area_user_vip_info.setText("开通会员享受服务")
        main_object.label_user_avatar.setPixmap(QPixmap("./static/img/user/head_normal.png"))


def push_button_area_user_join_group_click(main_object):
    main_object.toolkit.text_box_util.show_text_dialog(
        main_object, "加入QQ用户交流群",
        {"content": "956584263", "size": [300, 200]}
    )
