import os
import subprocess
import webbrowser
from urllib.parse import unquote, quote
from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QFont, QTextCursor, QTextOption
from PySide6.QtWidgets import (QLabel, QPushButton, QLineEdit, QTextBrowser,
                               QWidget, QStackedWidget, QVBoxLayout, QHBoxLayout,
                               QSizePolicy)
from src.card.MainCardManager.MainCard import MainCard
from src.thread_list.everything_search_thread import EverythingStatusThread, EverythingSearchThread
from src.ui import style_util
from src.component.LoadAnimation.LoadAnimation import LoadAnimation

file_type_map_list = [
    # 音频
    {
        "type": "audio",
        "icon": "Office/audio-file",
        "suffixList": ["mp3", "flac", "wav", "wma", "aac", "ogg", "ape"]
    },
    # 视频
    {
        "type": "video",
        "icon": "Office/video-file",
        "suffixList": ["mp4", "avi", "mkv", "mov", "webm", "wmv"]
    },
    # 图片
    {
        "type": "image",
        "icon": "Office/image-files",
        "suffixList": ["jpg", "jpeg", "jpe", "jfif", "png", "bmp", "gif", "ico", "svg"]
    },
    # excel表格
    {
        "type": "excel",
        "icon": "Office/file-excel",
        "suffixList": ["xlsx", "xls"]
    },
    # pdf
    {
        "type": "pdf",
        "icon": "Office/file-pdf-one",
        "suffixList": ["pdf"]
    },
    # ppt
    {
        "type": "ppt",
        "icon": "Office/file-ppt",
        "suffixList": ["ppt", "pptx"]
    },
    # word
    {
        "type": "word",
        "icon": "Office/file-word",
        "suffixList": ["word", "doc", "docx"]
    },
    # 文本文件
    {
        "type": "txt",
        "icon": "Office/file-txt-one",
        "suffixList": ["txt", "md"]
    },
    # 压缩文件
    {
        "type": "zip",
        "icon": "Office/file-zip",
        "suffixList": ["zip", "7z", "rar", "gzip", "gz"]
    },
    # 代码文件
    {
        "type": "code",
        "icon": "Office/file-code",
        "suffixList": ["py", "pyc", "pyo", "pyd", "java", "class", "h", "c", "hpp", "cpp", "cs", "php",
                       "html", "js", "css", "kt", "pl", "pm", "shell", "sh", "vue", "xml", "yml"]
    },
    # exe文件
    {
        "type": "exe",
        "icon": "Abstract/ad-product",
        "suffixList": ["exe"]
    },
]


