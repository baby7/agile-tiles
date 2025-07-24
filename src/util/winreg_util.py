import winreg
import sys

def get_exe_path():
    """获取打包后的exe路径"""
    return sys.executable

def is_auto_start_enabled():
    """检查是否已启用自启动"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_READ
        )
        value, _ = winreg.QueryValueEx(key, "AgileTiles")
        key.Close()
        return value == get_exe_path()
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"Error checking auto-start: {e}")
        return False

def set_auto_start(enabled):
    """启用/禁用自启动"""
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            key_path,
            0, winreg.KEY_SET_VALUE
        )
        if enabled:
            exe_path = get_exe_path()
            winreg.SetValueEx(key, "AgileTiles", 0, winreg.REG_SZ, exe_path)
        else:
            try:
                winreg.DeleteValue(key, "AgileTiles")
            except FileNotFoundError:
                pass
        key.Close()
    except Exception as e:
        print(f"Error setting auto-start: {e}")