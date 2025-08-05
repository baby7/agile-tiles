import os
import winreg
import sys

# 注册表信息
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

def get_quoted_path(path):
    """处理含空格的路径，添加双引号"""
    if " " in path and not path.startswith('"'):
        return f'"{path}"'
    return path

def is_auto_start_enabled():
    """检查是否已启用自启动"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            WINREG_KEY,
            0, winreg.KEY_READ
        )
        reg_value, _ = winreg.QueryValueEx(key, WINREG_NAME)
        key.Close()
        current_path = get_quoted_path(get_exe_path())
        return os.path.normpath(reg_value) == os.path.normpath(current_path)
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"Error checking auto-start: {e}")
        return False

def set_auto_start(enabled):
    """启用/禁用自启动"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            WINREG_KEY,
            0, winreg.KEY_SET_VALUE
        )
        if enabled:
            current_path = get_quoted_path(get_exe_path())
            print(f"current_path:{current_path}")
            winreg.SetValueEx(key, WINREG_NAME, 0, winreg.REG_SZ, current_path)
        else:
            try:
                winreg.DeleteValue(key, WINREG_NAME)
            except FileNotFoundError:
                pass
        key.Close()
    except Exception as e:
        print(f"Error setting auto-start: {e}")