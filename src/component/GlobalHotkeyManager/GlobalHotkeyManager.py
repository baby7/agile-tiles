import ctypes
from PySide6.QtCore import Signal, QObject

# Windows API 常量定义
MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004
MOD_WIN = 0x0008
WM_HOTKEY = 0x0312

# 虚拟键码映射表 (部分常用键)
VK_KEY_MAP = {
    '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34,
    '5': 0x35, '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39,
    'A': 0x41, 'B': 0x42, 'C': 0x43, 'D': 0x44, 'E': 0x45,
    'F': 0x46, 'G': 0x47, 'H': 0x48, 'I': 0x49, 'J': 0x4A,
    'K': 0x4B, 'L': 0x4C, 'M': 0x4D, 'N': 0x4E, 'O': 0x4F,
    'P': 0x50, 'Q': 0x51, 'R': 0x52, 'S': 0x53, 'T': 0x54,
    'U': 0x55, 'V': 0x56, 'W': 0x57, 'X': 0x58, 'Y': 0x59,
    'Z': 0x5A,
    'F1': 0x70, 'F2': 0x71, 'F3': 0x72, 'F4': 0x73,
    'F5': 0x74, 'F6': 0x75, 'F7': 0x76, 'F8': 0x77,
    'F9': 0x78, 'F10': 0x79, 'F11': 0x7A, 'F12': 0x7B,
    'Space': 0x20, 'Enter': 0x0D, 'Escape': 0x1B,
    'Tab': 0x09, 'Backspace': 0x08, 'Insert': 0x2D,
    'Delete': 0x2E, 'Home': 0x24, 'End': 0x23,
    'PageUp': 0x21, 'PageDown': 0x22,
    'Left': 0x25, 'Right': 0x27, 'Up': 0x26, 'Down': 0x28
}
# 用于热键检测的临时ID（确保不会和正常ID冲突）
TEMP_ID = 0x0000FFFF


class GlobalHotkeyManager(QObject):
    """全局热键管理器"""
    hotkey_triggered = Signal(str)

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.hotkey_ids = {}  # 存储热键ID: (modifiers, key)
        self.next_id = 1  # 热键ID计数器

    @staticmethod
    def parse_hotkey(key_combination):
        """解析热键字符串，返回修饰符和虚拟键码"""
        parts = key_combination.split('+')
        modifiers = 0
        key_name = parts[-1]

        # 解析修饰键
        for mod in parts[:-1]:
            mod_lower = mod.lower()
            if mod_lower == 'ctrl':
                modifiers |= MOD_CONTROL
            elif mod_lower == 'alt':
                modifiers |= MOD_ALT
            elif mod_lower == 'shift':
                modifiers |= MOD_SHIFT
            elif mod_lower == 'win':
                modifiers |= MOD_WIN

        # 获取虚拟键码
        vk_code = VK_KEY_MAP.get(key_name.upper())
        if not vk_code:
            raise ValueError(f"无效的按键: {key_name}")

        return modifiers, vk_code

    @staticmethod
    def is_hotkey_occupied(win_id, key_combination):
        """
        检测热键是否已被占用
        返回: True-已被占用, False-可用
        """
        try:
            modifiers, vk_code = GlobalHotkeyManager.parse_hotkey(key_combination)
        except ValueError:
            return False  # 无效热键视为不可用

        # 尝试注册临时热键检测占用
        success = ctypes.windll.user32.RegisterHotKey(
            win_id,
            TEMP_ID,
            modifiers,
            vk_code
        )

        if success:
            # 注册成功说明未被占用，立即注销临时热键
            ctypes.windll.user32.UnregisterHotKey(win_id, TEMP_ID)
            return False
        else:
            # 获取错误代码判断是否因占用而失败
            error_code = ctypes.windll.kernel32.GetLastError()
            # 0x581 (1409) 表示热键已被占用
            return error_code == 0x581

    def register_hotkey(self, key_combination):
        """
        注册全局热键
        :param key_combination: 格式如 "Ctrl+Shift+A"
        """
        modifiers, vk_code = self.parse_hotkey(key_combination)

        # 注册热键
        hotkey_id = self.next_id
        if not ctypes.windll.user32.RegisterHotKey(
                self.window.winId(), hotkey_id, modifiers, vk_code
        ):
            error_code = ctypes.windll.kernel32.GetLastError()
            if error_code == 0x581:  # 热键已被占用
                raise RuntimeError(f"热键已被占用: {key_combination}")
            else:
                raise RuntimeError(f"注册热键失败，错误代码: {error_code}")

        self.hotkey_ids[hotkey_id] = key_combination
        self.next_id += 1
        return hotkey_id

    def unregister_hotkey(self, hotkey_id):
        """注销热键"""
        if hotkey_id in self.hotkey_ids:
            ctypes.windll.user32.UnregisterHotKey(self.window.winId(), hotkey_id)
            del self.hotkey_ids[hotkey_id]

    def unregister_all(self):
        """注销所有热键"""
        for hotkey_id in list(self.hotkey_ids.keys()):
            self.unregister_hotkey(hotkey_id)

    def handle_hotkey(self, hotkey_id):
        """处理热键触发事件"""
        if hotkey_id in self.hotkey_ids:
            self.hotkey_triggered.emit(self.hotkey_ids[hotkey_id])