class FileSearchCard(MainCard):
    """文件搜索卡片"""

    title = "文件搜索"
    name = "FileSearchCard"
    support_size_list = ["Big"]

    # 只读参数
    x = None
    y = None
    size = None
    theme = None
    width = 0
    height = 0
    fillet_corner = 0

    # 可使用
    card = None
    data = None
    toolkit = None
    logger = None

    # 可调用
    save_data_func = None

    # 搜索相关
    status_thread = None
    search_thread = None
    is_indexing = False
    current_search_text = ""
    current_offset = 0
    has_more_results = False
    total_results = 0
    displayed_results = 0
    everything_path = None  # Everything安装路径
    is_ready = False  # Everything是否就绪
    load_ok = False

    def __init__(self, main_object=None, parent=None, theme=None, card=None, cache=None, data=None,
                 toolkit=None, logger=None, save_data_func=None):
        super().__init__(main_object=main_object, parent=parent, theme=theme, card=card, cache=cache, data=data,
                         toolkit=toolkit, logger=logger, save_data_func=save_data_func)
        self.everything_path = "./static/thirdparty/everything/"

        # 图标路径
        self.file_icon_path = "Base/save"
        self.folder_icon_path = "Office/folder-open"
        # 图标对应路径
        self.suffix_icon_map = {
            "file": self.file_icon_path,
            "folder": self.folder_icon_path
        }
        # 图标对应路径
        for item in file_type_map_list:
            item_suffix_list = item["suffixList"]
            for suffix in item_suffix_list:
                self.suffix_icon_map[suffix] = item["icon"]

    def clear(self):
        """清理资源"""
        try:
            # 停止everything
            self.shutdown_everything()
            # 停止状态线程
            try:
                if self.status_thread and self.status_thread.isRunning():
                    self.status_thread.stop()
            except Exception as e:
                print(e)
            # 停止搜索线程
            try:
                if self.search_thread and self.search_thread.isRunning():
                    self.search_thread.stop()
            except Exception as e:
                print(e)
            # 清理UI元素
            self.line_edit_search.setVisible(False)
            self.line_edit_search.deleteLater()
            self.push_button_search.setVisible(False)
            self.push_button_search.deleteLater()
            self.text_browser_results.setVisible(False)
            self.text_browser_results.deleteLater()
            self.label_status.setVisible(False)
            self.label_status.deleteLater()
            self.label_indexing.setVisible(False)
            self.label_indexing.deleteLater()
            self.label_ready_status.setVisible(False)
            self.label_ready_status.deleteLater()
            self.load_animation.setVisible(False)
            self.load_animation.deleteLater()
            self.label_loading_more.setVisible(False)
            self.label_loading_more.deleteLater()
        except Exception as e:
            print(e)
        super().clear()

    def shutdown_everything(self):
        """
        关闭由本程序启动的Everything实例
        """
        try:
            # 如果有搜索器实例且启动了Everything进程，则关闭它
            if (hasattr(self, 'search_thread') and
                    self.search_thread and
                    hasattr(self.search_thread.searcher, 'everything_process') and
                    self.search_thread.searcher.everything_process):

                process = self.search_thread.searcher.everything_process
                if process.poll() is None:  # 检查进程是否仍在运行
                    process.terminate()  # 终止进程
                    try:
                        process.wait(timeout=3)  # 等待最多3秒
                    except subprocess.TimeoutExpired:
                        process.kill()  # 如果未能正常终止，则强制杀死进程

            # 同样检查状态线程中的搜索器
            if (hasattr(self, 'status_thread') and
                    self.status_thread and
                    hasattr(self.status_thread, 'searcher') and
                    self.status_thread.searcher and
                    hasattr(self.status_thread.searcher, 'everything_process') and
                    self.status_thread.searcher.everything_process):

                process = self.status_thread.searcher.everything_process
                if process.poll() is None:  # 检查进程是否仍在运行
                    process.terminate()
                    try:
                        process.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        process.kill()

        except Exception as e:
            self.logger.card_error("文件搜索", f"关闭Everything时出错: {str(e)}")

    def init_ui(self):
        """初始化UI"""
        super().init_ui()

        # 创建堆叠窗口
        self.stacked_widget = QStackedWidget(self.card)
        self.stacked_widget.setStyleSheet("background-color: transparent; border: none;")
        self.stacked_widget.setGeometry(QRect(0, 0, self.card.width(), self.card.height()))

        # 创建主界面
        self.main_widget = QWidget()
        self.main_widget.setStyleSheet("background-color: transparent; border: none;")
        self.init_main_ui()
        self.stacked_widget.addWidget(self.main_widget)

        # 创建遮罩层
        self.mask_widget = QWidget()
        self.init_mask_ui()
        self.stacked_widget.addWidget(self.mask_widget)

        # 初始显示遮罩层
        self.stacked_widget.setCurrentIndex(1)

    def init_main_ui(self):
        """初始化主界面UI"""
        # 字体设置
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)

        font2 = QFont()
        font2.setPointSize(9)

        # 创建主布局
        main_layout = QVBoxLayout(self.main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)
        # 标题
        title = QLabel("本地文件搜索")
        title.setStyleSheet("background-color: transparent; border: none;")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # 搜索行布局
        search_layout = QHBoxLayout()
        search_layout.setSpacing(5)

        # 搜索输入框
        self.line_edit_search = QLineEdit()
        self.line_edit_search.setObjectName(u"line_edit_search")
        self.line_edit_search.setFont(font1)
        self.line_edit_search.setPlaceholderText("输入搜索本地文件/文件夹的关键词...")
        self.line_edit_search.setMinimumHeight(25)
        self.line_edit_search.returnPressed.connect(self.start_search)
        search_layout.addWidget(self.line_edit_search)

        # 清理按钮
        self.push_button_clean = QPushButton()
        self.push_button_clean.setObjectName(u"push_button_clean")
        self.push_button_clean.setText("清空")
        self.push_button_clean.setMinimumHeight(25)
        self.push_button_clean.setMinimumWidth(60)
        self.push_button_clean.clicked.connect(self.start_clean)
        search_layout.addWidget(self.push_button_clean)

        # 搜索按钮
        self.push_button_search = QPushButton()
        self.push_button_search.setObjectName(u"push_button_search")
        self.push_button_search.setText("搜索")
        self.push_button_search.setMinimumHeight(25)
        self.push_button_search.setMinimumWidth(60)
        self.push_button_search.clicked.connect(self.start_search)
        search_layout.addWidget(self.push_button_search)

        main_layout.addLayout(search_layout)

        # 状态信息布局
        status_layout = QVBoxLayout()
        status_layout.setSpacing(5)

        # 就绪状态标签
        self.label_ready_status = QLabel()
        self.label_ready_status.setObjectName(u"label_ready_status")
        self.label_ready_status.setFont(font2)
        self.label_ready_status.setStyleSheet("background: transparent;")
        self.label_ready_status.setText("正在检查Everything状态...")
        status_layout.addWidget(self.label_ready_status)

        # 搜索状态标签
        self.label_status = QLabel()
        self.label_status.setObjectName(u"label_status")
        self.label_status.setFont(font2)
        self.label_status.setStyleSheet("background: transparent;")
        self.label_status.setText("准备搜索本地文件/文件夹...")
        status_layout.addWidget(self.label_status)

        # 索引状态标签
        self.label_indexing = QLabel()
        self.label_indexing.setObjectName(u"label_indexing")
        self.label_indexing.setFont(font2)
        self.label_indexing.setText("")
        self.label_indexing.setStyleSheet("background: transparent;")
        self.label_indexing.hide()
        status_layout.addWidget(self.label_indexing)

        main_layout.addLayout(status_layout)

        # 结果显示区域
        self.text_browser_results = QTextBrowser()
        self.text_browser_results.setObjectName(u"text_browser_results")
        self.text_browser_results.setFont(font1)
        self.text_browser_results.setOpenLinks(False)
        self.text_browser_results.setWordWrapMode(QTextOption.WrapMode.WrapAnywhere)        # 禁用智能换行改为按照宽度换行
        self.text_browser_results.anchorClicked.connect(self.on_result_clicked)
        self.text_browser_results.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.text_browser_results)

        # 加载更多提示标签
        self.label_loading_more = QLabel()
        self.label_loading_more.setObjectName(u"label_loading_more")
        self.label_loading_more.setFont(font2)
        self.label_loading_more.setAlignment(Qt.AlignCenter)
        self.label_loading_more.setText("滚动加载更多结果...")
        self.label_loading_more.hide()
        main_layout.addWidget(self.label_loading_more)

        # 加载动画 - 使用覆盖层方式
        self.load_animation = LoadAnimation(self.main_widget, self.theme)
        self.load_animation.setStyleSheet("background:transparent;border: 0px solid gray;")
        self.load_animation.setFixedSize(60, 60)
        self.load_animation.hide()

        # 连接滚动条信号
        scroll_bar = self.text_browser_results.verticalScrollBar()
        scroll_bar.valueChanged.connect(self.on_scroll)

        # 设置样式
        self.refresh_theme()

    def init_mask_ui(self):
        """初始化遮罩层UI"""
        # 设置遮罩层样式
        self.mask_widget.setStyleSheet("background: transparent;")

        # 创建垂直布局
        layout = QVBoxLayout(self.mask_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        # 加载动画
        self.mask_animation = LoadAnimation(self.mask_widget, self.theme)
        self.mask_animation.setStyleSheet("background: transparent;")
        self.mask_animation.setFixedSize(60, 60)
        layout.addWidget(self.mask_animation, 0, Qt.AlignCenter)

        # 加载状态文字
        self.mask_label = QLabel("正在启动Everything搜索服务...")
        self.mask_label.setStyleSheet("background: transparent; font-size: 14px;")
        self.mask_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.mask_label)

        # 提示文字
        tip_text = '您可以下载 <a href="https://www.voidtools.com/zh-cn/downloads/" style="color: #4fc3f7; text-decoration: none;">Everything安装包</a> 安装并设置开机自启动，这样可以跳过每次开机后的重新索引'
        self.tip_label = QLabel(tip_text)
        self.tip_label.setStyleSheet("background: transparent; font-size: 12px;")
        self.tip_label.setAlignment(Qt.AlignCenter)
        self.tip_label.setOpenExternalLinks(False)
        self.tip_label.setWordWrap(True)
        self.tip_label.linkActivated.connect(self.on_tip_link_activated)
        layout.addWidget(self.tip_label)

    def resizeEvent(self, event):
        """重写resizeEvent以调整加载动画位置"""
        super().resizeEvent(event)
        # 调整加载动画位置到中心
        if hasattr(self, 'load_animation') and self.load_animation:
            x = (self.main_widget.width() - self.load_animation.width()) // 2
            y = (self.main_widget.height() - self.load_animation.height()) // 2
            self.load_animation.move(x, y)

    def on_tip_link_activated(self, link):
        """处理提示文字中的链接点击"""
        webbrowser.open(link)

    def check_everything_status(self):
        """检查Everything状态"""
        # 显示遮罩层
        self.stacked_widget.setCurrentIndex(1)
        self.mask_animation.load()

        # 停止之前的状态线程
        if self.status_thread and self.status_thread.isRunning():
            self.status_thread.stop()

        # 创建并启动状态线程
        self.status_thread = EverythingStatusThread(self.everything_path)
        self.status_thread.status_updated.connect(self.on_status_updated)
        self.status_thread.error_occurred.connect(self.on_status_error)
        self.status_thread.start()

    def on_status_updated(self, message, is_ready):
        """状态更新处理"""
        self.label_ready_status.setText(message)
        self.is_ready = is_ready
        self.push_button_search.setEnabled(is_ready)

        if is_ready:
            self.label_ready_status.setStyleSheet("color: green;")
            # Everything已就绪，切换到主界面
            self.stacked_widget.setCurrentIndex(0)
            self.mask_animation.hide()
            self.label_ready_status.hide()
        else:
            self.label_ready_status.setStyleSheet("color: orange;")
            # 更新遮罩层文字
            self.mask_label.setText(message)
            # 重置加载状态
            self.load_ok = False

    def on_status_error(self, error_msg):
        """状态错误处理"""
        self.label_ready_status.show()
        self.label_ready_status.setText(f"Everything错误: {error_msg}")
        self.label_ready_status.setStyleSheet("color: red;")
        self.push_button_search.setEnabled(False)
        self.logger.card_error("文件搜索", f"Everything错误: {error_msg}")

        # 更新遮罩层文字
        self.mask_label.setText(f"Everything错误: {error_msg}")

    def start_clean(self):
        self.line_edit_search.clear()
        self.label_status.setText("请输入搜索关键词")
        self.text_browser_results.clear()

    def start_search(self, offset=0):
        """开始搜索"""
        if not self.is_ready:
            self.label_status.setText("Everything未就绪，无法搜索")
            return

        search_text = self.line_edit_search.text().strip()
        if not search_text:
            self.label_status.setText("请输入搜索关键词")
            # 清空结果显示
            self.text_browser_results.clear()
            return

        # 如果是新的搜索，重置状态
        if offset == 0:
            self.current_search_text = search_text
            self.current_offset = 0
            self.has_more_results = True
            self.total_results = 0
            self.displayed_results = 0

            # 清空结果显示
            self.text_browser_results.clear()
            self.label_status.setText(f"正在搜索: {search_text}")

            # 显示加载动画
            self.load_animation.show()
            self.load_animation.load()
        else:
            # 显示加载更多提示
            self.label_loading_more.show()

        # 停止之前的搜索线程
        if self.search_thread and self.search_thread.isRunning():
            self.search_thread.stop()

        # 创建并启动搜索线程
        self.search_thread = EverythingSearchThread(
            search_text,
            everything_path=self.everything_path,
            offset=offset,
            limit=50
        )
        self.search_thread.search_finished.connect(self.on_search_finished)
        self.search_thread.search_error.connect(self.on_search_error)
        self.search_thread.indexing_status.connect(self.on_indexing_status)
        self.search_thread.start()

    def on_search_finished(self, results, total_results, has_more):
        """搜索完成处理"""
        self.load_animation.hide()
        self.label_loading_more.hide()

        # 更新结果
        if results:
            self.append_results_to_browser(results)

        # 更新状态
        self.total_results = total_results
        self.has_more_results = has_more
        self.current_offset += len(results)

        if self.displayed_results == 0:
            self.label_status.setText("未找到匹配的文件")
        else:
            more_text = "，还有更多结果..." if has_more else ""
            self.label_status.setText(f"已找到 {total_results} 个结果，已显示 {self.displayed_results} 个{more_text}")

    def append_results_to_browser(self, results):
        """将结果追加到浏览器中"""
        if not results:
            return

        html_content = ""
        for result in results:
            # 提取文件名和路径
            file_name = result.filename
            file_suffix_list = os.path.splitext(file_name)
            file_suffix = file_suffix_list[1].replace(".", "").lower() if len(file_suffix_list) > 1 else ""
            file_path = result.path
            file_type = "文件夹" if result.is_folder else "文件"
            # 使用新函数格式化文件大小
            file_size = "0B" if result.is_folder else self.format_file_size(result.size)
            modified_time = result.date_modified.strftime("%Y-%m-%d %H:%M:%S")

            # 对文件路径进行URL编码，特别是处理空格等特殊字符
            encoded_path = quote(file_path.replace("\\", "/"))  # 转换为正斜杠并编码

            # 根据文件类型选择图标或字符
            if result.is_folder:
                # 使用文字字符📁代替文件夹图标
                icon_html = '<span style="font-size: 26px; vertical-align: middle;">📁</span>'
            else:
                if file_suffix in self.suffix_icon_map:
                    icon_path = self.suffix_icon_map[file_suffix]
                else:
                    icon_path = self.suffix_icon_map["file"]
                icon_path = ":static/img/IconPark/grey/" + icon_path + ".png"
                icon_html = f'<img src="{icon_path}" width="26" height="26" style="vertical-align: middle;">'

            # 创建可点击的链接
            html_content += f'<div style="margin-bottom: 5px;">'
            html_content += f'{icon_html}'
            html_content += f'<a href="file:///{encoded_path}" style="font-weight: bold; text-decoration: none; font-size: 14px; vertical-align: middle;">&nbsp;{file_name}</a>'
            html_content += f'</div>'
            html_content += f'<div style="color: #666; font-size: 12px; margin-bottom: 10px;">{file_path}<br>'
            html_content += f'类型: <span style="font-weight: bold; font-size: 12px;"> {file_type} </span>'
            html_content += f' | 大小: <span style="font-weight: bold; font-size: 12px;"> {file_size} </span>'
            html_content += f' | 修改时间: <span style="font-weight: bold; font-size: 12px;"> {modified_time} </span>'
            html_content += f'<br></div>'

        # 保存当前滚动位置
        scroll_bar = self.text_browser_results.verticalScrollBar()
        scroll_pos = scroll_bar.value()

        # 追加内容
        cursor = self.text_browser_results.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.text_browser_results.setTextCursor(cursor)
        self.text_browser_results.insertHtml(html_content)

        # 恢复滚动位置
        scroll_bar.setValue(scroll_pos)

        # 更新计数
        self.displayed_results += len(results)

    def format_file_size(self, size_bytes):
        """
        将文件大小从字节转换为合适的单位进行展示

        Args:
            size_bytes (int): 文件大小（字节）

        Returns:
            str: 格式化后的文件大小字符串
        """
        if size_bytes == 0:
            return "0 B"

        size_units = ["B", "KB", "MB", "GB", "TB"]
        unit_index = 0
        size_value = float(size_bytes)

        while size_value >= 1024 and unit_index < len(size_units) - 1:
            size_value /= 1024
            unit_index += 1

        # 如果是整数，显示为整数格式
        if size_value.is_integer():
            return f"{int(size_value)} {size_units[unit_index]}"
        else:
            return f"{size_value:.1f} {size_units[unit_index]}"

    def on_search_error(self, error_msg):
        """搜索错误处理"""
        self.load_animation.hide()
        self.label_loading_more.hide()
        self.label_status.setText(f"搜索错误: {error_msg}")
        self.logger.card_error("文件搜索", f"搜索错误: {error_msg}")

    def on_indexing_status(self, is_indexing):
        """索引状态更新"""
        self.is_indexing = is_indexing
        if is_indexing:
            self.label_indexing.setText("Everything正在索引文件，请稍候...")
        else:
            self.label_indexing.setText("")
            self.label_indexing.hide()

    def on_scroll(self, value):
        """滚动事件处理"""
        scroll_bar = self.text_browser_results.verticalScrollBar()

        # 检查是否滚动到底部
        if (value >= scroll_bar.maximum() - 10 and
                self.has_more_results and
                not (self.search_thread and self.search_thread.isRunning())):
            # 加载更多结果
            self.start_search(offset=self.current_offset)

    def on_result_clicked(self, url):
        """结果点击处理"""
        # 获取原始URL并解码
        raw_url = url.toString()
        # 移除"file:///"前缀并解码URL
        if raw_url.startswith("file:///"):
            file_path = unquote(raw_url[8:])  # 移除"file:///"前缀并解码
        else:
            file_path = unquote(raw_url)
        try:
            # 在文件管理器中打开并选中文件
            if os.name == 'nt':  # Windows
                file_path = file_path.replace("/", "\\")
                os.system(f'explorer /select,\""{file_path}"\"')
            elif os.name == 'posix':  # macOS
                os.system(f'open -R "{file_path}"')
            else:  # Linux
                os.system(f'xdg-open "{os.path.dirname(file_path)}"')
        except Exception as e:
            self.logger.card_error("文件搜索", f"打开文件失败: {str(e)}")

    def refresh_theme(self):
        """刷新主题"""
        if not super().refresh_theme():
            return False

        if self.is_light():
            # 浅色主题样式
            self.text_browser_results.setStyleSheet("""
                QTextBrowser {
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    background-color: transparent;
                }
            """ + style_util.scroll_bar_style)
            self.label_ready_status.setStyleSheet("background: transparent;")
            self.label_status.setStyleSheet("background: transparent;")
            self.label_indexing.setStyleSheet("background: transparent;")
            self.label_loading_more.setStyleSheet("background: transparent;")
        else:
            # 深色主题样式
            self.text_browser_results.setStyleSheet("""
                QTextBrowser {
                    border: 1px solid #555;
                    border-radius: 4px;
                    background-color: transparent;
                    color: white;
                }
            """ + style_util.scroll_bar_style)
            self.label_ready_status.setStyleSheet("color: #aaa;")
            self.label_status.setStyleSheet("color: #aaa;")
            self.label_indexing.setStyleSheet("color: #ffaa33;")
            self.label_loading_more.setStyleSheet("color: #aaa;")
        # 调整其他样式
        style_util.set_button_style(self.push_button_clean, self.main_object.is_dark)
        style_util.set_button_style(self.push_button_search, self.main_object.is_dark)
        style_util.set_line_edit_style(self.line_edit_search, self.main_object.is_dark)
        self.load_animation.set_theme(self.is_light())
        return True

    def refresh_data(self, date_time_str):
        """刷新数据"""
        super().refresh_data(date_time_str)
        if self.load_ok:
            return
        self.load_ok = True
        # 启动状态检查
        print("启动everything状态检查...")
        self.check_everything_status()

    def refresh_ui(self, date_time_str):
        """刷新UI"""
        super().refresh_ui(date_time_str)
        super().refresh_ui_end(date_time_str)

    def show_form(self):
        """
        隐藏窗口
        """
        # 设置输入焦点
        self.line_edit_search.setFocus()