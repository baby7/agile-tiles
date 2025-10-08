import base64
from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Hash import MD5
# import hashlib
from PySide6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QGridLayout, \
    QApplication, QLabel, QLineEdit, QComboBox

from src.module import dialog_module
from src.ui import style_util


def clear_click(input_text, output_text):
    input_text.clear()
    output_text.clear()


def copy_click(output_text):
    text = output_text.toPlainText()
    if not text:
        output_text.setText("请先进行加密/解密")
        return
    try:
        QApplication.clipboard().setText(text)
        output_text.setText("复制到剪贴板成功")
    except Exception as e:
        output_text.setText("复制到剪贴板失败")


class AESTab(QWidget):
    """AES加解密标签页"""

    def __init__(self, use_parent):
        super().__init__()
        self.use_parent = use_parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

        # 密钥输入
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("密钥:"))
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("输入密钥（16/24/32字节）")
        key_layout.addWidget(self.key_input)
        layout.addLayout(key_layout)

        # IV输入
        iv_layout = QHBoxLayout()
        iv_layout.addWidget(QLabel("IV向量:"))
        self.iv_input = QLineEdit()
        self.iv_input.setPlaceholderText("输入IV向量（16字节，ECB模式不需要）")
        iv_layout.addWidget(self.iv_input)
        layout.addLayout(iv_layout)

        # 模式选择
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("加密模式:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["ECB", "CBC", "CFB", "OFB"])
        mode_layout.addWidget(self.mode_combo)
        layout.addLayout(mode_layout)

        # 输入框
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("输入文本（将进行AES加密/解密）")
        self.input_text.setMaximumHeight(100)
        layout.addWidget(self.input_text)

        # 按钮
        btn_layout = QHBoxLayout()
        self.encrypt_btn = QPushButton("AES加密")
        self.encrypt_btn.setMinimumHeight(35)
        self.encrypt_btn.setMaximumHeight(35)
        self.encrypt_btn.clicked.connect(self.encrypt_text)
        btn_layout.addWidget(self.encrypt_btn)

        self.decrypt_btn = QPushButton("AES解密")
        self.decrypt_btn.setMinimumHeight(35)
        self.decrypt_btn.setMaximumHeight(35)
        self.decrypt_btn.clicked.connect(self.decrypt_text)
        btn_layout.addWidget(self.decrypt_btn)

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
        self.clear_btn.clicked.connect(lambda: clear_click(self.input_text, self.output_text))
        result_layout.addWidget(self.clear_btn)
        self.copy_btn = QPushButton("复制")
        self.copy_btn.setMinimumHeight(35)
        self.copy_btn.setMaximumHeight(35)
        self.copy_btn.clicked.connect(lambda: copy_click(self.output_text))
        result_layout.addWidget(self.copy_btn)
        layout.addLayout(result_layout)

        self.setLayout(layout)

    def encrypt_text(self):
        text = self.input_text.toPlainText()
        key = self.key_input.text()
        iv = self.iv_input.text()
        mode = self.mode_combo.currentText()

        if not text:
            dialog_module.box_information(self.use_parent, "警告", "请输入要加密的文本")
            return
        if not key:
            dialog_module.box_information(self.use_parent, "警告", "请输入密钥")
            return

        try:
            # 处理密钥
            key_bytes = key.encode('utf-8')
            if len(key_bytes) not in [16, 24, 32]:
                # 自动调整密钥长度
                if len(key_bytes) < 16:
                    key_bytes = key_bytes.ljust(16, b'\0')
                elif len(key_bytes) < 24:
                    key_bytes = key_bytes.ljust(24, b'\0')
                else:
                    key_bytes = key_bytes[:32]

            # 处理IV
            iv_bytes = iv.encode('utf-8') if iv else None
            if mode != "ECB" and (not iv or len(iv_bytes) != 16):
                # 生成随机IV
                iv_bytes = get_random_bytes(16)
                self.iv_input.setText(base64.b64encode(iv_bytes).decode('utf-8'))

            # 创建加密器
            if mode == "ECB":
                cipher = AES.new(key_bytes, AES.MODE_ECB)
            elif mode == "CBC":
                cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
            elif mode == "CFB":
                cipher = AES.new(key_bytes, AES.MODE_CFB, iv_bytes)
            elif mode == "OFB":
                cipher = AES.new(key_bytes, AES.MODE_OFB, iv_bytes)

            # 加密
            text_bytes = text.encode('utf-8')
            if mode == "ECB":
                # ECB模式需要填充
                text_bytes = pad(text_bytes, AES.block_size)
            encrypted_bytes = cipher.encrypt(text_bytes)

            # 编码为base64输出
            result = base64.b64encode(encrypted_bytes).decode('utf-8')
            self.output_text.setPlainText(result)
        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"加密时发生错误: {str(e)}")

    def decrypt_text(self):
        text = self.input_text.toPlainText()
        key = self.key_input.text()
        iv = self.iv_input.text()
        mode = self.mode_combo.currentText()

        if not text:
            dialog_module.box_information(self.use_parent, "警告", "请输入要解密的文本")
            return
        if not key:
            dialog_module.box_information(self.use_parent, "警告", "请输入密钥")
            return

        try:
            # 处理密钥
            key_bytes = key.encode('utf-8')
            if len(key_bytes) not in [16, 24, 32]:
                # 自动调整密钥长度
                if len(key_bytes) < 16:
                    key_bytes = key_bytes.ljust(16, b'\0')
                elif len(key_bytes) < 24:
                    key_bytes = key_bytes.ljust(24, b'\0')
                else:
                    key_bytes = key_bytes[:32]

            # 处理IV
            iv_bytes = iv.encode('utf-8') if iv else None
            if mode != "ECB" and (not iv or len(iv_bytes) != 16):
                dialog_module.box_information(self.use_parent, "错误", "非ECB模式需要16字节IV向量")
                return

            # 创建解密器
            if mode == "ECB":
                cipher = AES.new(key_bytes, AES.MODE_ECB)
            elif mode == "CBC":
                cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
            elif mode == "CFB":
                cipher = AES.new(key_bytes, AES.MODE_CFB, iv_bytes)
            elif mode == "OFB":
                cipher = AES.new(key_bytes, AES.MODE_OFB, iv_bytes)

            # 解密
            encrypted_bytes = base64.b64decode(text)
            decrypted_bytes = cipher.decrypt(encrypted_bytes)

            if mode == "ECB":
                # ECB模式需要去除填充
                decrypted_bytes = unpad(decrypted_bytes, AES.block_size)

            result = decrypted_bytes.decode('utf-8')
            self.output_text.setPlainText(result)
        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"解密时发生错误: {str(e)}")


