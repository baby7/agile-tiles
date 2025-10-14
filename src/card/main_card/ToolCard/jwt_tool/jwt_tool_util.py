from PySide6.QtWidgets import QLabel, QLineEdit, QTextEdit, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
import json
import base64
import hmac
import hashlib
import time

from src.ui import style_util


class JWTEncoderDecoderPopup(QWidget):

    def __init__(self, parent=None, main_object=None, is_dark=None):
        super().__init__(parent=parent)
        # 初始化
        self.parent = parent
        self.use_parent = main_object
        self.updating = False  # 防止循环更新
        # 初始化界面
        self.init_ui()
        # 设置样式
        style_util.set_dialog_control_style(self, is_dark)

    def init_ui(self):
        # 主部件和布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(2)
        main_layout.setContentsMargins(5, 2, 5, 2)

        # Header部分
        header_label = QLabel("Header:")
        header_label.setStyleSheet("background: transparent;")
        main_layout.addWidget(header_label)

        self.header_input = QTextEdit()
        self.header_input.setPlaceholderText('输入Header JSON，例如：{"alg": "HS256", "typ": "JWT"}')
        # self.header_input.setMaximumHeight(80)
        main_layout.addWidget(self.header_input)

        # Payload部分
        payload_label = QLabel("Payload:")
        payload_label.setStyleSheet("background: transparent;")
        main_layout.addWidget(payload_label)

        self.payload_input = QTextEdit()
        self.payload_input.setPlaceholderText(
            '输入Payload JSON，例如：{"sub": "1234567890", "name": "John Doe", "iat": 1516239022}')
        # self.payload_input.setMaximumHeight(120)
        main_layout.addWidget(self.payload_input)

        # 密钥输入
        secret_label = QLabel("Secret Key:")
        secret_label.setStyleSheet("background: transparent;")
        main_layout.addWidget(secret_label)

        self.secret_input = QLineEdit()
        self.secret_input.setMinimumHeight(35)
        self.secret_input.setPlaceholderText("输入签名密钥")
        main_layout.addWidget(self.secret_input)

        # 按钮布局
        button_layout = QHBoxLayout()

        self.encode_btn = QPushButton("编码 JWT")
        self.encode_btn.setMinimumHeight(35)
        self.encode_btn.clicked.connect(self.encode_jwt)
        button_layout.addWidget(self.encode_btn)

        self.decode_btn = QPushButton("解码 JWT")
        self.decode_btn.setMinimumHeight(35)
        self.decode_btn.clicked.connect(self.decode_jwt)
        button_layout.addWidget(self.decode_btn)

        main_layout.addLayout(button_layout)

        # JWT Token显示
        token_label = QLabel("JWT Token:")
        token_label.setStyleSheet("background: transparent;")
        main_layout.addWidget(token_label)

        self.token_input = QTextEdit()
        self.token_input.setPlaceholderText("JWT Token将在这里显示")
        # self.token_input.setMaximumHeight(80)
        main_layout.addWidget(self.token_input)

        # 解码结果显示
        result_label = QLabel("解码结果:")
        result_label.setStyleSheet("background: transparent;")
        main_layout.addWidget(result_label)

        self.result_display = QTextEdit()
        self.result_display.setPlaceholderText("解码结果将在这里显示")
        # self.result_display.setMaximumHeight(120)
        self.result_display.setReadOnly(True)
        main_layout.addWidget(self.result_display)

        # 说明标签
        # note_label = QLabel("提示: 支持HS256算法，Header和Payload需要是有效的JSON格式")
        # note_label.setStyleSheet("font-size: 12px; color: #666; background: transparent;")
        # note_label.setAlignment(Qt.AlignCenter)
        # main_layout.addWidget(note_label)

    def base64url_encode(self, data: bytes) -> str:
        """Base64URL编码"""
        return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

    def base64url_decode(self, data: str) -> bytes:
        """Base64URL解码"""
        padding = 4 - (len(data) % 4)
        data = data + ('=' * padding)
        return base64.urlsafe_b64decode(data)

    def encode_jwt(self):
        """编码JWT"""
        try:
            # 获取输入数据
            header_text = self.header_input.toPlainText().strip() or '{"alg": "HS256", "typ": "JWT"}'
            payload_text = self.payload_input.toPlainText().strip()
            secret = self.secret_input.text().strip()

            if not payload_text:
                self.result_display.setPlainText("错误: Payload不能为空")
                return

            # 解析JSON
            header = json.loads(header_text)
            payload = json.loads(payload_text)

            # 编码Header和Payload
            header_encoded = self.base64url_encode(json.dumps(header, separators=(',', ':')).encode('utf-8'))
            payload_encoded = self.base64url_encode(json.dumps(payload, separators=(',', ':')).encode('utf-8'))

            # 生成签名
            message = f"{header_encoded}.{payload_encoded}".encode('utf-8')

            if header.get('alg') == 'HS256':
                signature = hmac.new(
                    secret.encode('utf-8'),
                    message,
                    hashlib.sha256
                ).digest()
            else:
                # 默认使用HS256
                signature = hmac.new(
                    secret.encode('utf-8'),
                    message,
                    hashlib.sha256
                ).digest()

            signature_encoded = self.base64url_encode(signature)

            # 生成完整的JWT
            jwt_token = f"{header_encoded}.{payload_encoded}.{signature_encoded}"
            self.token_input.setPlainText(jwt_token)
            self.result_display.setPlainText("JWT编码成功!")

        except json.JSONDecodeError as e:
            self.result_display.setPlainText(f"JSON解析错误: {str(e)}")
        except Exception as e:
            self.result_display.setPlainText(f"编码错误: {str(e)}")

    def decode_jwt(self):
        """解码JWT"""
        try:
            jwt_token = self.token_input.toPlainText().strip()
            secret = self.secret_input.text().strip()

            if not jwt_token:
                self.result_display.setPlainText("错误: JWT Token不能为空")
                return

            # 分割JWT
            parts = jwt_token.split('.')
            if len(parts) != 3:
                self.result_display.setPlainText("错误: 无效的JWT格式")
                return

            header_encoded, payload_encoded, signature_encoded = parts

            # 解码Header和Payload
            header_json = self.base64url_decode(header_encoded).decode('utf-8')
            payload_json = self.base64url_decode(payload_encoded).decode('utf-8')

            header = json.loads(header_json)
            payload = json.loads(payload_json)

            # 验证签名
            message = f"{header_encoded}.{payload_encoded}".encode('utf-8')
            expected_signature = self.base64url_encode(
                hmac.new(
                    secret.encode('utf-8'),
                    message,
                    hashlib.sha256
                ).digest()
            )

            signature_valid = hmac.compare_digest(signature_encoded, expected_signature)

            # 格式化结果显示
            result = {
                "header": header,
                "payload": payload,
                "signature_valid": signature_valid
            }

            # 检查过期时间
            current_time = time.time()
            if 'exp' in payload and payload['exp'] < current_time:
                result['expired'] = True
                result['expired_at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(payload['exp']))
            else:
                result['expired'] = False

            self.result_display.setPlainText(json.dumps(result, indent=2, ensure_ascii=False))

        except json.JSONDecodeError as e:
            self.result_display.setPlainText(f"JSON解析错误: {str(e)}")
        except Exception as e:
            self.result_display.setPlainText(f"解码错误: {str(e)}")

    def refresh_theme(self, main_object):
        # 设置样式
        style_util.set_dialog_control_style(self, main_object.is_dark)
