# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QCursor, QColor
from PySide6.QtWidgets import QLabel, QPushButton
from qframelesswindow import TitleBar

from src.util import browser_util


class AgileTilesTitleBar(TitleBar):
    """ Title bar with icon and title """

    link = None
    is_dark = False

    def __init__(self, parent, is_dark=False):
        super().__init__(parent)
        self.is_dark = is_dark
        self.dialog_parent = parent

        # add window icon
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(15, 15)
        self.hBoxLayout.insertSpacing(0, 15)
        self.hBoxLayout.insertWidget(1, self.iconLabel, 0, Qt.AlignLeft)
        self.window().windowIconChanged.connect(self.setIcon)

        # add title button
        self.titlePushButton = QPushButton(self)
        self.titlePushButton.setObjectName("AgileTilesTitleBarTitlePushButton")
        self.hBoxLayout.insertWidget(2, self.titlePushButton, 0, Qt.AlignLeft)
        if self.is_dark:
            self.titlePushButton.setStyleSheet("""
                QPushButton {
                    border: none;
                    background: transparent;
                    padding: 0 4px;
                    color: rgba(255, 255, 255, 200);
                }""")
            self.minBtn.setNormalColor(QColor(255, 255, 255))
            self.maxBtn.setNormalColor(QColor(255, 255, 255))
            self.closeBtn.setNormalColor(QColor(255, 255, 255))
        else:
            self.titlePushButton.setStyleSheet("""
                QPushButton {
                    border: none;
                    background: transparent;
                    padding: 0 4px;
                    color: #000000;
                }""")
        self.titlePushButton.clicked.connect(self.push_button_title_click)
        self.window().windowTitleChanged.connect(self.setTitle)

        # add question button
        self.questionPushButton = QPushButton(self)
        self.questionPushButton.setObjectName("AgileTilesTitleBarQuestionPushButton")
        self.hBoxLayout.insertWidget(3, self.questionPushButton, 0, Qt.AlignLeft)
        if self.is_dark:
            self.questionPushButton.setStyleSheet("""
                QPushButton {
                    border: none;
                    background: transparent;
                    padding: 0 4px;
                }""")
            self.questionPushButton.setIcon(QIcon("./static/img/IconPark/light/Character/help.png"))
        else:
            self.questionPushButton.setStyleSheet("""
                QPushButton {
                    border: none;
                    background: transparent;
                    padding: 0 4px;
                }""")
            self.questionPushButton.setIcon(QIcon("./static/img/IconPark/dark/Character/help.png"))
        self.questionPushButton.clicked.connect(self.push_button_question_click)
        self.questionPushButton.setToolTip("这是第三方模块，可以点击左边的标题按钮访问模块主页哦~")
        self.questionPushButton.hide()

        # # 鼠标手形
        self.minBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.maxBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.closeBtn.setCursor(QCursor(Qt.PointingHandCursor))

    def setTitle(self, title):
        """ set the title of title bar
        Parameters
        ----------
        title: str
            the title of title bar
        """
        self.titlePushButton.setText(title)
        self.titlePushButton.adjustSize()

    def setIcon(self, icon):
        """ set the icon of title bar
        Parameters
        ----------
        icon: QIcon | QPixmap | str
            the icon of title bar
        """
        self.iconLabel.setPixmap(QIcon(icon).pixmap(15, 15))

    def setLink(self, link):
        self.link = link
        # 标题颜色变为蓝色
        self.titlePushButton.setStyleSheet("""
            QPushButton{
                border: none;
                background: transparent;
                padding: 0 4px;
                color: #0078D4;
                text-decoration:underline;
            }
        """)
        # 指向手势
        self.titlePushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.questionPushButton.show()

    def push_button_title_click(self):
        if self.link:
            browser_util.open_url(self.link)

    def push_button_question_click(self):
        if self.link:
            self.dialog_parent.message_box_util.box_information(self.dialog_parent, "提示", "这是第三方模块，可以点击左边的标题按钮访问模块主页哦~")
