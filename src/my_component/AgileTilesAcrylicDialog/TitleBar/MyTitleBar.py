# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLabel
from qframelesswindow import TitleBar


class MyTitleBar(TitleBar):
    """ Title bar with icon and title """

    def __init__(self, parent):
        super().__init__(parent)
        # add window icon
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(15, 15)
        self.hBoxLayout.insertSpacing(0, 15)
        self.hBoxLayout.insertWidget(1, self.iconLabel, 0, Qt.AlignLeft)
        self.window().windowIconChanged.connect(self.setIcon)

        # add title label
        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(2, self.titleLabel, 0, Qt.AlignLeft)
        self.titleLabel.setStyleSheet("""
            QLabel{
                background: transparent;
                padding: 0 4px
            }
        """)
        self.window().windowTitleChanged.connect(self.setTitle)
        # 隐藏最大化和最小化按钮
        self.minBtn.hide()
        self.maxBtn.hide()
        # 禁用最大化、最小化功能
        self.maxBtn.setEnabled(False)
        self.minBtn.setEnabled(False)

    def setTitle(self, title):
        """ set the title of title bar
        Parameters
        ----------
        title: str
            the title of title bar
        """
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        """ set the icon of title bar
        Parameters
        ----------
        icon: QIcon | QPixmap | str
            the icon of title bar
        """
        self.iconLabel.setPixmap(QIcon(icon).pixmap(15, 15))

    # 禁用双击最大化
    def mouseDoubleClickEvent(self, event):
        pass