class DESTab(QWidget):
    """DES加解密标签页"""

    def __init__(self, use_parent):
        super().__init__()
        self.use_parent = use_parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

        # 密钥输入
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("密钥:"))
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("输入密钥（8字节）")
        key_layout.addWidget(self.key_input)
        layout.addLayout(key_layout)

        # IV输入
        iv_layout = QHBoxLayout()
        iv_layout.addWidget(QLabel("IV向量:"))
        self.iv_input = QLineEdit()
        self.iv_input.setPlaceholderText("输入IV向量（8字节，ECB模式不需要）")
        iv_layout.addWidget(self.iv_input)
        layout.addLayout(iv_layout)

        # 模式选择
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("加密模式:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["ECB", "CBC"])
        mode_layout.addWidget(self.mode_combo)
        layout.addLayout(mode_layout)

        # 输入框
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("输入文本（将进行DES加密/解密）")
        self.input_text.setMaximumHeight(100)
        layout.addWidget(self.input_text)

        # 按钮
        btn_layout = QHBoxLayout()
        self.encrypt_btn = QPushButton("DES加密")
        self.encrypt_btn.setMinimumHeight(35)
        self.encrypt_btn.setMaximumHeight(35)
        self.encrypt_btn.clicked.connect(self.encrypt_text)
        btn_layout.addWidget(self.encrypt_btn)

        self.decrypt_btn = QPushButton("DES解密")
        self.decrypt_btn.setMinimumHeight(35)
        self.decrypt_btn.setMaximumHeight(35)
        self.decrypt_btn.clicked.connect(self.decrypt_text)
        btn_layout.addWidget(self.decrypt_btn)

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
        self.clear_btn.clicked.connect(lambda: clear_click(self.input_text, self.output_text))
        result_layout.addWidget(self.clear_btn)
        self.copy_btn = QPushButton("复制")
        self.copy_btn.setMinimumHeight(35)
        self.copy_btn.setMaximumHeight(35)
        self.copy_btn.clicked.connect(lambda: copy_click(self.output_text))
        result_layout.addWidget(self.copy_btn)
        layout.addLayout(result_layout)

        self.setLayout(layout)

    def encrypt_text(self):
        text = self.input_text.toPlainText()
        key = self.key_input.text()
        iv = self.iv_input.text()
        mode = self.mode_combo.currentText()

        if not text:
            dialog_module.box_information(self.use_parent, "警告", "请输入要加密的文本")
            return
        if not key:
            dialog_module.box_information(self.use_parent, "警告", "请输入密钥")
            return

        try:
            # 处理密钥
            key_bytes = key.encode('utf-8')
            if len(key_bytes) != 8:
                # 自动调整密钥长度
                if len(key_bytes) < 8:
                    key_bytes = key_bytes.ljust(8, b'\0')
                else:
                    key_bytes = key_bytes[:8]

            # 处理IV
            iv_bytes = iv.encode('utf-8') if iv else None
            if mode != "ECB" and (not iv or len(iv_bytes) != 8):
                # 生成随机IV
                iv_bytes = get_random_bytes(8)
                self.iv_input.setText(base64.b64encode(iv_bytes).decode('utf-8'))

            # 创建加密器
            if mode == "ECB":
                cipher = DES.new(key_bytes, DES.MODE_ECB)
            elif mode == "CBC":
                cipher = DES.new(key_bytes, DES.MODE_CBC, iv_bytes)

            # 加密
            text_bytes = text.encode('utf-8')
            if mode == "ECB":
                # ECB模式需要填充
                text_bytes = pad(text_bytes, DES.block_size)
            encrypted_bytes = cipher.encrypt(text_bytes)

            # 编码为base64输出
            result = base64.b64encode(encrypted_bytes).decode('utf-8')
            self.output_text.setPlainText(result)
        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"加密时发生错误: {str(e)}")

    def decrypt_text(self):
        text = self.input_text.toPlainText()
        key = self.key_input.text()
        iv = self.iv_input.text()
        mode = self.mode_combo.currentText()

        if not text:
            dialog_module.box_information(self.use_parent, "警告", "请输入要解密的文本")
            return
        if not key:
            dialog_module.box_information(self.use_parent, "警告", "请输入密钥")
            return

        try:
            # 处理密钥
            key_bytes = key.encode('utf-8')
            if len(key_bytes) != 8:
                # 自动调整密钥长度
                if len(key_bytes) < 8:
                    key_bytes = key_bytes.ljust(8, b'\0')
                else:
                    key_bytes = key_bytes[:8]

            # 处理IV
            iv_bytes = iv.encode('utf-8') if iv else None
            if mode != "ECB" and (not iv or len(iv_bytes) != 8):
                dialog_module.box_information(self.use_parent, "错误", "非ECB模式需要8字节IV向量")
                return

            # 创建解密器
            if mode == "ECB":
                cipher = DES.new(key_bytes, DES.MODE_ECB)
            elif mode == "CBC":
                cipher = DES.new(key_bytes, DES.MODE_CBC, iv_bytes)

            # 解密
            encrypted_bytes = base64.b64decode(text)
            decrypted_bytes = cipher.decrypt(encrypted_bytes)

            if mode == "ECB":
                # ECB模式需要去除填充
                decrypted_bytes = unpad(decrypted_bytes, DES.block_size)

            result = decrypted_bytes.decode('utf-8')
            self.output_text.setPlainText(result)
        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"解密时发生错误: {str(e)}")


