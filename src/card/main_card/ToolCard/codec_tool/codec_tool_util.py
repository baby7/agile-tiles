import base64
import urllib.parse
from PySide6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QGridLayout, QApplication

from src.module import dialog_module
from src.ui import style_util


def clear_click(input_text, output_text):
    input_text.clear()
    output_text.clear()

def copy_click(output_text):
    text = output_text.toPlainText()
    if not text:
        output_text.setText("请先进行编码/解码")
        return
    try:
        QApplication.clipboard().setText(text)
        output_text.setText("复制到剪贴板成功")
    except Exception as e:
        output_text.setText("复制到剪贴板失败")


class MorseCodec:
    """摩尔斯电码编码解码器"""
    MORSE_CODE_DICT = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
        'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
        'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
        'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
        'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
        'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--',
        '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
        '9': '----.', '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.',
        '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...',
        ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-',
        '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.', ' ': '/'
    }

    # 反向字典
    REVERSE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}

    @classmethod
    def encode(cls, text):
        """将文本编码为摩尔斯电码"""
        text = text.upper()
        morse = []
        for char in text:
            if char in cls.MORSE_CODE_DICT:
                morse.append(cls.MORSE_CODE_DICT[char])
            else:
                morse.append('?')  # 未知字符用问号代替
        return ' '.join(morse)

    @classmethod
    def decode(cls, morse):
        """将摩尔斯电码解码为文本"""
        words = morse.split(' ')
        text = []
        for code in words:
            if code in cls.REVERSE_DICT:
                text.append(cls.REVERSE_DICT[code])
            elif code == '':
                continue  # 忽略多余的空格
            else:
                text.append('?')  # 未知电码用问号代替
        return ''.join(text)


class Base64Tab(QWidget):
    """Base64编码解码标签页"""

    def __init__(self, use_parent):
        super().__init__()
        self.use_parent = use_parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

        # 输入框
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("输入文本（将进行Base64编码/解码）\n例如: Hello World! 或 SGVsbG8gV29ybGQh")
        self.input_text.setMaximumHeight(100)
        layout.addWidget(self.input_text)

        # 按钮
        btn_layout = QHBoxLayout()
        self.encode_btn = QPushButton("Base64编码")
        self.encode_btn.setMinimumHeight(35)
        self.encode_btn.setMaximumHeight(35)
        self.encode_btn.clicked.connect(self.encode_text)
        btn_layout.addWidget(self.encode_btn)

        self.decode_btn = QPushButton("Base64解码")
        self.decode_btn.setMinimumHeight(35)
        self.decode_btn.setMaximumHeight(35)
        self.decode_btn.clicked.connect(self.decode_text)
        btn_layout.addWidget(self.decode_btn)

        layout.addLayout(btn_layout)

        # 输出框
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("输出结果")
        layout.addWidget(self.output_text)

        # 结果按钮
        result_layout = QHBoxLayout()
        self.clear_btn = QPushButton("清空")
        self.clear_btn.setMinimumHeight(35)
        self.clear_btn.setMaximumHeight(35)
        self.clear_btn.clicked.connect(lambda : clear_click(self.input_text, self.output_text))
        result_layout.addWidget(self.clear_btn)
        self.copy_btn = QPushButton("复制")
        self.copy_btn.setMinimumHeight(35)
        self.copy_btn.setMaximumHeight(35)
        self.copy_btn.clicked.connect(lambda : copy_click(self.output_text))
        result_layout.addWidget(self.copy_btn)
        layout.addLayout(result_layout)

        self.setLayout(layout)

    def encode_text(self):
        text = self.input_text.toPlainText()
        if not text:
            dialog_module.box_information(self.use_parent, "警告", "请输入要编码的文本")
            return

        try:
            # 转换为bytes然后进行base64编码
            encoded_bytes = base64.b64encode(text.encode('utf-8'))
            result = encoded_bytes.decode('utf-8')
            self.output_text.setPlainText(result)
        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"编码时发生错误: {str(e)}")

    def decode_text(self):
        text = self.input_text.toPlainText()
        if not text:
            dialog_module.box_information(self.use_parent, "警告", "请输入要解码的文本")
            return

        try:
            # 进行base64解码
            decoded_bytes = base64.b64decode(text)
            result = decoded_bytes.decode('utf-8')
            self.output_text.setPlainText(result)
        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"解码时发生错误: {str(e)}")


