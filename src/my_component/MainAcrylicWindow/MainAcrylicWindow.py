import win32con
from ctypes.wintypes import MSG

from PySide6.QtCore import QEvent, QPoint, Qt
from PySide6.QtGui import QCloseEvent, QMouseEvent, QCursor
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from qframelesswindow.titlebar.title_bar_buttons import TitleBarButtonState
from qframelesswindow.utils import win32_utils as win_utils
from qframelesswindow.windows import WindowsFramelessWindowBase

from src.my_component.BaseWindowsWindowEffect.BaseWindowsWindowEffect import BaseWindowsWindowEffect
from src.my_component.titlebar import TitleBar


class WindowsFramelessWindow(WindowsFramelessWindowBase, QWidget):
    """  Frameless window for Windows system """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._initFrameless()


class MainAcrylicWindow(WindowsFramelessWindow):
    """ A frameless window with acrylic effect """

    base_layout = None  # 基础布局
    widget_base = None  # 全局控件的基础
    # 自定义标识符
    has_set_acrylic_effect = False

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.__closedByKey = False
        self.titleBar.hide()
        self.init_ui()

    def init_ui(self):
        # 基础布局
        self.base_layout = QVBoxLayout(self)
        self.base_layout.setContentsMargins(0, 0, 0, 0)
        self.base_layout.setSpacing(0)
        self.widget_base = QWidget(self)
        self.widget_base.setObjectName(u"widget_base")
        self.widget_base.setStyleSheet(u"QWidget {"
        "    border-radius: 0px;"
        "    border: none;"
        "    background-color: background:transparent;"
        "}")
        self.base_layout.addWidget(self.widget_base)

    def _initFrameless(self):
        self.super_initFrameless()

    def super_initFrameless(self):
        self.windowEffect = BaseWindowsWindowEffect(self)
        self.titleBar = TitleBar(self)
        # self.titleBar.installEventFilter(self)
        self._isResizeEnabled = True
        self.updateFrameless()
        self.resize(500, 500)
        self.titleBar.raise_()

    def updateFrameless(self):
        pass


    def setFrameless(self, is_main=None, is_start=False, is_dark=None, form_theme_mode=None):
        base_type = "MainAcrylicWindow"
        windows_type = base_type + f"{'未知窗口' if is_main is None else {'主窗口' if is_main else '子窗口'}}"
        if is_start:
            # if not self.has_set_acrylic_effect:
            #     return
            # 初始化时使用
            self.windowEffect.enableBlurBehindWindow(self.winId())
            self.windowEffect.addWindowAnimation(self.winId())
            self.windowEffect.setAcrylicEffect(self.winId())          # 设置亚克力效果
            if win_utils.isGreaterEqualWin11():
                self.windowEffect.addShadowEffect(self.winId())   # 添加阴影
            self.has_set_acrylic_effect = True
        else:
            if is_dark:
                # 深色
                print(f"{windows_type}:setFrameless:深色")
                # if self.has_set_acrylic_effect:
                #     return
                self.windowEffect.enableBlurBehindWindow(self.winId())
                self.windowEffect.addWindowAnimation(self.winId())
                if win_utils.isGreaterEqualWin11():
                    self.windowEffect.addShadowEffect(self.winId())
                self.windowEffect.removeBackgroundEffect(self.winId())
                self.has_set_acrylic_effect = False
            else:
                # 浅色
                print(f"{windows_type}:setFrameless:浅色")
                if form_theme_mode is not None and form_theme_mode == "Acrylic":
                    # 亚克力
                    print(f"{windows_type}:setFrameless:浅色:亚克力")
                    # if not self.has_set_acrylic_effect:
                    #     return
                    self.windowEffect.enableBlurBehindWindow(self.winId())
                    self.windowEffect.addWindowAnimation(self.winId())
                    self.windowEffect.setAcrylicEffect(self.winId())          # 设置亚克力效果
                    if win_utils.isGreaterEqualWin11():
                        self.windowEffect.addShadowEffect(self.winId())   # 添加阴影
                    self.has_set_acrylic_effect = True
                else:
                    # 半透明
                    print(f"{windows_type}:setFrameless:浅色:半透明")
                    # if self.has_set_acrylic_effect:
                    #     return
                    if win_utils.isGreaterEqualWin11():
                        self.windowEffect.addShadowEffect(self.winId())   # 添加阴影
                    self.windowEffect.removeBackgroundEffect(self.winId())
                    self.has_set_acrylic_effect = False

    def nativeEvent(self, eventType, message):
        """ Handle the Windows message """
        msg = MSG.from_address(message.__int__())
        if not msg.hWnd:
            return super().nativeEvent(eventType, message)

        if msg.message == win32con.WM_NCHITTEST and self._isResizeEnabled:
            if self._isHoverMaxBtn():
                self.titleBar.maxBtn.setState(TitleBarButtonState.HOVER)
                return True, win32con.HTMAXBUTTON
        elif msg.message in [0x2A2, win32con.WM_MOUSELEAVE]:
            self.titleBar.maxBtn.setState(TitleBarButtonState.NORMAL)
        elif msg.message in [win32con.WM_NCLBUTTONDOWN, win32con.WM_NCLBUTTONDBLCLK] and self._isHoverMaxBtn():
            e = QMouseEvent(QEvent.MouseButtonPress, QPoint(), Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
            QApplication.sendEvent(self.titleBar.maxBtn, e)
            return True, 0
        elif msg.message in [win32con.WM_NCLBUTTONUP, win32con.WM_NCRBUTTONUP] and self._isHoverMaxBtn():
            e = QMouseEvent(QEvent.MouseButtonRelease, QPoint(), Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
            QApplication.sendEvent(self.titleBar.maxBtn, e)

        # handle resize and move
        if msg.message == win32con.WM_ENTERSIZEMOVE or msg.message == win32con.WM_ENTERSIZEMOVE:
            self.windowEffect.resetAcrylicEffect(self.winId())
        if msg.message == win32con.WM_EXITSIZEMOVE or msg.message == win32con.WM_EXITSIZEMOVE:
            self.windowEffect.setAcrylicEffect(self.winId())

        # handle Alt+F4
        if msg.message == win32con.WM_SYSKEYDOWN:
            if msg.wParam == win32con.VK_F4:
                self.__closedByKey = True
                QApplication.sendEvent(self, QCloseEvent())
                return False, 0

        return super().nativeEvent(eventType, message)

    def _isHoverMaxBtn(self):
        pos = QCursor.pos() - self.geometry().topLeft() - self.titleBar.pos()
        return self.titleBar.childAt(pos) is self.titleBar.maxBtn

    def closeEvent(self, e):
        if not self.__closedByKey or QApplication.quitOnLastWindowClosed():
            self.__closedByKey = False
            return super().closeEvent(e)

        # system tray icon
        self.__closedByKey = False
        self.hide()