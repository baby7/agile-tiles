import os
import sys
import win32com.client  # 需要安装 pywin32
import winreg  # 用于清理旧的注册表项

# 注册表信息（用于清理旧版本）
WINREG_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
WINREG_NAME = "AgileTiles"


def get_exe_path():
    """获取正确的可执行文件路径"""
    if getattr(sys, 'frozen', False):
        # 打包环境：使用sys.executable
        return sys.executable
    else:
        # 开发环境：使用当前脚本路径
        return os.path.abspath(sys.argv[0])


def get_startup_folder():
    """获取启动文件夹路径"""
    return os.path.join(os.environ['APPDATA'],
                        r'Microsoft\Windows\Start Menu\Programs\Startup')


def get_shortcut_path():
    """获取快捷方式路径"""
    return os.path.join(get_startup_folder(), "AgileTiles.lnk")


def is_auto_start_enabled():
    """检查是否已启用自启动"""
    # 先检查快捷方式是否存在
    shortcut_path = get_shortcut_path()
    if os.path.exists(shortcut_path):
        try:
            # 检查快捷方式指向的路径是否正确
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            current_path = get_exe_path()
            return os.path.normpath(shortcut.Targetpath) == os.path.normpath(current_path)
        except Exception as e:
            print(f"Error checking shortcut: {e}")

    # 如果没有快捷方式，检查是否有旧的注册表项（兼容旧版本）
    # try:
    #     key = winreg.OpenKey(
    #         winreg.HKEY_CURRENT_USER,
    #         WINREG_KEY,
    #         0, winreg.KEY_READ
    #     )
    #     reg_value, _ = winreg.QueryValueEx(key, WINREG_NAME)
    #     key.Close()
    #     current_path = get_exe_path()
    #     # 处理可能被引号包裹的路径
    #     reg_value = reg_value.strip('"')
    #     return os.path.normpath(reg_value) == os.path.normpath(current_path)
    # except FileNotFoundError:
    #     return False
    # except Exception as e:
    #     print(f"Error checking registry: {e}")
    #     return False


def cleanup_old_registry_entry():
    """清理旧的注册表项"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            WINREG_KEY,
            0, winreg.KEY_SET_VALUE
        )
        try:
            winreg.DeleteValue(key, WINREG_NAME)
            print("Removed old registry entry")
        except FileNotFoundError:
            pass  # 如果不存在，忽略错误
        key.Close()
    except Exception as e:
        print(f"Error cleaning up registry: {e}")


def set_auto_start(enabled):
    """启用/禁用自启动"""
    # 无论启用还是禁用，都先清理旧的注册表项
    cleanup_old_registry_entry()

    shortcut_path = get_shortcut_path()

    if enabled:
        try:
            # 获取当前可执行文件路径
            target_path = get_exe_path()
            # 获取工作目录
            working_dir = os.path.dirname(target_path)

            # 确保启动文件夹存在
            startup_folder = get_startup_folder()
            if not os.path.exists(startup_folder):
                os.makedirs(startup_folder)

            # 创建快捷方式
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = target_path
            shortcut.WorkingDirectory = working_dir
            shortcut.save()
            print(f"Created shortcut at: {shortcut_path}")
        except Exception as e:
            print(f"Error creating shortcut: {e}")
    else:
        try:
            # 删除快捷方式
            if os.path.exists(shortcut_path):
                os.remove(shortcut_path)
                print(f"Removed shortcut: {shortcut_path}")
        except Exception as e:
            print(f"Error removing shortcut: {e}")