class UrlTab(QWidget):
    """URL编码解码标签页"""

    def __init__(self, use_parent):
        super().__init__()
        self.use_parent = use_parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

        # 输入框
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("输入文本（将进行URL编码/解码）\n例如: Hello World! 或 Hello%20World%21")
        self.input_text.setMaximumHeight(100)
        layout.addWidget(self.input_text)

        # 按钮
        btn_layout = QGridLayout()
        self.encode_uri_btn = QPushButton("encodeURI编码")
        self.encode_uri_btn.setMinimumHeight(35)
        self.encode_uri_btn.setMaximumHeight(35)
        self.encode_uri_btn.clicked.connect(self.encode_uri)
        btn_layout.addWidget(self.encode_uri_btn, 0, 0)

        self.encode_component_btn = QPushButton("encodeURIComponent编码")
        self.encode_component_btn.setMinimumHeight(35)
        self.encode_component_btn.setMaximumHeight(35)
        self.encode_component_btn.clicked.connect(self.encode_component)
        btn_layout.addWidget(self.encode_component_btn, 0, 1)

        self.decode_btn = QPushButton("URL解码")
        self.decode_btn.setMinimumHeight(35)
        self.decode_btn.setMaximumHeight(35)
        self.decode_btn.clicked.connect(self.decode_url)
        btn_layout.addWidget(self.decode_btn, 1, 0, 1, 2)  # 跨两列

        layout.addLayout(btn_layout)

        # 输出框
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("输出结果")
        layout.addWidget(self.output_text)

        # 结果按钮
        result_layout = QHBoxLayout()
        self.clear_btn = QPushButton("清空")
        self.clear_btn.setMinimumHeight(35)
        self.clear_btn.setMaximumHeight(35)
        self.clear_btn.clicked.connect(lambda : clear_click(self.input_text, self.output_text))
        result_layout.addWidget(self.clear_btn)
        self.copy_btn = QPushButton("复制")
        self.copy_btn.setMinimumHeight(35)
        self.copy_btn.setMaximumHeight(35)
        self.copy_btn.clicked.connect(lambda : copy_click(self.output_text))
        result_layout.addWidget(self.copy_btn)
        layout.addLayout(result_layout)

        self.setLayout(layout)

    def encode_uri(self):
        text = self.input_text.toPlainText()
        if not text:
            dialog_module.box_information(self.use_parent, "警告", "请输入要编码的文本")
            return

        try:
            # encodeURI风格编码（不编码保留字符如:/?#[]@!$&'()*+,;=）
            result = urllib.parse.quote(text, safe=";/?:@&=+$,#")
            self.output_text.setPlainText(result)
        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"编码时发生错误: {str(e)}")

    def encode_component(self):
        text = self.input_text.toPlainText()
        if not text:
            dialog_module.box_information(self.use_parent, "警告", "请输入要编码的文本")
            return

        try:
            # encodeURIComponent风格编码（编码所有特殊字符）
            result = urllib.parse.quote(text, safe='')
            self.output_text.setPlainText(result)
        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"编码时发生错误: {str(e)}")

    def decode_url(self):
        text = self.input_text.toPlainText()
        if not text:
            dialog_module.box_information(self.use_parent, "警告", "请输入要解码的文本")
            return

        try:
            # URL解码
            result = urllib.parse.unquote(text)
            self.output_text.setPlainText(result)
        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"解码时发生错误: {str(e)}")


