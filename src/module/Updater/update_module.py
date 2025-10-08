import ctypes
import sys
import os
import subprocess
from PySide6.QtWidgets import QApplication, QLabel

from src.client import common
from src.constant import version_constant
from src.module.Updater.Updater import Updater
from src.module.Box import message_box_util

# 添加全局变量，存储更新信息
current_update_info = None

def check_update_on_start(main_object, tag=None):
    """启动时静默检查更新"""
    main_object.silent_updater = Updater(
        api_url=common.BASE_URL + "/version/public/check?type=Windows",
        app_version=main_object.app_version,
        update_dir=main_object.app_data_update_path
    )
    main_object.silent_updater.finished.connect(
        lambda success, update_info: handle_silent_update_result(main_object, success, update_info, tag)
    )
    # 直接调用检查更新方法，不再使用线程
    main_object.silent_updater.check_update()


def handle_silent_update_result(main_object, success, update_info, tag):
    """静默更新检查回调"""
    global current_update_info
    current_update_info = update_info

    if not success or update_info is None:
        message_box_util.box_information(
            main_object,
            "更新失败",
            "获取云端版本失败，请检查网络连接或稍后重试"
        )
        main_object.agree_update = False
        main_object.update_ready.emit()
        return

    # 如果强制更新
    if tag == "Start" and update_info.get("updateTag") is not None and update_info.get("updateTag"):
        # 强制更新
        if main_object.run_environment == "exe":
            show_force_update_dialog(main_object, update_info)
        elif main_object.run_environment == "msix":
            show_msix_force_update_dialog(main_object, update_info)
        else:
            main_object.agree_update = False
            main_object.update_ready.emit()
        return

    # 有更新
    if version_constant.compare_version(main_object.silent_updater.app_version, update_info["version"]) < 0:
        if tag == "Login":
            markdown_content = update_info["title"] + "\n" + update_info["message"]
            result = message_box_util.box_acknowledgement(main_object,
                                                          title="可以进行更新",
                                                          markdown_content=markdown_content,
                                                          button_ok_text="确定更新", button_no_text="以后再说")
            if result:
                main_object.agree_update = True
                start_update_process(main_object, update_info)
            else:
                main_object.agree_update = False
                main_object.update_ready.emit()
            return
        else:
            main_object.agree_update = True
            main_object.update_ready.emit()
            return

    # 无需更新
    main_object.agree_update = True
    main_object.update_ready.emit()
    print("无需更新")
    if tag == "Login":
        message_box_util.box_information(
            main_object,
            "更新信息",
            f"无需更新，您已是最新版本，版本: {main_object.silent_updater.app_version}"
        )
    return


def show_force_update_dialog(main_object, update_info):
    """强制更新弹窗"""
    markdown_content = update_info["title"] + "\n" + update_info["message"]
    result = message_box_util.box_acknowledgement(main_object,
                                                  title="必须升级到最新版本才能继续使用", markdown_content=markdown_content,
                                                  button_ok_text="确定更新", button_no_text="退出应用")
    if result:
        main_object.agree_update = True
        start_update_process(main_object, update_info)
    else:
        main_object.agree_update = False
        main_object.update_ready.emit()


def show_msix_force_update_dialog(main_object, update_info):
    """强制Msix更新弹窗"""
    markdown_content = update_info["title"] + "\n" + update_info["message"]
    result = message_box_util.box_acknowledgement(main_object,
                                                  title="必须升级到最新版本才能继续使用", markdown_content=markdown_content,
                                                  button_ok_text="确定更新", button_no_text="退出应用")
    if result:
        store_url = "ms-windows-store://downloadsandupdates"
        try:
            # 在Windows上
            subprocess.Popen(f'cmd /c start "" "{store_url}"', shell=True)
        except Exception as e:
            message_box_util.box_information(main_object, "错误", "无法打开微软商店，请手动打开微软商店对灵卡面板进行更新")
        main_object.agree_update = False
        main_object.update_ready.emit()
    else:
        main_object.agree_update = False
        main_object.update_ready.emit()


def handle_update_choice(main_object, button, update_info):
    """处理用户更新选择"""
    if button.text() == "&Yes":
        start_update_process(main_object, update_info)


def start_update_process(main_object, update_info):
    """开始更新流程"""
    # 创建自定义进度对话框
    progress_dialog, progress_bar, cancel_button = message_box_util.box_progress(
        main_object,
        "软件更新",
        "正在下载更新..."
    )

    # 显示对话框
    main_object.progress_dialog = progress_dialog
    main_object.progress_dialog.show()
    # 置顶对话框
    main_object.progress_dialog.raise_()

    # 创建下载器
    main_object.downloader = Updater(
        api_url=common.BASE_URL + "/version/public/check?type=Windows",
        app_version=main_object.silent_updater.app_version,
        update_dir=main_object.app_data_update_path
    )

    # 连接信号
    main_object.downloader.progress.connect(progress_bar.setValue)
    main_object.downloader.finished.connect(
        lambda success, _: handle_download_finished(main_object, success, update_info))

    # 取消按钮事件
    cancel_button.clicked.connect(lambda: handle_cancel_download(main_object))

    # 开始下载
    main_object.downloader.download_package(update_info)


