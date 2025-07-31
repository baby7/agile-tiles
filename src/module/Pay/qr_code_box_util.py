import io
import qrcode

from PySide6.QtGui import Qt, QFont, QPixmap
from PySide6.QtCore import Signal, QTimer
from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QLayout, QStackedLayout, QWidget

from src.client import common
from src.component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
from src.component.LoadAnimation.LoadAnimation import LoadAnimation
from src.module.Pay.payment_result_page import PaymentResultPage
from src.module.Pay.payment_websocket_client import PaymentWebSocketClient
from src.module.Pay.plan_card import PlanCard
from src.module.Pay.qr_generation_thread import QRGenerationManager
from src.module.Pay.subscription_plan_fetcher import SubscriptionPlanFetcher
from src.ui import style_util


class SquareQLabel(QLabel):
    def resizeEvent(self, event):
        size = min(self.width(), self.height())
        self.setFixedSize(size, size)
        super().resizeEvent(event)


class QrPopup(AgileTilesAcrylicWindow):
    setPixmapSignal = Signal(QPixmap)
    # 添加调试模式常量
    DEBUG_MODE = False  # 设为True时显示支付状态标签

    def __init__(self, parent=None, use_parent=None, title=None, screen=None):
        super().__init__(parent=parent, is_dark=use_parent.is_dark, form_theme_mode=use_parent.form_theme_mode,
                         form_theme_transparency=use_parent.form_theme_transparency)
        self.use_parent = use_parent
        # 新增加载状态标志
        self.is_loading = False
        # 创建二维码管理器（不再是线程）
        self.create_qr_manager()
        # 创建WebSocket客户端
        self.create_websocket_client()
        # 参数初始化
        self.is_closed = False              # 添加关闭状态标志
        self.screen = screen                # 屏幕对象
        # 订阅计划
        self.subscription_plans = []        # 存储订阅计划
        self.plan_cards = {}                # 存储卡片对象
        # 状态标志
        self.current_plan = None            # 当前选中的计划
        self.current_order_no = None        # 当前订单号
        self.payment_success = False        # 支付状态标志
        # 添加分层控制变量
        self.payment_page = None            # 付款页面
        self.result_page = None             # 结果页面
        self.stacked_layout = None          # 堆叠布局管理器
        try:
            self.setWindowTitle("支付" if title is None else title)
            self.center_on_screen()
            self.setMinimumWidth(500)  # 增加最小宽度以适应新布局
            self.setMinimumHeight(600)
            # 初始化界面
            self.init_ui()
            # 获取订阅计划
            self.fetch_subscription_plans()
        except Exception as e:
            print(e)
        # 连接新信号
        self.setPixmapSignal.connect(self.on_image_loaded)
        # 新增超时定时器
        self.load_timeout_timer = QTimer(self)
        self.load_timeout_timer.setSingleShot(True)
        self.load_timeout_timer.timeout.connect(self.handle_load_timeout)

    def create_qr_manager(self):
        """创建二维码管理器"""
        self.qr_manager = QRGenerationManager(self.use_parent)
        self.qr_manager.finished.connect(self.on_qr_data_received)
        self.qr_manager.error.connect(self.on_qr_generation_error)

    def create_websocket_client(self):
        """创建WebSocket客户端"""
        self.websocket_client = PaymentWebSocketClient(self.use_parent)
        self.websocket_client.connected.connect(self.on_websocket_connected)
        self.websocket_client.disconnected.connect(self.on_websocket_disconnected)
        self.websocket_client.message_received.connect(self.on_websocket_message)
        self.websocket_client.error_occurred.connect(self.on_websocket_error)

    def fetch_subscription_plans(self):
        """获取订阅计划列表"""
        self.plan_fetcher = SubscriptionPlanFetcher(self.use_parent)
        self.plan_fetcher.fetched.connect(self.on_plans_fetched)
        self.plan_fetcher.error.connect(self.on_plans_error)
        self.plan_fetcher.fetch()  # 直接调用，无需启动线程

    def init_ui(self):
        # 创建堆叠布局管理两层页面
        self.stacked_layout = QStackedLayout()

        # 创建付款页面
        self.payment_page = QWidget()
        self.init_payment_page()
        self.stacked_layout.addWidget(self.payment_page)

        # 创建结果页面
        self.result_page = PaymentResultPage(self, self.is_dark)
        # 连接信号
        self.result_page.completeClicked.connect(self.close)
        self.result_page.retryClicked.connect(self.return_to_payment)
        self.stacked_layout.addWidget(self.result_page)

        # 默认显示付款页面
        self.stacked_layout.setCurrentIndex(0)

        # 设置主布局
        self.widget_base.setLayout(self.stacked_layout)
        self.update()

    def init_payment_page(self):
        """初始化付款组件页面"""
        # 主垂直布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # 1. 添加标题
        title_label = QLabel("选择订阅计划")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #4d90fe;" if not self.is_dark else "color: #64b5f6;")
        main_layout.addWidget(title_label)

        # 2. 添加选项卡片容器
        self.cards_container = QHBoxLayout()
        self.cards_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cards_container.setSpacing(20)

        # 添加加载动画
        self.plans_loading = LoadAnimation(self, theme="Dark" if self.is_dark else "Light")
        self.plans_loading.setFixedSize(40, 40)
        self.cards_container.addWidget(self.plans_loading)

        main_layout.addLayout(self.cards_container)

        # 3. 支付区域（二维码和支付信息）
        payment_layout = QHBoxLayout()
        payment_layout.setSpacing(30)

        # 左边：二维码区域
        qr_container = QVBoxLayout()
        qr_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        qr_container.setSpacing(10)
        qr_container.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        # 二维码标题
        qr_title = QLabel("支付宝二维码")
        qr_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        qr_title_font = QFont()
        qr_title_font.setPointSize(14)
        qr_title_font.setBold(True)
        qr_title.setFont(qr_title_font)
        qr_container.addWidget(qr_title)

        # 加载动画容器
        self.loading_container = QHBoxLayout()
        self.loading_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        qr_container.addLayout(self.loading_container)

        # 二维码标签
        self.image_label = SquareQLabel(self)
        self.image_label.setStyleSheet(style_util.transparent_style)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(200, 200)
        qr_container.addWidget(self.image_label)

        payment_layout.addLayout(qr_container, 50)

        # 右边：支付信息
        info_container = QVBoxLayout()
        info_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_container.setSpacing(15)

        # 价格信息
        price_title = QLabel("当前价格")
        price_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        price_title_font = QFont()
        price_title_font.setPointSize(14)
        price_title.setFont(price_title_font)
        price_title.setStyleSheet("background: transparent;")
        info_container.addWidget(price_title)

        self.price_value = QLabel("¥0.00")
        price_value_font = QFont()
        price_value_font.setPointSize(28)
        price_value_font.setBold(True)
        self.price_value.setFont(price_value_font)
        self.price_value.setStyleSheet(
            "background: transparent;color: #e74c3c;" if not self.is_dark else "background: transparent;color: #ef9a9a;")
        self.price_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_container.addWidget(self.price_value)

        # 支付提示
        payment_info = QLabel("使用支付宝扫码支付")
        payment_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        payment_info_font = QFont()
        payment_info_font.setPointSize(16)
        payment_info.setFont(payment_info_font)
        payment_info.setStyleSheet("background: transparent;")
        info_container.addWidget(payment_info)

        # 协议提示
        agreement_info = QLabel(
            f'开通前请阅读<a href="{common.user_agreement_url}"><span style="color: #4d90fe; text-decoration: underline;">《用户协议》</span></a>')
        agreement_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        agreement_info.setOpenExternalLinks(True)
        agreement_info_font = QFont()
        agreement_info_font.setPointSize(11)
        agreement_info.setFont(agreement_info_font)
        agreement_info.setStyleSheet("background: transparent;")
        info_container.addWidget(agreement_info)

        # 占位空间
        info_container.addStretch(1)

        payment_layout.addLayout(info_container, 50)
        main_layout.addLayout(payment_layout, 70)

        # 仅在调试模式下显示支付状态标签
        if self.DEBUG_MODE:
            debug_layout = QVBoxLayout()
            debug_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            debug_layout.setContentsMargins(0, 20, 0, 0)

            self.debug_status_label = QLabel("调试状态: 等待支付...")
            self.debug_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            debug_font = QFont()
            debug_font.setPointSize(12)
            self.debug_status_label.setFont(debug_font)
            self.debug_status_label.setStyleSheet("color: #f39c12;")
            debug_layout.addWidget(self.debug_status_label)

            main_layout.addLayout(debug_layout)

        self.payment_page.setLayout(main_layout)

    def return_to_payment(self):
        """返回付款页面"""
        self.stacked_layout.setCurrentIndex(0)  # 切换到付款页面
        self.reload_qr_code()

    def center_on_screen(self):
        self.refresh_geometry(self.screen)

    def on_plans_fetched(self, plans):
        """订阅计划获取成功"""
        self.subscription_plans = plans
        self.plans_loading.deleteLater()  # 移除加载动画

        if not plans:
            error_label = QLabel("暂无可用订阅计划")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            error_label.setStyleSheet("color: #e74c3c;" if not self.is_dark else "color: #ef9a9a;")
            self.cards_container.addWidget(error_label)
            return

        # 创建计划卡片
        for plan in plans:
            card = PlanCard(
                title=plan["name"],
                base_price=plan['basePrice'],
                discount_price=plan['discountPrice'],
                plan_code=plan['code'],
                is_dark=self.is_dark
            )
            card.mousePressEvent = lambda event, p=plan: self.plan_changed(p['code'])
            self.cards_container.addWidget(card)
            self.plan_cards[plan['code']] = card

        # 默认选中第一个计划
        if plans:
            self.plan_changed(plans[0]['code'])

    def on_plans_error(self, error_msg):
        """订阅计划获取失败"""
        self.plans_loading.deleteLater()  # 移除加载动画
        error_label = QLabel(error_msg)
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_label.setStyleSheet("color: #e74c3c;" if not self.is_dark else "color: #ef9a9a;")
        self.cards_container.addWidget(error_label)

    def plan_changed(self, plan_code):
        """当用户切换订阅计划时调用"""
        # 检查是否正在加载中
        if self.is_loading:
            return

        # 检查是否与当前计划相同
        if self.current_plan == plan_code:
            return

        # 更新所有卡片选中状态
        for code, card in self.plan_cards.items():
            card.set_selected(code == plan_code)

        # 更新当前选中的计划
        self.current_plan = plan_code

        # 查找对应的计划信息
        selected_plan = next((p for p in self.subscription_plans if p['code'] == plan_code), None)

        if selected_plan:
            # 更新价格显示
            self.price_value.setText(f"¥{selected_plan['discountPrice']:.2f}")
            self.reload_qr_code()

    def reload_qr_code(self):
        """重新加载二维码"""
        # 设置加载状态
        self.is_loading = True

        # 清理现有连接
        self.websocket_client.disconnect_from_server()

        self.payment_success = False
        self.update_payment_status("等待支付...", "info")

        if not self.current_plan:
            return

        # 清除当前显示的二维码
        self.image_label.clear()

        # 显示加载动画
        self.show_loading_animation()

        # 发起异步请求
        self.qr_manager.fetch_qr_code(self.current_plan)

        # 启动超时定时器 (5秒超时)
        self.load_timeout_timer.start(5000)  # 1000毫秒 = 1秒

    def handle_load_timeout(self):
        """处理加载超时"""
        if not self.is_loading:
           return

        # 取消当前请求
        self.cancel_current_request()

        # 移除加载动画
        if hasattr(self, 'loading_animation'):
           self.loading_animation.deleteLater()
           del self.loading_animation

        # 显示超时提示
        self.image_label.setText("加载超时，请重试")

        # 重置加载状态
        self.is_loading = False

    def show_loading_animation(self):
        """显示加载动画"""
        try:
            # 移除旧的加载动画（如果存在）
            if hasattr(self, 'loading_animation'):
                self.loading_animation.deleteLater()

            # 创建新的加载动画
            self.loading_animation = LoadAnimation(self, theme="Dark" if self.is_dark else "Light")
            self.loading_animation.setFixedSize(60, 60)

            # 清除加载容器并添加新动画
            while self.loading_container.count():
                item = self.loading_container.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            self.loading_container.addWidget(self.loading_animation)
            self.loading_animation.load()
        except Exception as e:
            print(f"加载动画错误: {e}")

    def generate_qr_in_main_thread(self, qr_data):
        """在主线程生成二维码"""
        if self.is_closed or not qr_data:
            return None

        try:
            qr = qrcode.main.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

            with io.BytesIO() as buffer:
                img.save(buffer, format='PNG')
                pixmap = QPixmap()
                pixmap.loadFromData(buffer.getvalue(), 'PNG')
                return pixmap

        except Exception as e:
            print(f"二维码生成错误: {str(e)}")
            return None

    def on_qr_data_received(self, qr_data):
        """接收二维码数据并在主线程生成图片"""
        # 停止超时定时器
        self.load_timeout_timer.stop()

        # 重置加载状态
        self.is_loading = False

        if self.is_closed:
            return

        # 移除加载动画
        if hasattr(self, 'loading_animation'):
            self.loading_animation.deleteLater()
            del self.loading_animation

        # 更新订单号 & 添加WebSocket连接
        self.current_order_no = qr_data['outTradeNo']
        self.websocket_client.connect_to_server(self.current_order_no)

        # 在主线程生成二维码
        pixmap = self.generate_qr_in_main_thread(qr_data['qrCode'])

        # 显示二维码
        if pixmap and not pixmap.isNull():
            self.setPixmapSignal.emit(pixmap)
        else:
            self.image_label.setText("二维码生成失败")

    def on_qr_generation_error(self, error_msg):
        """处理二维码生成错误"""
        # 停止超时定时器
        self.load_timeout_timer.stop()

        # 重置加载状态
        self.is_loading = False

        if self.is_closed:
            return

        # 移除加载动画
        if hasattr(self, 'loading_animation'):
            self.loading_animation.deleteLater()
            del self.loading_animation

        self.image_label.setText(f"错误: {error_msg}")

    def cancel_current_request(self):
        """取消当前请求"""
        self.qr_manager.cancel()

    def on_image_loaded(self, pixmap):
        """图片加载完成后的处理"""
        if not pixmap or pixmap.isNull():
            self.image_label.setText("二维码生成失败")
            return
        # 设置二维码图片
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        # 调整窗口大小
        self.adjustSize()
        # 窗口居中
        self.center_on_screen()
        self.update()

    def on_websocket_connected(self):
        """WebSocket连接成功"""
        self.update_payment_status("正在监听支付结果...", "info")

    def on_websocket_disconnected(self):
        """WebSocket断开连接"""
        self.update_payment_status("连接中断，正在重连...", "warning")

    def on_websocket_error(self, error_msg):
        """WebSocket错误处理"""
        self.update_payment_status(error_msg, "error")

    def on_websocket_message(self, data):
        """处理WebSocket消息"""
        order_id = data.get('orderId')
        status = data.get('status')

        # 只处理当前订单的消息
        if order_id == self.current_order_no:
            if status == "PAID":
                self.handle_payment_success()
                # 触发刷新
                self.use_parent.time_task()
            elif status == "FAILED":
                self.handle_payment_failed()

    def update_payment_status(self, message, status_type):
        """更新支付状态显示（仅在调试模式下显示）"""
        if self.DEBUG_MODE and hasattr(self, 'debug_status_label'):
            self.debug_status_label.setText(f"调试信息: {message}, 状态类型: {status_type}")

    def handle_payment_success(self):
        """处理支付成功"""
        self.payment_success = True

        # 切换到结果页面
        if not self.stacked_layout:
            print("错误: stacked_layout 未初始化!")
            return
        self.stacked_layout.setCurrentIndex(1)

        # 设置结果页面为成功状态
        self.result_page.set_result(True)

        # 关闭WebSocket
        try:
            self.websocket_client.disconnect_from_server()
        except Exception as e:
            print(f"WebSocket 错误: {str(e)}")

        # 通知主程序进行更新
        try:
            self.use_parent.time_task()
        except Exception as e:
            print(f"付款后通知主程序刷新错误: {str(e)}")

    def handle_payment_failed(self):
        """处理支付失败"""
        # 切换到结果页面
        if not self.stacked_layout:
            print("错误: stacked_layout 未初始化!")
            return
        self.stacked_layout.setCurrentIndex(1)

        # 设置结果页面为失败状态
        self.result_page.set_result(False)

        # 清除当前二维码
        self.image_label.clear()

        # 关闭WebSocket
        self.websocket_client.disconnect_from_server()

    def closeEvent(self, event):
        # 停止超时定时器
        self.load_timeout_timer.stop()

        # 标记窗口已关闭
        self.is_closed = True

        # 取消所有网络请求
        self.cancel_current_request()

        # 取消计划获取器
        if hasattr(self, 'plan_fetcher'):
            self.plan_fetcher.manager.deleteLater()

        # 移除加载动画
        if hasattr(self, 'loading_animation'):
            try:
                self.loading_animation.deleteLater()
            except RuntimeError:
                pass

        # WebSocket清理
        self.websocket_client.disconnect_from_server()

        super().closeEvent(event)


def show_qr_code_dialog(main_object, title):
    screen = main_object.toolkit.resolution_util.get_screen(main_object)
    dialog = QrPopup(None, use_parent=main_object, title=title, screen=screen)
    dialog.refresh_geometry(screen)
    dialog.show()
    return dialog