class AsciiTab(QWidget):
    """ASCII编码解码标签页"""

    def __init__(self, use_parent):
        super().__init__()
        self.use_parent = use_parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

        # 输入框
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("输入文本（将进行ASCII编码/解码）\n例如: Hello 或 72 101 108 108 111")
        self.input_text.setMaximumHeight(100)
        layout.addWidget(self.input_text)

        # 按钮
        btn_layout = QHBoxLayout()
        self.encode_btn = QPushButton("ASCII编码")
        self.encode_btn.setMinimumHeight(35)
        self.encode_btn.setMaximumHeight(35)
        self.encode_btn.clicked.connect(self.encode_ascii)
        btn_layout.addWidget(self.encode_btn)

        self.decode_btn = QPushButton("ASCII解码")
        self.decode_btn.setMinimumHeight(35)
        self.decode_btn.setMaximumHeight(35)
        self.decode_btn.clicked.connect(self.decode_ascii)
        btn_layout.addWidget(self.decode_btn)

        layout.addLayout(btn_layout)

        # 输出框
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("输出结果")
        layout.addWidget(self.output_text)

        # 结果按钮
        result_layout = QHBoxLayout()
        self.clear_btn = QPushButton("清空")
        self.clear_btn.setMinimumHeight(35)
        self.clear_btn.setMaximumHeight(35)
        self.clear_btn.clicked.connect(lambda : clear_click(self.input_text, self.output_text))
        result_layout.addWidget(self.clear_btn)
        self.copy_btn = QPushButton("复制")
        self.copy_btn.setMinimumHeight(35)
        self.copy_btn.setMaximumHeight(35)
        self.copy_btn.clicked.connect(lambda : copy_click(self.output_text))
        result_layout.addWidget(self.copy_btn)
        layout.addLayout(result_layout)

        self.setLayout(layout)

    def encode_ascii(self):
        text = self.input_text.toPlainText()
        if not text:
            dialog_module.box_information(self.use_parent, "警告", "请输入要编码的文本")
            return

        try:
            # 将每个字符转换为其ASCII码
            ascii_codes = [str(ord(char)) for char in text]
            result = ' '.join(ascii_codes)
            self.output_text.setPlainText(result)
        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"编码时发生错误: {str(e)}")

    def decode_ascii(self):
        text = self.input_text.toPlainText()
        if not text:
            dialog_module.box_information(self.use_parent, "警告", "请输入要解码的ASCII码（空格分隔）")
            return

        try:
            # 将ASCII码转换回字符
            ascii_codes = text.split()
            chars = [chr(int(code)) for code in ascii_codes]
            result = ''.join(chars)
            self.output_text.setPlainText(result)
        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"解码时发生错误: {str(e)}")


class MorseTab(QWidget):
    """摩尔斯电码编码解码标签页"""

    def __init__(self, use_parent):
        super().__init__()
        self.use_parent = use_parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

        # 输入框
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("输入文本（将进行摩尔斯电码编码/解码）\n例如: SOS 或 ... --- ...")
        self.input_text.setMaximumHeight(100)
        layout.addWidget(self.input_text)

        # 按钮
        btn_layout = QHBoxLayout()
        self.encode_btn = QPushButton("摩尔斯编码")
        self.encode_btn.setMinimumHeight(35)
        self.encode_btn.setMaximumHeight(35)
        self.encode_btn.clicked.connect(self.encode_morse)
        btn_layout.addWidget(self.encode_btn)

        self.decode_btn = QPushButton("摩尔斯解码")
        self.decode_btn.setMinimumHeight(35)
        self.decode_btn.setMaximumHeight(35)
        self.decode_btn.clicked.connect(self.decode_morse)
        btn_layout.addWidget(self.decode_btn)

        layout.addLayout(btn_layout)

        # 输出框
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("输出结果")
        layout.addWidget(self.output_text)

        # 结果按钮
        result_layout = QHBoxLayout()
        self.clear_btn = QPushButton("清空")
        self.clear_btn.setMinimumHeight(35)
        self.clear_btn.setMaximumHeight(35)
        self.clear_btn.clicked.connect(lambda : clear_click(self.input_text, self.output_text))
        result_layout.addWidget(self.clear_btn)
        self.copy_btn = QPushButton("复制")
        self.copy_btn.setMinimumHeight(35)
        self.copy_btn.setMaximumHeight(35)
        self.copy_btn.clicked.connect(lambda : copy_click(self.output_text))
        result_layout.addWidget(self.copy_btn)
        layout.addLayout(result_layout)

        self.setLayout(layout)

    def encode_morse(self):
        text = self.input_text.toPlainText()
        if not text:
            dialog_module.box_information(self.use_parent, "警告", "请输入要编码的文本")
            return

        try:
            result = MorseCodec.encode(text)
            self.output_text.setPlainText(result)
        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"编码时发生错误: {str(e)}")

    def decode_morse(self):
        text = self.input_text.toPlainText()
        if not text:
            dialog_module.box_information(self.use_parent, "警告", "请输入要解码的摩尔斯电码")
            return

        try:
            result = MorseCodec.decode(text)
            self.output_text.setPlainText(result)
        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"解码时发生错误: {str(e)}")