def handle_cancel_download(main_object):
    """取消下载处理"""
    if main_object.downloader and main_object.downloader.current_reply:
        main_object.downloader.current_reply.abort()
    if main_object.progress_dialog:
        main_object.progress_dialog.close()


def handle_download_finished(main_object, success, update_info):
    """下载完成处理"""
    main_object.progress_dialog.close()

    if success:
        # 获取下载的文件路径
        download_path = main_object.downloader.downloaded_file_path
        if update_info.get("updateTag"):
            # 大版本更新：运行安装包并退出
            run_installer_and_exit(main_object, download_path)
        else:
            if "exeUrl" in update_info and update_info["exeUrl"] is not None and update_info["exeUrl"] != "":
                # 小版本更新：替换exe文件
                replace_exe_and_restart(main_object, download_path, update_info)
            else:
                # 没有小版本更新文件则默认运行安装包
                run_installer_and_exit(main_object, download_path)
    else:
        message_box_util.box_information(
            main_object,
            "更新失败",
            "下载更新包失败，请检查网络连接或稍后重试"
        )
        main_object.agree_update = False
        main_object.update_ready.emit()

def replace_exe_and_restart(main_object, new_exe_path, update_info):
    """替换exe文件并重启应用"""
    # 获取当前exe的路径
    current_exe_path = os.path.abspath(sys.argv[0])
    # 获取updater_helper的路径（假设在同一目录下）
    helper_path = os.path.join(os.path.dirname(current_exe_path), "patch_updater.exe")
    if not os.path.exists(helper_path):
        message_box_util.box_information(
            main_object,
            "错误",
            "更新失败，您可以在官网下载安装最新版本。"
        )
        main_object.agree_update = False
        main_object.update_ready.emit()
        return
    # 关闭主程序
    main_object.quit_before_do()
    # 运行安装包
    try:
        if sys.platform == "win32":
            os.startfile(helper_path)
        else:
            subprocess.Popen([helper_path])
    except Exception as e:
        message_box_util.box_information(
            main_object,
            "错误",
            f"无法启动安装程序: {str(e)}"
        )
    # 退出应用
    QApplication.quit()


def run_installer_and_exit(main_object, exe_path):
    """运行安装包并退出程序"""
    # 获取当前exe的路径
    current_exe_path = os.path.abspath(sys.argv[0])
    # 获取updater_helper的路径（假设在同一目录下）
    helper_path = os.path.join(os.path.dirname(current_exe_path), "full_updater.exe")
    if not os.path.exists(helper_path):
        message_box_util.box_information(
            main_object,
            "错误",
            "更新失败，您可以在官网下载安装最新版本。"
        )
        main_object.agree_update = False
        main_object.update_ready.emit()
        return
    # 关闭主程序
    main_object.quit_before_do()
    # 运行安装包
    try:
        if sys.platform == "win32":
            os.startfile(helper_path)
        else:
            subprocess.Popen([helper_path])
    except Exception as e:
        message_box_util.box_information(
            main_object,
            "错误",
            f"无法启动安装程序: {str(e)}"
        )
    # 退出应用
    QApplication.quit()


def check_update_normal(main_object):
    """检查更新"""
    try:
        main_object.silent_updater = Updater(
            api_url=common.BASE_URL + "/version/public/check?type=Windows",
            app_version=main_object.app_version,
            update_dir=main_object.app_data_update_path
        )
        main_object.silent_updater.finished.connect(
            lambda success, update_info: handle_silent_update_normal_result(main_object, success, update_info)
        )
        # 直接调用检查更新方法，不再使用线程
        main_object.silent_updater.check_update()
    except Exception as e:
        print(f"检查更新:{e}")


def handle_silent_update_normal_result(main_object, success, update_info):
    """更新检查回调"""
    try:
        if not success or not update_info:
            # 获取更新失败
            return
        # 判断版本是否相同
        if update_info["version"] == main_object.silent_updater.app_version:
            # 无更新，判断是否有更新提示，有更新提示就隐藏
            if main_object.update_red_dot is not None:
                main_object.update_red_dot.hide()
            return
        else:
            # 判断是否需要更新
            if version_constant.compare_version(main_object.silent_updater.app_version, update_info["version"]) >= 0:
                return
            # 有更新，就在检查更新右上角添加/显示更新提示
            button_width = 70
            button_interval = 10
            red_dot_padding = 10
            if main_object.update_red_dot is None:
                main_object.update_red_dot = add_red_dot_in_button(main_object.push_button_setting_version)
                main_object.update_red_dot.move(button_width * 2 + button_interval * 1 - red_dot_padding, red_dot_padding)
            else:
                main_object.update_red_dot.show()
    except Exception as e:
        print(f"静默更新检查回调:{e}")

def add_red_dot_in_button(button):
    # 创建红点Label（确保按钮有父对象）
    red_dot = QLabel(button.parentWidget())
    red_dot.setStyleSheet("""
        background-color: red;
        border-radius: 3px;
        min-width: 6px;
        min-height: 6px;
        max-width: 6px;
        max-height: 6px;
    """)
    red_dot.raise_()  # 确保在最上层
    return red_dot  # 保留引用