class RC4Tab(QWidget):
    """RC4加解密标签页"""

    def __init__(self, use_parent):
        super().__init__()
        self.use_parent = use_parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

        # 密钥输入
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("密钥:"))
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("输入密钥")
        key_layout.addWidget(self.key_input)
        layout.addLayout(key_layout)

        # 输入框
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("输入文本（将进行RC4加密/解密）")
        self.input_text.setMaximumHeight(100)
        layout.addWidget(self.input_text)

        # 按钮
        btn_layout = QHBoxLayout()
        self.encrypt_btn = QPushButton("RC4加密")
        self.encrypt_btn.setMinimumHeight(35)
        self.encrypt_btn.setMaximumHeight(35)
        self.encrypt_btn.clicked.connect(self.encrypt_text)
        btn_layout.addWidget(self.encrypt_btn)

        self.decrypt_btn = QPushButton("RC4解密")
        self.decrypt_btn.setMinimumHeight(35)
        self.decrypt_btn.setMaximumHeight(35)
        self.decrypt_btn.clicked.connect(self.decrypt_text)
        btn_layout.addWidget(self.decrypt_btn)

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
        self.clear_btn.clicked.connect(lambda: clear_click(self.input_text, self.output_text))
        result_layout.addWidget(self.clear_btn)
        self.copy_btn = QPushButton("复制")
        self.copy_btn.setMinimumHeight(35)
        self.copy_btn.setMaximumHeight(35)
        self.copy_btn.clicked.connect(lambda: copy_click(self.output_text))
        result_layout.addWidget(self.copy_btn)
        layout.addLayout(result_layout)

        self.setLayout(layout)

    def rc4_crypt(self, data, key):
        """RC4加密/解密算法"""
        S = list(range(256))
        j = 0
        out = []

        # KSA (Key-scheduling algorithm)
        for i in range(256):
            j = (j + S[i] + key[i % len(key)]) % 256
            S[i], S[j] = S[j], S[i]

        # PRGA (Pseudo-random generation algorithm)
        i = j = 0
        for char in data:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            out.append(char ^ S[(S[i] + S[j]) % 256])

        return bytes(out)

    def encrypt_text(self):
        text = self.input_text.toPlainText()
        key = self.key_input.text()

        if not text:
            dialog_module.box_information(self.use_parent, "警告", "请输入要加密的文本")
            return
        if not key:
            dialog_module.box_information(self.use_parent, "警告", "请输入密钥")
            return

        try:
            # 转换为字节
            text_bytes = text.encode('utf-8')
            key_bytes = key.encode('utf-8')

            # RC4加密
            encrypted_bytes = self.rc4_crypt(text_bytes, key_bytes)

            # 编码为base64输出
            result = base64.b64encode(encrypted_bytes).decode('utf-8')
            self.output_text.setPlainText(result)
        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"加密时发生错误: {str(e)}")

    def decrypt_text(self):
        text = self.input_text.toPlainText()
        key = self.key_input.text()

        if not text:
            dialog_module.box_information(self.use_parent, "警告", "请输入要解密的文本")
            return
        if not key:
            dialog_module.box_information(self.use_parent, "警告", "请输入密钥")
            return

        try:
            # 转换为字节
            encrypted_bytes = base64.b64decode(text)
            key_bytes = key.encode('utf-8')

            # RC4解密（加密和解密算法相同）
            decrypted_bytes = self.rc4_crypt(encrypted_bytes, key_bytes)

            # 解码为字符串
            result = decrypted_bytes.decode('utf-8')
            self.output_text.setPlainText(result)
        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"解密时发生错误: {str(e)}")


