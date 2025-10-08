import os
import sys
import traceback

import win32com.client  # 需要安装 pywin32


def get_exe_path():
    """获取正确的可执行文件路径"""
    try:
        if getattr(sys, 'frozen', False):
            # 打包环境：使用sys.executable获取真实路径
            return os.path.abspath(sys.executable)
        else:
            # 开发环境：使用当前脚本路径
            return os.path.abspath(sys.argv[0])
    except Exception as e:
        print(f"获取可执行文件路径失败: {traceback.format_exc()}")
        return None


def get_startup_folder():
    """获取启动文件夹路径"""
    try:
        appdata = os.environ.get('APPDATA', '')
        if not appdata:
            raise Exception("APPDATA environment variable not available")
        return os.path.join(appdata, r'Microsoft\Windows\Start Menu\Programs\Startup')
    except Exception as e:
        print(f"获取启动文件夹路径失败: {traceback.format_exc()}")
        return None


def get_shortcut_path():
    """获取快捷方式路径"""
    return os.path.join(get_startup_folder(), "AgileTiles.lnk")


def is_auto_start_enabled():
    """检查是否已启用自启动"""
    shortcut_path = get_shortcut_path()
    if not os.path.exists(shortcut_path):
        return False
    try:
        # 检查快捷方式指向的路径是否正确
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        current_path = get_exe_path()
        return os.path.normpath(shortcut.Targetpath) == os.path.normpath(current_path)
    except Exception as e:
        print(f"检查快捷方式指向的路径失败: {traceback.format_exc()}")
        return False


def set_auto_start(enabled):
    """启用/禁用自启动"""
    print(f"启用/禁用自启动: {enabled}")
    shortcut_path = get_shortcut_path()
    print(f"快捷方式路径: {shortcut_path}")
    if enabled:
        try:
            # 获取当前可执行文件路径
            target_path = get_exe_path()
            print(f"当前可执行文件路径: {target_path}")
            # 获取工作目录
            working_dir = os.path.dirname(target_path)
            print(f"工作目录: {working_dir}")
            # 确保启动文件夹存在
            startup_folder = get_startup_folder()
            print(f"启动文件夹: {startup_folder}")
            if not os.path.exists(startup_folder):
                print(f"创建启动文件夹: {startup_folder}")
                os.makedirs(startup_folder)
            # 创建快捷方式
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = target_path
            shortcut.WorkingDirectory = working_dir
            shortcut.save()
            print(f"创建快捷方式: {shortcut_path}")
        except Exception as e:
            print(f"创建快捷方式失败: {traceback.format_exc()}")
    else:
        try:
            # 删除快捷方式
            if os.path.exists(shortcut_path):
                os.remove(shortcut_path)
                print(f"删除快捷方式: {shortcut_path}")
        except Exception as e:
            print(f"删除快捷方式失败: {traceback.format_exc()}")
