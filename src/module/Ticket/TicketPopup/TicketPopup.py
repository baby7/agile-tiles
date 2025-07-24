import os
import json
import mimetypes
from PySide6.QtGui import Qt, QFont, QPixmap, QPainter, QBrush, QColor
from PySide6.QtCore import Qt, Signal, QRect, Slot, QUrl, QFile, QByteArray
from PySide6.QtWidgets import (
    QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QTextEdit, QPushButton,
    QScrollArea, QFrame, QWidget, QFileDialog, QProgressBar
)
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply, QHttpMultiPart, QHttpPart

from src.client import common
from src.component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
from src.component.ImagePreviewWidget.ImagePreviewWidget import ImagePreviewWidget
from src.module.Box import message_box_util


class TicketPopup(AgileTilesAcrylicWindow):
    """工单创建/回复弹窗"""
    setPixmapSignal = Signal(QPixmap)
    # 添加调试模式常量
    DEBUG_MODE = False  # 设为True时显示支付状态标签
    ticket_reply = None
    file_ids = []

    def __init__(self, parent=None, use_parent=None, title=None, screen=None, current_user=None,
                 mode="create", ticket_id=None, ticket_title=None):
        """
        初始化工单弹窗

        :param mode: "create" - 创建新工单, "reply" - 回复工单
        :param ticket_id: 回复工单时的工单ID
        :param ticket_title: 回复工单时的工单标题（用于显示）
        """
        super().__init__(parent=parent, is_dark=use_parent.is_dark, form_theme_mode=use_parent.form_theme_mode,
                         form_theme_transparency=use_parent.form_theme_transparency)
        self.use_parent = use_parent
        # 参数初始化
        self.is_closed = False  # 添加关闭状态标志
        self.screen = screen  # 屏幕对象
        # 用户数据
        self.current_user = current_user  # 用户数据
        # 网络管理器
        self.upload_manager = QNetworkAccessManager(self)  # 用于图片上传
        self.ticket_manager = QNetworkAccessManager(self)  # 用于反馈提交
        # 当前上传请求
        self.current_upload = None
        self.current_file_path = None

        # 工单模式
        self.mode = mode
        self.ticket_id = ticket_id

        try:
            self.setWindowTitle(title if title else ("新建工单" if mode == "create" else "回复工单"))
            self.setMinimumWidth(700)  # 增加最小宽度以适应新布局
            self.setMinimumHeight(850)
            # 初始化界面
            self.init_ui(ticket_title)
        except Exception as e:
            print(e)
        self.showMaximized()

    def init_ui(self, ticket_title=None):
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        self.widget_base.setLayout(main_layout)

        # 根据主题设置颜色变量
        if self.is_dark:
            bg_color = "#2D2D30"  # 深色背景
            text_color = "#CCCCCC"  # 浅色文字
            border_color = "#555555"  # 深色边框
            hover_color = "#3C3C3F"  # 深色悬停
            button_bg = "#007ACC"  # 深色按钮
            button_hover = "#0062A3"  # 深色按钮悬停
        else:
            bg_color = "#FFFFFF"  # 浅色背景
            text_color = "#606266"  # 深色文字
            border_color = "#DCDFE6"  # 浅色边框
            hover_color = "#ECF5FF"  # 浅色悬停
            button_bg = "#409EFF"  # 浅色按钮
            button_hover = "#66B1FF"  # 浅色按钮悬停

        # 表单容器
        form_container = QFrame()
        form_container.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border-radius: 8px;
                padding: 20px;
            }}
        """)
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(10)

        # 标题输入 - 在回复模式下只显示标题
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)

        if self.mode == "reply":
            # 回复模式：显示工单标题（只读）
            title_label = QLabel("工单标题")
            title_label.setFont(QFont("Microsoft YaHei", 10))
            title_label.setStyleSheet(f"color: {text_color};")

            self.title_display = QLabel(ticket_title if ticket_title else "")
            self.title_display.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
            self.title_display.setStyleSheet(
                f"color: {text_color}; padding: 5px; border: 1px solid {border_color}; border-radius: 4px;")
            self.title_display.setWordWrap(True)

            title_layout.addWidget(title_label)
            title_layout.addWidget(self.title_display)
        else:
            # 创建模式：可编辑的标题输入框
            title_label = QLabel("* 标题")
            title_label.setFont(QFont("Microsoft YaHei", 10))
            title_label.setStyleSheet(f"color: {text_color};")

            self.title_input = QLineEdit()
            self.title_input.setFont(QFont("Microsoft YaHei", 10))
            self.title_input.setPlaceholderText("请输入工单标题（50字以内）")
            self.title_input.setStyleSheet(f"""
                QLineEdit {{
                    height: 40px;
                    border: 1px solid {border_color};
                    border-radius: 4px;
                    padding: 0 10px;
                    background-color: {bg_color};
                    color: {text_color};
                }}
                QLineEdit:focus {{
                    border: 1px solid {button_bg};
                }}
            """)
            self.title_input.setMaxLength(50)

            title_layout.addWidget(title_label)
            title_layout.addWidget(self.title_input)

        form_layout.addLayout(title_layout)

        # 内容输入
        content_layout = QVBoxLayout()
        content_layout.setSpacing(4)

        content_label_text = "* 内容" if self.mode == "create" else "* 回复内容"
        content_label = QLabel(content_label_text)
        content_label.setFont(QFont("Microsoft YaHei", 10))
        content_label.setStyleSheet(f"color: {text_color};")

        placeholder_text = "请详细描述您的问题或建议（1000字以内）" if self.mode == "create" else "请输入您的回复内容（1000字以内）"
        self.content_input = QTextEdit()
        self.content_input.setFont(QFont("Microsoft YaHei", 10))
        self.content_input.setPlaceholderText(placeholder_text)
        self.content_input.setStyleSheet(f"""
            QTextEdit {{
                border: 1px solid {border_color};
                border-radius: 4px;
                padding: 10px;
                background-color: {bg_color};
                color: {text_color};
            }}
            QTextEdit:focus {{
                border: 1px solid {button_bg};
            }}
        """)
        self.content_input.setMinimumHeight(130)
        # 添加长度限制信号连接
        self.content_input.textChanged.connect(self.limit_content_length)

        content_layout.addWidget(content_label)
        content_layout.addWidget(self.content_input)
        form_layout.addLayout(content_layout)

        # 图片上传区域
        image_layout = QVBoxLayout()
        image_layout.setSpacing(4)
        image_label = QLabel("图片")
        image_label.setFont(QFont("Microsoft YaHei", 10))
        image_label.setStyleSheet("color: #606266; background-color: transparent;")
        image_layout.addWidget(image_label)

        # 图片上传容器
        self.image_container = QWidget()
        self.image_container.setStyleSheet("border: none; background-color: transparent;")
        self.image_container_layout = QHBoxLayout(self.image_container)
        self.image_container_layout.setContentsMargins(0, 0, 0, 0)
        self.image_container_layout.setSpacing(10)

        # 上传按钮
        self.upload_button = QPushButton()
        self.upload_button.setFixedSize(100, 100)
        self.upload_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                border: 1px dashed {border_color};
                border-radius: 6px;
            }}
            QPushButton:hover {{
                border-color: {button_bg};
                background-color: {hover_color};
            }}
        """)

        # 创建上传按钮内部的加号
        upload_icon = QLabel(self.upload_button)
        upload_icon.setAlignment(Qt.AlignCenter)
        upload_icon.setStyleSheet("font-size: 30px; color: #8c939d;")
        upload_icon.setText("+")
        upload_icon.setGeometry(0, 0, 100, 100)

        self.upload_button.clicked.connect(self.upload_image)
        self.image_container_layout.addWidget(self.upload_button)

        # 滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("border: 1px solid #DCDFE6;")
        scroll_area.setWidget(self.image_container)

        image_layout.addWidget(scroll_area)
        form_layout.addLayout(image_layout)

        # 添加提示标签
        hint_label = QLabel("最多可上传5张图片（支持JPG、PNG、BMP格式）")
        hint_label.setFont(QFont("Microsoft YaHei", 8))
        hint_label.setStyleSheet(f"color: {text_color};")

        image_layout.addWidget(scroll_area)
        image_layout.addWidget(hint_label)
        form_layout.addLayout(image_layout)

        # 进度条容器
        self.progress_container = QWidget()
        self.progress_container.setVisible(False)
        progress_layout = QVBoxLayout(self.progress_container)
        progress_layout.setContentsMargins(0, 10, 0, 0)
        progress_layout.setSpacing(5)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                height: 20px;
                border-radius: 10px;
                background-color: #ebeef5;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #409EFF;
                border-radius: 10px;
            }
        """)

        # 提交按钮
        submit_text = "提交工单" if self.mode == "create" else "提交回复"
        submit_button = QPushButton(submit_text)
        submit_button.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        submit_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {button_bg};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 12px 20px;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: {button_hover};
            }}
            QPushButton:pressed {{
                background-color: {button_bg};
            }}
        """)
        submit_button.clicked.connect(self.submit_ticket if self.mode == "create" else self.submit_reply)

        form_layout.addWidget(submit_button, alignment=Qt.AlignRight)
        main_layout.addWidget(form_container)

        # 存储图片信息
        self.images = []
        # 当前上传线程
        self.upload_thread = None

        # 设置输入焦点
        self.title_input.setFocus()
        # 添加编辑界面回车跳转（焦点移到下一个输入框）
        self.title_input.returnPressed.connect(
            lambda: self.content_input.setFocus()
        )

    # 新增长度限制方法
    def limit_content_length(self):
        """限制内容输入框长度为1000字符"""
        content = self.content_input.toPlainText()
        if len(content) > 1000:
            cursor = self.content_input.textCursor()
            position = cursor.position()
            self.content_input.blockSignals(True)  # 防止递归触发
            self.content_input.setPlainText(content[:1000])
            cursor.setPosition(min(position, 1000))
            self.content_input.setTextCursor(cursor)
            self.content_input.blockSignals(False)

    def create_icon(self):
        """创建应用图标"""
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor("#409EFF")))
        painter.drawEllipse(0, 0, 32, 32)
        painter.setPen(QColor(Qt.white))
        painter.setFont(QFont("Arial", 16))
        painter.drawText(QRect(0, 0, 32, 32), Qt.AlignCenter, "T")
        painter.end()
        return pixmap

    def upload_image(self):
        """上传图片"""
        if len(self.images) >= 5:
            message_box_util.box_acknowledgement(self.use_parent, "提示", "最多只能上传5张图片")
            return

        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp)")
        if not file_dialog.exec():
            return
        selected_files = file_dialog.selectedFiles()
        if not selected_files:
            return
        # 检查文件大小（5MB限制）
        MAX_SIZE = 5 * 1024 * 1024  # 5MB
        file_path = selected_files[0]
        file_size = os.path.getsize(file_path)

        if file_size > MAX_SIZE:
            message_box_util.box_acknowledgement(
                self.use_parent,
                "文件过大",
                f"图片大小不能超过5MB (当前: {file_size // 1024}KB)"
            )
            return

        # 显示进度条
        self.progress_container.setVisible(True)
        self.progress_bar.setValue(0)

        # 使用QNetworkRequest上传图片
        self.upload_file_with_qnetwork(file_path)

    def upload_file_with_qnetwork(self, file_path):
        """使用QNetworkRequest上传文件"""
        # 获取文件类型
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = 'application/octet-stream'

        # 准备文件
        file_name = os.path.basename(file_path)
        file = QFile(file_path)
        if not file.open(QFile.ReadOnly):
            message_box_util.box_acknowledgement(self.use_parent, "错误", f"无法打开文件: {file_path}")
            return

        # 保存当前上传文件路径
        self.current_file_path = file_path

        # 创建多部分请求
        multi_part = QHttpMultiPart(QHttpMultiPart.FormDataType)

        # 添加文件部分
        file_part = QHttpPart()
        file_part.setHeader(QNetworkRequest.ContentTypeHeader, mime_type)
        file_part.setHeader(QNetworkRequest.ContentDispositionHeader,
                            f'form-data; name="file"; filename="{file_name}"')
        file_part.setBodyDevice(file)
        file.setParent(multi_part)  # 确保文件在multi_part销毁时关闭
        multi_part.append(file_part)

        # 创建请求
        if self.mode == "create":
            url = QUrl(f"{common.BASE_URL}/file/ticket/save")
        else:
            url = QUrl(f"{common.BASE_URL}/file/ticketResponse/save")
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.use_parent.token.encode())

        # 发送请求
        self.current_upload = self.upload_manager.post(request, multi_part)
        multi_part.setParent(self.current_upload)  # 确保multi_part在请求完成后被删除

        # 连接进度信号
        self.current_upload.uploadProgress.connect(self.update_upload_progress)
        self.current_upload.finished.connect(lambda: self.handle_upload_finished(self.current_upload))

    @Slot(int, int)
    def update_upload_progress(self, bytes_sent, bytes_total):
        """更新上传进度"""
        if bytes_total > 0:
            progress = int((bytes_sent / bytes_total) * 100)
            self.progress_bar.setValue(progress)

    @Slot(QNetworkReply)
    def handle_upload_finished(self, reply):
        """处理上传完成"""
        # 检查是否有错误
        if reply.error() != QNetworkReply.NoError:
            error_str = reply.errorString()
            message_box_util.box_acknowledgement(self.use_parent, "上传失败", f"图片上传失败: {error_str}")
            self.progress_container.setVisible(False)
            return

        # 解析响应
        response_data = reply.readAll().data()
        try:
            result = json.loads(response_data.decode('utf-8'))
            if str(result.get('code')) == "0":
                file_id = result["data"]["id"]  # 获取文件ID
                self.file_ids.append(file_id)  # 添加到文件ID列表
                image_info = {
                    'local_path': self.current_file_path,
                    'file_id': file_id,  # 存储文件ID
                    'remote_url': result["data"]["url"],
                    'file_name': os.path.basename(self.current_file_path)
                }
                self.images.append(image_info)
                self.add_image_preview(image_info)

                # 检查是否达到上限
                if len(self.images) >= 5:
                    self.upload_button.hide()
            else:
                message_box_util.box_acknowledgement(self.use_parent, "上传失败", result.get('message', '上传失败'))
        except Exception as e:
            message_box_util.box_acknowledgement(self.use_parent, "解析错误", f"响应解析失败: {str(e)}")

        # 隐藏进度条
        self.progress_container.setVisible(False)
        self.current_upload = None
        self.current_file_path = None

    def add_image_preview(self, image_info):
        """添加图片预览"""
        # 创建预览小部件
        preview = ImagePreviewWidget(image_info["local_path"])
        # 添加image_info属性到预览部件
        preview.image_info = image_info
        preview.deleteClicked.connect(lambda: self.remove_image(image_info))

        # 添加到布局
        self.image_container_layout.insertWidget(self.image_container_layout.count() - 1, preview)

    def remove_image(self, image_info):
        """移除图片"""
        if image_info in self.images:
            # 从图片列表和文件ID列表中移除
            self.images.remove(image_info)
            if 'file_id' in image_info:  # 确保有file_id字段
                try:
                    # 从文件ID列表中移除对应的ID
                    self.file_ids.remove(image_info['file_id'])
                except ValueError:  # 如果ID不存在则忽略
                    pass

            # 重新构建图片预览区域
            for i in reversed(range(self.image_container_layout.count())):
                widget = self.image_container_layout.itemAt(i).widget()
                # 检查是否是图片预览部件（排除上传按钮）
                if widget and hasattr(widget, 'image_info') and widget.image_info == image_info:
                    self.image_container_layout.removeWidget(widget)
                    widget.deleteLater()
                    break

            # 显示上传按钮（如果之前被隐藏）
            if len(self.images) < 5 and self.upload_button.isHidden():
                self.upload_button.show()

    def submit_ticket(self):
        """提交工单"""
        title = self.title_input.text().strip()
        content = self.content_input.toPlainText().strip()

        # 验证输入
        if not title:
            self.show_error("标题不能为空")
            return
        if len(title) > 50:
            self.show_error("标题长度不能超过50字")
            return
        if not content:
            self.show_error("内容不能为空")
            return
        if len(content) > 1000:
            self.show_error("内容长度不能超过1000字")
            return

        # 准备数据
        ticket_data = {
            "title": title,
            "content": content,
            "fileIds": self.file_ids
        }

        # 使用 QNetworkRequest 提交工单
        url = QUrl(common.BASE_URL + "/tickets")
        request = QNetworkRequest(url)
        request.setRawHeader(b"Content-Type", b"application/json")
        request.setRawHeader(b"Authorization", self.use_parent.token.encode())

        # 将 JSON 数据转换为 QByteArray
        json_data = QByteArray(json.dumps(ticket_data).encode('utf-8'))

        # 发送网络请求
        ticket_reply = self.ticket_manager.post(request, json_data)
        ticket_reply.finished.connect(lambda: self.handle_ticket_response(ticket_reply))

    def submit_reply(self):
        """提交工单回复"""
        content = self.content_input.toPlainText().strip()

        # 验证输入
        if not content:
            self.show_error("回复内容不能为空")
            return
        if len(content) > 1000:
            self.show_error("回复内容长度不能超过1000字")
            return

        # 准备数据
        reply_data = {
            "content": content,
            "fileIds": self.file_ids
        }

        # 使用 QNetworkRequest 提交回复
        url = QUrl(common.BASE_URL + f"/tickets/{self.ticket_id}/responses")
        request = QNetworkRequest(url)
        request.setRawHeader(b"Content-Type", b"application/json")
        request.setRawHeader(b"Authorization", self.use_parent.token.encode())

        # 将 JSON 数据转换为 QByteArray
        json_data = QByteArray(json.dumps(reply_data).encode('utf-8'))

        # 发送网络请求
        reply_reply = self.ticket_manager.post(request, json_data)
        reply_reply.finished.connect(lambda: self.handle_reply_response(reply_reply))

    def handle_ticket_response(self, reply):
        """处理工单提交的响应"""
        try:
            # 获取响应
            if reply.error() == QNetworkReply.NoError:
                # 解析 JSON 响应
                data = reply.readAll().data()
                if data is None or data == b'':
                    message_box_util.box_acknowledgement(self.use_parent, "提交失败", "请稍后重试")
                else:
                    response_data = json.loads(data.decode('utf-8'))
                    if "code" in response_data and response_data.get('code') == 0:
                        message_box_util.box_acknowledgement(self.use_parent, "提交成功", "您的工单已成功提交！")
                        self.reset_form()
                    else:
                        error_msg = response_data.get("message", "未知错误，请稍后重试")
                        message_box_util.box_acknowledgement(self.use_parent, "提交失败", error_msg)
            else:
                message_box_util.box_acknowledgement(self.use_parent, "提交失败", f"网络错误: {reply.errorString()}")
        except Exception as e:
            message_box_util.box_acknowledgement(self.use_parent, "处理错误", f"响应处理失败: {str(e)}")
        finally:
            reply.deleteLater()
            self.ticket_reply = None  # 清除引用

    def handle_reply_response(self, reply):
        """处理回复提交的响应"""
        try:
            # 获取响应
            if reply.error() == QNetworkReply.NoError:
                # 解析 JSON 响应
                data = reply.readAll().data()
                if data is None or data == b'':
                    message_box_util.box_acknowledgement(self.use_parent, "提交失败", "请稍后重试")
                else:
                    response_data = json.loads(data.decode('utf-8'))
                    if "code" in response_data and response_data.get('code') == 0:
                        message_box_util.box_acknowledgement(self.use_parent, "提交成功", "您的回复已成功提交！")
                        self.reset_form()
                    else:
                        error_msg = response_data.get("message", "未知错误，请稍后重试")
                        message_box_util.box_acknowledgement(self.use_parent, "提交失败", error_msg)
            else:
                message_box_util.box_acknowledgement(self.use_parent, "提交失败", f"网络错误: {reply.errorString()}")
        except Exception as e:
            message_box_util.box_acknowledgement(self.use_parent, "处理错误", f"响应处理失败: {str(e)}")
        finally:
            reply.deleteLater()
            self.ticket_reply = None  # 清除引用

    def show_error(self, message):
        """显示错误提示"""
        message_box_util.box_acknowledgement(self.use_parent, "输入错误", message)

    def reset_form(self):
        """重置表单"""
        if hasattr(self, 'title_input'):
            self.title_input.clear()
        self.content_input.clear()
        self.images = []

        # 移除所有图片预览
        for i in reversed(range(self.image_container_layout.count())):
            widget = self.image_container_layout.itemAt(i).widget()
            if widget != self.upload_button:
                self.image_container_layout.removeWidget(widget)
                widget.deleteLater()

        # 确保上传按钮可见
        if self.upload_button.isHidden():
            self.upload_button.show()

    def closeEvent(self, event):
        # 标记窗口已关闭
        self.is_closed = True
        # 取消图片上传
        if self.current_upload and self.current_upload.isRunning():
            self.current_upload.abort()
        # 取消反馈提交
        if hasattr(self, 'ticket_reply') and self.ticket_reply and self.ticket_reply.isRunning():
            self.ticket_reply.abort()
        super().closeEvent(event)