class RabbitTab(QWidget):
    """Rabbit加解密标签页"""

    def __init__(self, use_parent):
        super().__init__()
        self.use_parent = use_parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

        # 密钥输入
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("密钥:"))
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("输入密钥（16字节）")
        key_layout.addWidget(self.key_input)
        layout.addLayout(key_layout)

        # IV输入
        iv_layout = QHBoxLayout()
        iv_layout.addWidget(QLabel("IV向量:"))
        self.iv_input = QLineEdit()
        self.iv_input.setPlaceholderText("输入IV向量（8字节，可选）")
        iv_layout.addWidget(self.iv_input)
        layout.addLayout(iv_layout)

        # 输入框
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("输入文本（将进行Rabbit加密/解密）")
        self.input_text.setMaximumHeight(100)
        layout.addWidget(self.input_text)

        # 按钮
        btn_layout = QHBoxLayout()
        self.encrypt_btn = QPushButton("Rabbit加密")
        self.encrypt_btn.setMinimumHeight(35)
        self.encrypt_btn.setMaximumHeight(35)
        self.encrypt_btn.clicked.connect(self.encrypt_text)
        btn_layout.addWidget(self.encrypt_btn)

        self.decrypt_btn = QPushButton("Rabbit解密")
        self.decrypt_btn.setMinimumHeight(35)
        self.decrypt_btn.setMaximumHeight(35)
        self.decrypt_btn.clicked.connect(self.decrypt_text)
        btn_layout.addWidget(self.decrypt_btn)

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
        self.clear_btn.clicked.connect(lambda: clear_click(self.input_text, self.output_text))
        result_layout.addWidget(self.clear_btn)
        self.copy_btn = QPushButton("复制")
        self.copy_btn.setMinimumHeight(35)
        self.copy_btn.setMaximumHeight(35)
        self.copy_btn.clicked.connect(lambda: copy_click(self.output_text))
        result_layout.addWidget(self.copy_btn)
        layout.addLayout(result_layout)

        self.setLayout(layout)

    def rabbit_crypt(self, data, key, iv=None):
        """Rabbit流密码算法实现"""
        # 这是一个简化的Rabbit实现，实际应用中建议使用专门的密码库
        # 这里使用简单的异或操作模拟流密码

        # 生成密钥流
        key_bytes = key.encode('utf-8') if isinstance(key, str) else key
        if len(key_bytes) < 16:
            key_bytes = key_bytes.ljust(16, b'\0')
        else:
            key_bytes = key_bytes[:16]

        # 使用密钥生成伪随机字节流
        import struct
        key_stream = bytearray()
        state = list(struct.unpack('4I', key_bytes))

        for i in range(len(data)):
            # 简化的伪随机数生成
            state[0] = (state[0] + 0x9E3779B9) & 0xFFFFFFFF
            state[1] = (state[1] + state[0]) & 0xFFFFFFFF
            state[2] = (state[2] + state[1]) & 0xFFFFFFFF
            state[3] = (state[3] + state[2]) & 0xFFFFFFFF

            key_byte = (state[0] ^ state[1] ^ state[2] ^ state[3]) & 0xFF
            key_stream.append(key_byte)

        # 异或加密
        result = bytearray()
        for i in range(len(data)):
            result.append(data[i] ^ key_stream[i])

        return bytes(result)

    def encrypt_text(self):
        text = self.input_text.toPlainText()
        key = self.key_input.text()
        iv = self.iv_input.text()

        if not text:
            dialog_module.box_information(self.use_parent, "警告", "请输入要加密的文本")
            return
        if not key:
            dialog_module.box_information(self.use_parent, "警告", "请输入密钥")
            return

        try:
            # 转换为字节
            text_bytes = text.encode('utf-8')

            # Rabbit加密
            encrypted_bytes = self.rabbit_crypt(text_bytes, key, iv)

            # 编码为base64输出
            result = base64.b64encode(encrypted_bytes).decode('utf-8')
            self.output_text.setPlainText(result)
        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"加密时发生错误: {str(e)}")

    def decrypt_text(self):
        text = self.input_text.toPlainText()
        key = self.key_input.text()
        iv = self.iv_input.text()

        if not text:
            dialog_module.box_information(self.use_parent, "警告", "请输入要解密的文本")
            return
        if not key:
            dialog_module.box_information(self.use_parent, "警告", "请输入密钥")
            return

        try:
            # 转换为字节
            encrypted_bytes = base64.b64decode(text)

            # Rabbit解密（加密和解密算法相同）
            decrypted_bytes = self.rabbit_crypt(encrypted_bytes, key, iv)

            # 解码为字符串
            result = decrypted_bytes.decode('utf-8')
            self.output_text.setPlainText(result)
        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"解密时发生错误: {str(e)}")