class EncodingTab(QWidget):
    """字符编码转换标签页"""

    def __init__(self, use_parent):
        super().__init__()
        self.use_parent = use_parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

        # 输入框
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("输入文本（将进行字符编码转换）\n例如: 你好 或 \\u4f60\\u597d")
        self.input_text.setMaximumHeight(100)
        layout.addWidget(self.input_text)

        # 按钮 - 使用网格布局，每行两个按钮
        btn_layout = QGridLayout()

        self.to_unicode_btn = QPushButton("转换为Unicode")
        self.to_unicode_btn.setMinimumHeight(35)
        self.to_unicode_btn.setMaximumHeight(35)
        self.to_unicode_btn.clicked.connect(self.to_unicode)
        btn_layout.addWidget(self.to_unicode_btn, 0, 0)

        self.from_unicode_btn = QPushButton("从Unicode转换")
        self.from_unicode_btn.setMinimumHeight(35)
        self.from_unicode_btn.setMaximumHeight(35)
        self.from_unicode_btn.clicked.connect(self.from_unicode)
        btn_layout.addWidget(self.from_unicode_btn, 0, 1)

        self.to_utf8_btn = QPushButton("转换为UTF-8字节")
        self.to_utf8_btn.setMinimumHeight(35)
        self.to_utf8_btn.setMaximumHeight(35)
        self.to_utf8_btn.clicked.connect(self.to_utf8)
        btn_layout.addWidget(self.to_utf8_btn, 1, 0)

        self.from_utf8_btn = QPushButton("从UTF-8字节转换")
        self.from_utf8_btn.setMinimumHeight(35)
        self.from_utf8_btn.setMaximumHeight(35)
        self.from_utf8_btn.clicked.connect(self.from_utf8)
        btn_layout.addWidget(self.from_utf8_btn, 1, 1)

        self.to_gbk_btn = QPushButton("转换为GBK字节")
        self.to_gbk_btn.setMinimumHeight(35)
        self.to_gbk_btn.setMaximumHeight(35)
        self.to_gbk_btn.clicked.connect(self.to_gbk)
        btn_layout.addWidget(self.to_gbk_btn, 2, 0)

        self.from_gbk_btn = QPushButton("从GBK字节转换")
        self.from_gbk_btn.setMinimumHeight(35)
        self.from_gbk_btn.setMaximumHeight(35)
        self.from_gbk_btn.clicked.connect(self.from_gbk)
        btn_layout.addWidget(self.from_gbk_btn, 2, 1)

        layout.addLayout(btn_layout)

        # 输出框
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("输出结果")
        layout.addWidget(self.output_text)

        # 结果按钮
        result_layout = QHBoxLayout()
        self.clear_btn = QPushButton("清空")
        self.clear_btn.setMinimumHeight(35)
        self.clear_btn.setMaximumHeight(35)
        self.clear_btn.clicked.connect(lambda : clear_click(self.input_text, self.output_text))
        result_layout.addWidget(self.clear_btn)
        self.copy_btn = QPushButton("复制")
        self.copy_btn.setMinimumHeight(35)
        self.copy_btn.setMaximumHeight(35)
        self.copy_btn.clicked.connect(lambda : copy_click(self.output_text))
        result_layout.addWidget(self.copy_btn)
        layout.addLayout(result_layout)

        self.setLayout(layout)

    def to_unicode(self):
        text = self.input_text.toPlainText()
        if not text:
            dialog_module.box_information(self.use_parent, "警告", "请输入要转换的文本")
            return

        try:
            # 将每个字符转换为其Unicode转义序列
            unicode_seq = []
            for char in text:
                code_point = ord(char)
                if code_point < 0x10000:
                    unicode_seq.append(f"\\u{code_point:04x}")
                else:
                    # 处理辅助平面字符
                    code_point -= 0x10000
                    high_surrogate = 0xD800 + (code_point >> 10)
                    low_surrogate = 0xDC00 + (code_point & 0x3FF)
                    unicode_seq.append(f"\\u{high_surrogate:04x}\\u{low_surrogate:04x}")

            result = ''.join(unicode_seq)
            self.output_text.setPlainText(result)
        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"转换时发生错误: {str(e)}")

    def from_unicode(self):
        text = self.input_text.toPlainText()
        if not text:
            dialog_module.box_information(self.use_parent, "警告", "请输入Unicode转义序列")
            return

        try:
            # 简单的Unicode转义序列解析
            result = ""
            i = 0
            while i < len(text):
                if text[i] == '\\' and i + 1 < len(text):
                    if text[i + 1] == 'u' and i + 5 < len(text):
                        # 解析Unicode转义序列
                        hex_str = text[i + 2:i + 6]
                        code_point = int(hex_str, 16)
                        result += chr(code_point)
                        i += 6
                        continue
                    elif text[i + 1] == 'U' and i + 9 < len(text):
                        # 解析长格式Unicode转义序列
                        hex_str = text[i + 2:i + 10]
                        code_point = int(hex_str, 16)
                        result += chr(code_point)
                        i += 10
                        continue

                result += text[i]
                i += 1

            self.output_text.setPlainText(result)
        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"转换时发生错误: {str(e)}")

    def to_utf8(self):
        text = self.input_text.toPlainText()
        if not text:
            dialog_module.box_information(self.use_parent, "警告", "请输入要转换的文本")
            return

        try:
            # 转换为UTF-8字节
            utf8_bytes = text.encode('utf-8')
            # 显示为十六进制
            hex_str = ' '.join(f"{b:02x}" for b in utf8_bytes)
            self.output_text.setPlainText(hex_str)
        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"转换时发生错误: {str(e)}")

    def from_utf8(self):
        text = self.input_text.toPlainText()
        if not text:
            dialog_module.box_information(self.use_parent, "警告", "请输入UTF-8字节（十六进制，空格分隔）")
            return

        try:
            # 从十六进制字符串解析字节
            hex_values = text.split()
            bytes_data = bytes(int(x, 16) for x in hex_values)
            # 解码为字符串
            result = bytes_data.decode('utf-8')
            self.output_text.setPlainText(result)
        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"转换时发生错误: {str(e)}")

    def to_gbk(self):
        text = self.input_text.toPlainText()
        if not text:
            dialog_module.box_information(self.use_parent, "警告", "请输入要转换的文本")
            return

        try:
            # 转换为GBK字节
            gbk_bytes = text.encode('gbk')
            # 显示为十六进制
            hex_str = ' '.join(f"{b:02x}" for b in gbk_bytes)
            self.output_text.setPlainText(hex_str)
        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"转换时发生错误: {str(e)}")

    def from_gbk(self):
        text = self.input_text.toPlainText()
        if not text:
            dialog_module.box_information(self.use_parent, "警告", "请输入GBK字节（十六进制，空格分隔）")
            return

        try:
            # 从十六进制字符串解析字节
            hex_values = text.split()
            bytes_data = bytes(int(x, 16) for x in hex_values)
            # 解码为字符串
            result = bytes_data.decode('gbk')
            self.output_text.setPlainText(result)
        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"转换时发生错误: {str(e)}")


class CodecTool(QWidget):

    def __init__(self, parent=None, main_object=None, is_dark=None):
        super().__init__(parent=parent)
        # 初始化
        self.parent = parent
        self.use_parent = main_object
        # 初始化界面
        self.init_ui()
        # 设置样式
        style_util.set_dialog_control_style(self, is_dark)

    def init_ui(self):
        # 主部件和布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 创建标签页容器
        self.tabs = QTabWidget()

        # 添加各个标签页
        self.base64_tab = Base64Tab(self.use_parent)
        self.url_tab = UrlTab(self.use_parent)
        self.ascii_tab = AsciiTab(self.use_parent)
        self.morse_tab = MorseTab(self.use_parent)
        self.encoding_tab = EncodingTab(self.use_parent)

        self.tabs.addTab(self.base64_tab, "Base64")
        self.tabs.addTab(self.url_tab, "URL编码")
        self.tabs.addTab(self.ascii_tab, "ASCII")
        self.tabs.addTab(self.morse_tab, "摩尔斯电码")
        self.tabs.addTab(self.encoding_tab, "字符编码")

        main_layout.addWidget(self.tabs)

    def refresh_theme(self, main_object):
        # 设置样式
        style_util.set_dialog_control_style(self, main_object.is_dark)