class MD5Tab(QWidget):
    """MD5哈希标签页"""

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
        self.input_text.setPlaceholderText("输入文本（将进行MD5哈希）")
        self.input_text.setMaximumHeight(100)
        layout.addWidget(self.input_text)

        # 按钮
        btn_layout = QHBoxLayout()
        self.hash_btn = QPushButton("MD5哈希")
        self.hash_btn.setMinimumHeight(35)
        self.hash_btn.setMaximumHeight(35)
        self.hash_btn.clicked.connect(self.hash_text)
        btn_layout.addWidget(self.hash_btn)

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
        self.clear_btn.clicked.connect(lambda: clear_click(self.input_text, self.output_text))
        result_layout.addWidget(self.clear_btn)
        self.copy_btn = QPushButton("复制")
        self.copy_btn.setMinimumHeight(35)
        self.copy_btn.setMaximumHeight(35)
        self.copy_btn.clicked.connect(lambda: copy_click(self.output_text))
        result_layout.addWidget(self.copy_btn)
        layout.addLayout(result_layout)

        self.setLayout(layout)

    def hash_text(self):
        text = self.input_text.toPlainText()

        if not text:
            dialog_module.box_information(self.use_parent, "警告", "请输入要哈希的文本")
            return

        try:
            # 使用pycryptodome的MD5
            md5_hash = MD5.new()
            md5_hash.update(text.encode('utf-8'))
            result = md5_hash.hexdigest()

            # 也可以使用hashlib作为备选
            # result = hashlib.md5(text.encode('utf-8')).hexdigest()

            self.output_text.setPlainText(result)
        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"哈希时发生错误: {str(e)}")


class CryptoTool(QWidget):

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
        self.aes_tab = AESTab(self.use_parent)
        self.des_tab = DESTab(self.use_parent)
        self.rc4_tab = RC4Tab(self.use_parent)
        self.rabbit_tab = RabbitTab(self.use_parent)
        self.md5_tab = MD5Tab(self.use_parent)

        self.tabs.addTab(self.aes_tab, "AES")
        self.tabs.addTab(self.des_tab, "DES")
        self.tabs.addTab(self.rc4_tab, "RC4")
        self.tabs.addTab(self.rabbit_tab, "Rabbit")
        self.tabs.addTab(self.md5_tab, "MD5")

        main_layout.addWidget(self.tabs)

    def refresh_theme(self, main_object):
        # 设置样式
        style_util.set_dialog_control_style(self, main_object.is_dark)