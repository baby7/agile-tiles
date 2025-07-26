# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'baby7_desktop_tool_form.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QTabWidget, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1542, 1255)
        self.setting_area = QScrollArea(Form)
        self.setting_area.setObjectName(u"setting_area")
        self.setting_area.setGeometry(QRect(490, 10, 386, 461))
        font = QFont()
        font.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font.setBold(True)
        self.setting_area.setFont(font)
        self.setting_area.setStyleSheet(u"\n"
"border-style:solid;\n"
"border-radius:10px;\n"
"border:0px groove gray;\n"
"color:rgb(0, 0, 0);\n"
"border-color:rgba(255, 255, 255, 0);\n"
"background-color:rgba(255, 255, 255, 100);\n"
"")
        self.setting_area.setFrameShape(QFrame.StyledPanel)
        self.setting_area.setLineWidth(1)
        self.setting_area.setWidgetResizable(True)
        self.scrollAreaWidgetContents_37 = QWidget()
        self.scrollAreaWidgetContents_37.setObjectName(u"scrollAreaWidgetContents_37")
        self.scrollAreaWidgetContents_37.setGeometry(QRect(0, 0, 386, 461))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents_37)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 20, 5, 5)
        self.label_17 = QLabel(self.scrollAreaWidgetContents_37)
        self.label_17.setObjectName(u"label_17")
        font1 = QFont()
        font1.setPointSize(11)
        self.label_17.setFont(font1)
        self.label_17.setStyleSheet(u"background: transparent;")

        self.verticalLayout.addWidget(self.label_17)

        self.widget_setting_setting = QWidget(self.scrollAreaWidgetContents_37)
        self.widget_setting_setting.setObjectName(u"widget_setting_setting")
        self.widget_setting_setting.setStyleSheet(u"QWidget {\n"
"border-style: solid;\n"
"border-radius: 10px;\n"
"border: 1px solid white;\n"
"background-color:rgba(255, 255, 255, 200);\n"
"}")
        self.gridLayout_3 = QGridLayout(self.widget_setting_setting)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.push_button_setting_system = QPushButton(self.widget_setting_setting)
        self.push_button_setting_system.setObjectName(u"push_button_setting_system")
        self.push_button_setting_system.setMinimumSize(QSize(70, 70))
        self.push_button_setting_system.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.push_button_setting_system)

        self.push_button_setting_card_permutation = QPushButton(self.widget_setting_setting)
        self.push_button_setting_card_permutation.setObjectName(u"push_button_setting_card_permutation")
        self.push_button_setting_card_permutation.setMinimumSize(QSize(70, 70))
        self.push_button_setting_card_permutation.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.push_button_setting_card_permutation)

        self.push_button_setting_screen = QPushButton(self.widget_setting_setting)
        self.push_button_setting_screen.setObjectName(u"push_button_setting_screen")
        self.push_button_setting_screen.setMinimumSize(QSize(70, 70))
        self.push_button_setting_screen.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.push_button_setting_screen)

        self.push_button_setting_theme = QPushButton(self.widget_setting_setting)
        self.push_button_setting_theme.setObjectName(u"push_button_setting_theme")
        self.push_button_setting_theme.setMinimumSize(QSize(70, 70))
        self.push_button_setting_theme.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.push_button_setting_theme)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.widget_setting_setting)

        self.label_20 = QLabel(self.scrollAreaWidgetContents_37)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font1)
        self.label_20.setStyleSheet(u"background: transparent;")

        self.verticalLayout.addWidget(self.label_20)

        self.widget_setting_update = QWidget(self.scrollAreaWidgetContents_37)
        self.widget_setting_update.setObjectName(u"widget_setting_update")
        self.widget_setting_update.setStyleSheet(u"QWidget {\n"
"border-style: solid;\n"
"border-radius: 10px;\n"
"border: 1px solid white;\n"
"background-color:rgba(255, 255, 255, 200);\n"
"}")
        self.gridLayout_4 = QGridLayout(self.widget_setting_update)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.push_button_setting_version_info = QPushButton(self.widget_setting_update)
        self.push_button_setting_version_info.setObjectName(u"push_button_setting_version_info")
        self.push_button_setting_version_info.setMinimumSize(QSize(70, 70))
        self.push_button_setting_version_info.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.push_button_setting_version_info)

        self.push_button_setting_version = QPushButton(self.widget_setting_update)
        self.push_button_setting_version.setObjectName(u"push_button_setting_version")
        self.push_button_setting_version.setMinimumSize(QSize(70, 70))
        self.push_button_setting_version.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.push_button_setting_version)

        self.push_button_setting_ticket = QPushButton(self.widget_setting_update)
        self.push_button_setting_ticket.setObjectName(u"push_button_setting_ticket")
        self.push_button_setting_ticket.setMinimumSize(QSize(70, 70))
        self.push_button_setting_ticket.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.push_button_setting_ticket)

        self.push_button_setting_feedback_opinion = QPushButton(self.widget_setting_update)
        self.push_button_setting_feedback_opinion.setObjectName(u"push_button_setting_feedback_opinion")
        self.push_button_setting_feedback_opinion.setMinimumSize(QSize(70, 70))
        self.push_button_setting_feedback_opinion.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.push_button_setting_feedback_opinion)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_6)


        self.gridLayout_4.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.widget_setting_update)

        self.label_19 = QLabel(self.scrollAreaWidgetContents_37)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font1)
        self.label_19.setStyleSheet(u"background: transparent;")

        self.verticalLayout.addWidget(self.label_19)

        self.widget_setting_about = QWidget(self.scrollAreaWidgetContents_37)
        self.widget_setting_about.setObjectName(u"widget_setting_about")
        self.widget_setting_about.setStyleSheet(u"QWidget {\n"
"border-style: solid;\n"
"border-radius: 10px;\n"
"border: 1px solid white;\n"
"background-color:rgba(255, 255, 255, 200);\n"
"}")
        self.gridLayout_2 = QGridLayout(self.widget_setting_about)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.push_button_setting_service_agreement = QPushButton(self.widget_setting_about)
        self.push_button_setting_service_agreement.setObjectName(u"push_button_setting_service_agreement")
        self.push_button_setting_service_agreement.setMinimumSize(QSize(70, 70))
        self.push_button_setting_service_agreement.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.push_button_setting_service_agreement)

        self.push_button_setting_privacy_agreement = QPushButton(self.widget_setting_about)
        self.push_button_setting_privacy_agreement.setObjectName(u"push_button_setting_privacy_agreement")
        self.push_button_setting_privacy_agreement.setMinimumSize(QSize(70, 70))
        self.push_button_setting_privacy_agreement.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.push_button_setting_privacy_agreement)

        self.push_button_setting_about_us = QPushButton(self.widget_setting_about)
        self.push_button_setting_about_us.setObjectName(u"push_button_setting_about_us")
        self.push_button_setting_about_us.setMinimumSize(QSize(70, 70))
        self.push_button_setting_about_us.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.push_button_setting_about_us)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.gridLayout_2.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)


        self.verticalLayout.addWidget(self.widget_setting_about)


        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 1, 1, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_5, 0, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 0, 0, 1, 1)

        self.setting_area.setWidget(self.scrollAreaWidgetContents_37)
        self.label_background = QLabel(Form)
        self.label_background.setObjectName(u"label_background")
        self.label_background.setGeometry(QRect(0, 0, 451, 1041))
        self.user_area = QScrollArea(Form)
        self.user_area.setObjectName(u"user_area")
        self.user_area.setGeometry(QRect(480, 480, 1051, 781))
        self.user_area.setStyleSheet(u"border-style:solid; border-radius:10px; border:0px groove gray; color:rgb(0, 0, 0);\n"
"border-color:rgba(255, 255, 255, 0); background-color:rgba(255, 255, 255, 100);")
        self.user_area.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1051, 781))
        self.tab_widget_user = QTabWidget(self.scrollAreaWidgetContents)
        self.tab_widget_user.setObjectName(u"tab_widget_user")
        self.tab_widget_user.setGeometry(QRect(10, 20, 451, 591))
        font2 = QFont()
        font2.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font2.setPointSize(10)
        font2.setBold(False)
        self.tab_widget_user.setFont(font2)
        self.tab_widget_user.setStyleSheet(u"QWidget {\n"
"    background:transparent\n"
"}\n"
"QTabWidget::pane {\n"
"    margin: 10px;\n"
"    background: rgba(255, 255, 255, 150);\n"
"    color: rgb(0, 0, 0);\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"}\n"
"QTabBar::tab {\n"
"    height:24px; \n"
"    min-width: 40px;\n"
"    background: transparent;\n"
"    border-radius: 12px;\n"
"    margin-top: 10px;\n"
"    margin-left: 10px;\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"}\n"
"QTabBar::tab:selected {\n"
"    background: rgba(255, 255, 255, 180);\n"
"    border: 1px solid rgb(120, 120, 120);\n"
"}\n"
"QTabBar::tab:!selected {\n"
"    background: rgba(255, 255, 255, 100);\n"
"}")
        self.tab_widget_user.setTabPosition(QTabWidget.North)
        self.tab_widget_user.setTabShape(QTabWidget.Rounded)
        self.tab_widget_user.setIconSize(QSize(16, 16))
        self.tab_widget_user.setElideMode(Qt.ElideLeft)
        self.tab_widget_user.setUsesScrollButtons(True)
        self.tab_widget_user.setMovable(False)
        self.tab_widget_user.setTabBarAutoHide(False)
        self.tab_11 = QWidget()
        self.tab_11.setObjectName(u"tab_11")
        self.gridLayout_12 = QGridLayout(self.tab_11)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.verticalLayout_18 = QVBoxLayout()
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_16)

        self.label_user_avatar = QLabel(self.tab_11)
        self.label_user_avatar.setObjectName(u"label_user_avatar")
        self.label_user_avatar.setMinimumSize(QSize(91, 91))
        self.label_user_avatar.setMaximumSize(QSize(91, 91))
        self.label_user_avatar.setStyleSheet(u"border-radius: 65px;\n"
"background-color: rgba(255, 255, 255, 0);")
        self.label_user_avatar.setScaledContents(True)

        self.horizontalLayout_20.addWidget(self.label_user_avatar)

        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalSpacer_14 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_16.addItem(self.verticalSpacer_14)

        self.label_area_user_message_nick_name = QLabel(self.tab_11)
        self.label_area_user_message_nick_name.setObjectName(u"label_area_user_message_nick_name")
        self.label_area_user_message_nick_name.setMinimumSize(QSize(160, 0))
        self.label_area_user_message_nick_name.setMaximumSize(QSize(200, 16777215))
        font3 = QFont()
        font3.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font3.setPointSize(11)
        font3.setBold(False)
        self.label_area_user_message_nick_name.setFont(font3)
        self.label_area_user_message_nick_name.setStyleSheet(u"border: none; background-color: transparent;")
        self.label_area_user_message_nick_name.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_16.addWidget(self.label_area_user_message_nick_name)

        self.label_area_user_message_username = QLabel(self.tab_11)
        self.label_area_user_message_username.setObjectName(u"label_area_user_message_username")
        self.label_area_user_message_username.setMinimumSize(QSize(160, 0))
        self.label_area_user_message_username.setMaximumSize(QSize(200, 16777215))
        font4 = QFont()
        font4.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setKerning(False)
        self.label_area_user_message_username.setFont(font4)
        self.label_area_user_message_username.setStyleSheet(u"border: none;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgba(0, 0, 0, 0.5);")
        self.label_area_user_message_username.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_16.addWidget(self.label_area_user_message_username)

        self.verticalSpacer_13 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_16.addItem(self.verticalSpacer_13)


        self.horizontalLayout_20.addLayout(self.verticalLayout_16)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_4)

        self.push_button_area_user_vip_subscription = QPushButton(self.tab_11)
        self.push_button_area_user_vip_subscription.setObjectName(u"push_button_area_user_vip_subscription")
        self.push_button_area_user_vip_subscription.setMinimumSize(QSize(80, 22))
        font5 = QFont()
        font5.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font5.setPointSize(10)
        font5.setBold(True)
        self.push_button_area_user_vip_subscription.setFont(font5)
        self.push_button_area_user_vip_subscription.setStyleSheet(u"QPushButton {\n"
"border-radius:10px;\n"
"background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop:0 rgb(255, 178, 0), stop:1 rgb(254, 232, 67));\n"
"color: white;\n"
"}\n"
"QPushButton:hover {\n"
"background-color: qlineargradient(x1:1, y1:0, x2:0, y2:0,stop:0 rgb(255, 178, 0), stop:1 rgb(254, 232, 67));\n"
"}")

        self.verticalLayout_4.addWidget(self.push_button_area_user_vip_subscription)

        self.label_area_user_vip_info = QLabel(self.tab_11)
        self.label_area_user_vip_info.setObjectName(u"label_area_user_vip_info")
        font6 = QFont()
        font6.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font6.setPointSize(8)
        font6.setBold(False)
        font6.setKerning(False)
        self.label_area_user_vip_info.setFont(font6)
        self.label_area_user_vip_info.setStyleSheet(u"border: 0px solid #FF8D16;\n"
"border-radius: 0px;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(234, 211, 40);")

        self.verticalLayout_4.addWidget(self.label_area_user_vip_info)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_5)


        self.horizontalLayout_20.addLayout(self.verticalLayout_4)

        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_21)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_17)


        self.verticalLayout_18.addLayout(self.horizontalLayout_20)

        self.line_area_user_message = QFrame(self.tab_11)
        self.line_area_user_message.setObjectName(u"line_area_user_message")
        self.line_area_user_message.setMinimumSize(QSize(0, 1))
        self.line_area_user_message.setMaximumSize(QSize(16777215, 1))
        self.line_area_user_message.setStyleSheet(u"color: #000;border-color: #000;background-color: #000;")
        self.line_area_user_message.setFrameShape(QFrame.HLine)
        self.line_area_user_message.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_18.addWidget(self.line_area_user_message)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_18)

        self.widget_area_user_vip_power_bg = QWidget(self.tab_11)
        self.widget_area_user_vip_power_bg.setObjectName(u"widget_area_user_vip_power_bg")
        self.widget_area_user_vip_power_bg.setMinimumSize(QSize(330, 250))
        self.widget_area_user_vip_power_bg.setMaximumSize(QSize(330, 250))
        self.widget_area_user_vip_power_bg.setStyleSheet(u"background-color: qlineargradient(x1:0, y1:1, x2:0, y2:0,stop:0 rgb(205, 232, 255), stop:1 rgb(71, 153, 253));")
        self.gridLayout_11 = QGridLayout(self.widget_area_user_vip_power_bg)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_area_user_vip_icon = QLabel(self.widget_area_user_vip_power_bg)
        self.label_area_user_vip_icon.setObjectName(u"label_area_user_vip_icon")
        self.label_area_user_vip_icon.setMinimumSize(QSize(30, 30))
        self.label_area_user_vip_icon.setMaximumSize(QSize(30, 30))
        self.label_area_user_vip_icon.setStyleSheet(u"border-radius: 65px;\n"
"background-color: rgba(255, 255, 255, 0);")
        self.label_area_user_vip_icon.setScaledContents(True)

        self.horizontalLayout_18.addWidget(self.label_area_user_vip_icon)

        self.label_user_login_title_14 = QLabel(self.widget_area_user_vip_power_bg)
        self.label_user_login_title_14.setObjectName(u"label_user_login_title_14")
        font7 = QFont()
        font7.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font7.setPointSize(14)
        font7.setBold(True)
        font7.setItalic(True)
        self.label_user_login_title_14.setFont(font7)
        self.label_user_login_title_14.setStyleSheet(u"border: 0px solid #FF8D16;\n"
"border-radius: 0px;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(254, 232, 67);")
        self.label_user_login_title_14.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_18.addWidget(self.label_user_login_title_14)


        self.verticalLayout_14.addLayout(self.horizontalLayout_18)


        self.horizontalLayout_19.addLayout(self.verticalLayout_14)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_15)


        self.verticalLayout_15.addLayout(self.horizontalLayout_19)

        self.label_area_user_vip_info_2 = QLabel(self.widget_area_user_vip_power_bg)
        self.label_area_user_vip_info_2.setObjectName(u"label_area_user_vip_info_2")
        self.label_area_user_vip_info_2.setFont(font6)
        self.label_area_user_vip_info_2.setStyleSheet(u"border: 0px solid #FF8D16;\n"
"border-radius: 0px;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(254, 232, 67);")

        self.verticalLayout_15.addWidget(self.label_area_user_vip_info_2)

        self.widget_area_user_vip_power_content = QWidget(self.widget_area_user_vip_power_bg)
        self.widget_area_user_vip_power_content.setObjectName(u"widget_area_user_vip_power_content")
        self.widget_area_user_vip_power_content.setMinimumSize(QSize(300, 160))
        self.widget_area_user_vip_power_content.setMaximumSize(QSize(500, 160))
        self.widget_area_user_vip_power_content.setStyleSheet(u"background-color: white;")
        self.gridLayout_10 = QGridLayout(self.widget_area_user_vip_power_content)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.push_button_area_user_vip_power_1 = QPushButton(self.widget_area_user_vip_power_content)
        self.push_button_area_user_vip_power_1.setObjectName(u"push_button_area_user_vip_power_1")
        self.push_button_area_user_vip_power_1.setMinimumSize(QSize(40, 40))
        self.push_button_area_user_vip_power_1.setMaximumSize(QSize(40, 40))
        self.push_button_area_user_vip_power_1.setFont(font5)
        self.push_button_area_user_vip_power_1.setStyleSheet(u"border: 0px solid white;\n"
"border-radius: 20px;\n"
"background-color: qlineargradient(x1:0, y1:1, x2:0, y2:0,stop:0 rgb(205, 232, 255), stop:1 rgb(71, 153, 253));")
        self.push_button_area_user_vip_power_1.setIconSize(QSize(20, 20))

        self.horizontalLayout_10.addWidget(self.push_button_area_user_vip_power_1)


        self.verticalLayout_7.addLayout(self.horizontalLayout_10)

        self.label_27 = QLabel(self.widget_area_user_vip_power_content)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setAlignment(Qt.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_27)


        self.horizontalLayout_16.addLayout(self.verticalLayout_7)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.push_button_area_user_vip_power_2 = QPushButton(self.widget_area_user_vip_power_content)
        self.push_button_area_user_vip_power_2.setObjectName(u"push_button_area_user_vip_power_2")
        self.push_button_area_user_vip_power_2.setMinimumSize(QSize(40, 40))
        self.push_button_area_user_vip_power_2.setMaximumSize(QSize(40, 40))
        self.push_button_area_user_vip_power_2.setFont(font5)
        self.push_button_area_user_vip_power_2.setStyleSheet(u"border: 0px solid white;\n"
"border-radius: 20px;\n"
"background-color: qlineargradient(x1:0, y1:1, x2:0, y2:0,stop:0 rgb(205, 232, 255), stop:1 rgb(71, 153, 253));")
        self.push_button_area_user_vip_power_2.setIconSize(QSize(20, 20))

        self.horizontalLayout_12.addWidget(self.push_button_area_user_vip_power_2)


        self.verticalLayout_9.addLayout(self.horizontalLayout_12)

        self.label_30 = QLabel(self.widget_area_user_vip_power_content)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setAlignment(Qt.AlignCenter)

        self.verticalLayout_9.addWidget(self.label_30)


        self.horizontalLayout_16.addLayout(self.verticalLayout_9)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.push_button_area_user_vip_power_3 = QPushButton(self.widget_area_user_vip_power_content)
        self.push_button_area_user_vip_power_3.setObjectName(u"push_button_area_user_vip_power_3")
        self.push_button_area_user_vip_power_3.setMinimumSize(QSize(40, 40))
        self.push_button_area_user_vip_power_3.setMaximumSize(QSize(40, 40))
        self.push_button_area_user_vip_power_3.setFont(font5)
        self.push_button_area_user_vip_power_3.setStyleSheet(u"border: 0px solid white;\n"
"border-radius: 20px;\n"
"background-color: qlineargradient(x1:0, y1:1, x2:0, y2:0,stop:0 rgb(205, 232, 255), stop:1 rgb(71, 153, 253));")
        self.push_button_area_user_vip_power_3.setIconSize(QSize(20, 20))

        self.horizontalLayout_11.addWidget(self.push_button_area_user_vip_power_3)


        self.verticalLayout_8.addLayout(self.horizontalLayout_11)

        self.label_29 = QLabel(self.widget_area_user_vip_power_content)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.label_29)


        self.horizontalLayout_16.addLayout(self.verticalLayout_8)


        self.verticalLayout_13.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.push_button_area_user_vip_power_4 = QPushButton(self.widget_area_user_vip_power_content)
        self.push_button_area_user_vip_power_4.setObjectName(u"push_button_area_user_vip_power_4")
        self.push_button_area_user_vip_power_4.setMinimumSize(QSize(40, 40))
        self.push_button_area_user_vip_power_4.setMaximumSize(QSize(40, 40))
        self.push_button_area_user_vip_power_4.setFont(font5)
        self.push_button_area_user_vip_power_4.setStyleSheet(u"border: 0px solid white;\n"
"border-radius: 20px;\n"
"background-color: qlineargradient(x1:0, y1:1, x2:0, y2:0,stop:0 rgb(205, 232, 255), stop:1 rgb(71, 153, 253));")
        self.push_button_area_user_vip_power_4.setIconSize(QSize(20, 20))

        self.horizontalLayout_14.addWidget(self.push_button_area_user_vip_power_4)


        self.verticalLayout_11.addLayout(self.horizontalLayout_14)

        self.label_32 = QLabel(self.widget_area_user_vip_power_content)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setAlignment(Qt.AlignCenter)

        self.verticalLayout_11.addWidget(self.label_32)


        self.horizontalLayout_17.addLayout(self.verticalLayout_11)

        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.push_button_area_user_vip_power_5 = QPushButton(self.widget_area_user_vip_power_content)
        self.push_button_area_user_vip_power_5.setObjectName(u"push_button_area_user_vip_power_5")
        self.push_button_area_user_vip_power_5.setMinimumSize(QSize(40, 40))
        self.push_button_area_user_vip_power_5.setMaximumSize(QSize(40, 40))
        self.push_button_area_user_vip_power_5.setFont(font5)
        self.push_button_area_user_vip_power_5.setStyleSheet(u"border: 0px solid white;\n"
"border-radius: 20px;\n"
"background-color: qlineargradient(x1:0, y1:1, x2:0, y2:0,stop:0 rgb(205, 232, 255), stop:1 rgb(71, 153, 253));")
        self.push_button_area_user_vip_power_5.setIconSize(QSize(20, 20))

        self.horizontalLayout_15.addWidget(self.push_button_area_user_vip_power_5)


        self.verticalLayout_12.addLayout(self.horizontalLayout_15)

        self.label_33 = QLabel(self.widget_area_user_vip_power_content)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setAlignment(Qt.AlignCenter)

        self.verticalLayout_12.addWidget(self.label_33)


        self.horizontalLayout_17.addLayout(self.verticalLayout_12)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.push_button_area_user_vip_power_6 = QPushButton(self.widget_area_user_vip_power_content)
        self.push_button_area_user_vip_power_6.setObjectName(u"push_button_area_user_vip_power_6")
        self.push_button_area_user_vip_power_6.setMinimumSize(QSize(40, 40))
        self.push_button_area_user_vip_power_6.setMaximumSize(QSize(40, 40))
        self.push_button_area_user_vip_power_6.setFont(font5)
        self.push_button_area_user_vip_power_6.setStyleSheet(u"border: 0px solid white;\n"
"border-radius: 20px;\n"
"background-color: qlineargradient(x1:0, y1:1, x2:0, y2:0,stop:0 rgb(205, 232, 255), stop:1 rgb(71, 153, 253));")
        self.push_button_area_user_vip_power_6.setIconSize(QSize(20, 20))

        self.horizontalLayout_13.addWidget(self.push_button_area_user_vip_power_6)


        self.verticalLayout_10.addLayout(self.horizontalLayout_13)

        self.label_31 = QLabel(self.widget_area_user_vip_power_content)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setAlignment(Qt.AlignCenter)

        self.verticalLayout_10.addWidget(self.label_31)


        self.horizontalLayout_17.addLayout(self.verticalLayout_10)


        self.verticalLayout_13.addLayout(self.horizontalLayout_17)


        self.gridLayout_10.addLayout(self.verticalLayout_13, 0, 0, 1, 1)


        self.verticalLayout_15.addWidget(self.widget_area_user_vip_power_content)


        self.gridLayout_11.addLayout(self.verticalLayout_15, 0, 0, 1, 1)


        self.horizontalLayout_21.addWidget(self.widget_area_user_vip_power_bg)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_19)


        self.verticalLayout_18.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_7)

        self.widget_area_user_invite_bg = QWidget(self.tab_11)
        self.widget_area_user_invite_bg.setObjectName(u"widget_area_user_invite_bg")
        self.widget_area_user_invite_bg.setMinimumSize(QSize(330, 0))
        self.widget_area_user_invite_bg.setMaximumSize(QSize(330, 250))
        self.widget_area_user_invite_bg.setStyleSheet(u"background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 rgb(205, 232, 255), stop:1 rgb(71, 153, 253));")
        self.gridLayout_14 = QGridLayout(self.widget_area_user_invite_bg)
        self.gridLayout_14.setSpacing(0)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.verticalLayout_19 = QVBoxLayout()
        self.verticalLayout_19.setSpacing(0)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setSpacing(0)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.verticalLayout_20 = QVBoxLayout()
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.label_area_user_invite_icon = QLabel(self.widget_area_user_invite_bg)
        self.label_area_user_invite_icon.setObjectName(u"label_area_user_invite_icon")
        self.label_area_user_invite_icon.setMinimumSize(QSize(30, 30))
        self.label_area_user_invite_icon.setMaximumSize(QSize(30, 30))
        self.label_area_user_invite_icon.setStyleSheet(u"border-radius: 65px;\n"
"background-color: rgba(255, 255, 255, 0);")
        self.label_area_user_invite_icon.setScaledContents(True)

        self.horizontalLayout_24.addWidget(self.label_area_user_invite_icon)

        self.label_user_login_invite_title = QLabel(self.widget_area_user_invite_bg)
        self.label_user_login_invite_title.setObjectName(u"label_user_login_invite_title")
        font8 = QFont()
        font8.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font8.setPointSize(12)
        font8.setBold(True)
        font8.setItalic(True)
        self.label_user_login_invite_title.setFont(font8)
        self.label_user_login_invite_title.setStyleSheet(u"border: 0px solid #FF8D16;\n"
"border-radius: 0px;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(0, 0, 0);")
        self.label_user_login_invite_title.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_24.addWidget(self.label_user_login_invite_title)


        self.verticalLayout_20.addLayout(self.horizontalLayout_24)


        self.horizontalLayout_23.addLayout(self.verticalLayout_20)

        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_22)

        self.push_button_area_user_invite_code = QPushButton(self.widget_area_user_invite_bg)
        self.push_button_area_user_invite_code.setObjectName(u"push_button_area_user_invite_code")
        self.push_button_area_user_invite_code.setMinimumSize(QSize(80, 22))
        font9 = QFont()
        font9.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font9.setPointSize(9)
        font9.setBold(True)
        self.push_button_area_user_invite_code.setFont(font9)
        self.push_button_area_user_invite_code.setStyleSheet(u"QPushButton {\n"
"border-radius:10px;\n"
"background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop:0 rgb(0, 145, 255), stop:1 rgb(92, 22, 255));\n"
"color: white;\n"
"}\n"
"QPushButton:hover {\n"
"background-color: qlineargradient(x1:1, y1:0, x2:0, y2:0,stop:0 rgb(0, 145, 255), stop:1 rgb(92, 22, 255));\n"
"}")

        self.horizontalLayout_23.addWidget(self.push_button_area_user_invite_code)


        self.verticalLayout_19.addLayout(self.horizontalLayout_23)

        self.label_area_user_invite_info = QLabel(self.widget_area_user_invite_bg)
        self.label_area_user_invite_info.setObjectName(u"label_area_user_invite_info")
        self.label_area_user_invite_info.setFont(font6)
        self.label_area_user_invite_info.setStyleSheet(u"border: 0px solid #FF8D16;\n"
"border-radius: 0px;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(0, 0, 0);")

        self.verticalLayout_19.addWidget(self.label_area_user_invite_info)


        self.gridLayout_14.addLayout(self.verticalLayout_19, 0, 0, 1, 1)


        self.horizontalLayout_2.addWidget(self.widget_area_user_invite_bg)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_18.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_18.addItem(self.verticalSpacer_6)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_20)

        self.widget_3 = QWidget(self.tab_11)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(70, 56))
        self.widget_3.setMaximumSize(QSize(70, 56))
        self.push_button_area_user_message_logout = QPushButton(self.widget_3)
        self.push_button_area_user_message_logout.setObjectName(u"push_button_area_user_message_logout")
        self.push_button_area_user_message_logout.setGeometry(QRect(14, 3, 40, 40))
        self.push_button_area_user_message_logout.setFont(font5)
        self.push_button_area_user_message_logout.setStyleSheet(u"border: 1px solid black; border-radius: 20px;")
        self.push_button_area_user_message_logout.setIconSize(QSize(20, 20))
        self.label_area_user_message_logout = QLabel(self.widget_3)
        self.label_area_user_message_logout.setObjectName(u"label_area_user_message_logout")
        self.label_area_user_message_logout.setGeometry(QRect(4, 36, 61, 18))
        self.label_area_user_message_logout.setStyleSheet(u"background: black;color:white;border-radius: 8px; padding:2px;")

        self.horizontalLayout_22.addWidget(self.widget_3)


        self.verticalLayout_18.addLayout(self.horizontalLayout_22)


        self.gridLayout_12.addLayout(self.verticalLayout_18, 0, 0, 2, 2)

        self.tab_widget_user.addTab(self.tab_11, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.label_user_last_backup_time_title = QLabel(self.tab_5)
        self.label_user_last_backup_time_title.setObjectName(u"label_user_last_backup_time_title")
        self.label_user_last_backup_time_title.setGeometry(QRect(40, 30, 61, 21))
        font10 = QFont()
        font10.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font10.setBold(False)
        font10.setKerning(False)
        self.label_user_last_backup_time_title.setFont(font10)
        self.label_user_last_backup_time_title.setStyleSheet(u"border: 0px solid #FF8D16;\n"
"border-radius: 0px;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgba(0, 0, 0, 0.5);")
        self.widget_area_user_data_server = QWidget(self.tab_5)
        self.widget_area_user_data_server.setObjectName(u"widget_area_user_data_server")
        self.widget_area_user_data_server.setGeometry(QRect(30, 130, 321, 71))
        self.widget_area_user_data_server.setStyleSheet(u"QWidget {\n"
"border-style: solid;\n"
"border-radius: 10px;\n"
"border: 1px solid white;\n"
"background-color:rgba(255, 255, 255, 200);\n"
"}")
        self.gridLayout_5 = QGridLayout(self.widget_area_user_data_server)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.push_button_area_user_data_backup = QPushButton(self.widget_area_user_data_server)
        self.push_button_area_user_data_backup.setObjectName(u"push_button_area_user_data_backup")
        self.push_button_area_user_data_backup.setFont(font5)
        self.push_button_area_user_data_backup.setStyleSheet(u"QPushButton {\n"
"border: none;\n"
"background: rgba(0, 0, 0, 0);\n"
"text-align:left;\n"
"}\n"
"QPushButton:hover {\n"
"font-weight: bold;\n"
"}")

        self.verticalLayout_2.addWidget(self.push_button_area_user_data_backup)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.push_button_area_user_data_recover = QPushButton(self.widget_area_user_data_server)
        self.push_button_area_user_data_recover.setObjectName(u"push_button_area_user_data_recover")
        self.push_button_area_user_data_recover.setFont(font5)
        self.push_button_area_user_data_recover.setStyleSheet(u"QPushButton {\n"
"border: none;\n"
"background: rgba(0, 0, 0, 0);\n"
"text-align:left;\n"
"}\n"
"QPushButton:hover {\n"
"font-weight: bold;\n"
"}")

        self.verticalLayout_2.addWidget(self.push_button_area_user_data_recover)


        self.gridLayout_5.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.widget_area_user_data_local = QWidget(self.tab_5)
        self.widget_area_user_data_local.setObjectName(u"widget_area_user_data_local")
        self.widget_area_user_data_local.setGeometry(QRect(30, 230, 321, 71))
        self.widget_area_user_data_local.setStyleSheet(u"QWidget {\n"
"border-style: solid;\n"
"border-radius: 10px;\n"
"border: 1px solid white;\n"
"background-color:rgba(255, 255, 255, 200);\n"
"}")
        self.gridLayout_6 = QGridLayout(self.widget_area_user_data_local)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.push_button_area_user_data_import = QPushButton(self.widget_area_user_data_local)
        self.push_button_area_user_data_import.setObjectName(u"push_button_area_user_data_import")
        self.push_button_area_user_data_import.setFont(font5)
        self.push_button_area_user_data_import.setStyleSheet(u"QPushButton {\n"
"border: none;\n"
"background: rgba(0, 0, 0, 0);\n"
"text-align:left;\n"
"}\n"
"QPushButton:hover {\n"
"font-weight: bold;\n"
"}")

        self.verticalLayout_3.addWidget(self.push_button_area_user_data_import)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.push_button_area_user_data_export = QPushButton(self.widget_area_user_data_local)
        self.push_button_area_user_data_export.setObjectName(u"push_button_area_user_data_export")
        self.push_button_area_user_data_export.setFont(font5)
        self.push_button_area_user_data_export.setStyleSheet(u"QPushButton {\n"
"border: none;\n"
"background: rgba(0, 0, 0, 0);\n"
"text-align:left;\n"
"}\n"
"QPushButton:hover {\n"
"font-weight: bold;\n"
"}")

        self.verticalLayout_3.addWidget(self.push_button_area_user_data_export)


        self.gridLayout_6.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.widget_area_user_data_sync = QWidget(self.tab_5)
        self.widget_area_user_data_sync.setObjectName(u"widget_area_user_data_sync")
        self.widget_area_user_data_sync.setGeometry(QRect(30, 60, 321, 41))
        self.widget_area_user_data_sync.setStyleSheet(u"QWidget {\n"
"border-style: solid;\n"
"border-radius: 10px;\n"
"border: 1px solid white;\n"
"background-color:rgba(255, 255, 255, 200);\n"
"}")
        self.gridLayout_8 = QGridLayout(self.widget_area_user_data_sync)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.push_button_area_user_data_synchronization = QPushButton(self.widget_area_user_data_sync)
        self.push_button_area_user_data_synchronization.setObjectName(u"push_button_area_user_data_synchronization")
        self.push_button_area_user_data_synchronization.setFont(font5)
        self.push_button_area_user_data_synchronization.setStyleSheet(u"QPushButton {\n"
"border: none;\n"
"background: rgba(0, 0, 0, 0);\n"
"text-align:left;\n"
"}\n"
"QPushButton:hover {\n"
"font-weight: bold;\n"
"}")

        self.verticalLayout_5.addWidget(self.push_button_area_user_data_synchronization)


        self.gridLayout_8.addLayout(self.verticalLayout_5, 0, 0, 1, 1)

        self.label_user_last_backup_time = QLabel(self.tab_5)
        self.label_user_last_backup_time.setObjectName(u"label_user_last_backup_time")
        self.label_user_last_backup_time.setGeometry(QRect(100, 30, 241, 21))
        self.label_user_last_backup_time.setFont(font10)
        self.label_user_last_backup_time.setStyleSheet(u"border: 0px solid #FF8D16;\n"
"border-radius: 0px;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgba(0, 0, 0, 0.5);")
        self.widget_area_user_communicate = QWidget(self.tab_5)
        self.widget_area_user_communicate.setObjectName(u"widget_area_user_communicate")
        self.widget_area_user_communicate.setGeometry(QRect(30, 330, 321, 41))
        self.widget_area_user_communicate.setStyleSheet(u"QWidget {\n"
"border-style: solid;\n"
"border-radius: 10px;\n"
"border: 1px solid white;\n"
"background-color:rgba(255, 255, 255, 200);\n"
"}")
        self.gridLayout_13 = QGridLayout(self.widget_area_user_communicate)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.verticalLayout_17 = QVBoxLayout()
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.push_button_area_user_join_group = QPushButton(self.widget_area_user_communicate)
        self.push_button_area_user_join_group.setObjectName(u"push_button_area_user_join_group")
        self.push_button_area_user_join_group.setFont(font5)
        self.push_button_area_user_join_group.setStyleSheet(u"QPushButton {\n"
"border: none;\n"
"background: rgba(0, 0, 0, 0);\n"
"text-align:left;\n"
"}\n"
"QPushButton:hover {\n"
"font-weight: bold;\n"
"}")

        self.verticalLayout_17.addWidget(self.push_button_area_user_join_group)


        self.gridLayout_13.addLayout(self.verticalLayout_17, 0, 0, 1, 1)

        self.tab_widget_user.addTab(self.tab_5, "")
        self.user_area.setWidget(self.scrollAreaWidgetContents)
        self.label_background.raise_()
        self.setting_area.raise_()
        self.user_area.raise_()

        self.retranslateUi(Form)

        self.tab_widget_user.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_17.setText(QCoreApplication.translate("Form", u"\u8bbe\u7f6e\u76f8\u5173", None))
        self.push_button_setting_system.setText(QCoreApplication.translate("Form", u"\u7cfb\u7edf\u8bbe\u7f6e", None))
        self.push_button_setting_card_permutation.setText(QCoreApplication.translate("Form", u"\u5361\u7247\u8bbe\u8ba1", None))
        self.push_button_setting_screen.setText(QCoreApplication.translate("Form", u"\u754c\u9762\u8bbe\u7f6e", None))
        self.push_button_setting_theme.setText(QCoreApplication.translate("Form", u"\u4e3b\u9898\u8bbe\u7f6e", None))
        self.label_20.setText(QCoreApplication.translate("Form", u"\u95ee\u9898\u548c\u66f4\u65b0", None))
        self.push_button_setting_version_info.setText(QCoreApplication.translate("Form", u"\u7248\u672c\u4fe1\u606f", None))
        self.push_button_setting_version.setText(QCoreApplication.translate("Form", u"\u68c0\u6d4b\u66f4\u65b0", None))
        self.push_button_setting_ticket.setText(QCoreApplication.translate("Form", u"\u4f1a\u5458\u5de5\u5355", None))
        self.push_button_setting_feedback_opinion.setText(QCoreApplication.translate("Form", u"\u610f\u89c1\u53cd\u9988", None))
        self.label_19.setText(QCoreApplication.translate("Form", u"\u5173\u4e8e", None))
        self.push_button_setting_service_agreement.setText(QCoreApplication.translate("Form", u"\u670d\u52a1\u534f\u8bae", None))
        self.push_button_setting_privacy_agreement.setText(QCoreApplication.translate("Form", u"\u9690\u79c1\u534f\u8bae", None))
        self.push_button_setting_about_us.setText(QCoreApplication.translate("Form", u"\u5173\u4e8e\u6211\u4eec", None))
        self.label_background.setText("")
        self.label_user_avatar.setText("")
        self.label_area_user_message_nick_name.setText(QCoreApplication.translate("Form", u"\u6635\u79f0", None))
        self.label_area_user_message_username.setText(QCoreApplication.translate("Form", u"\u7528\u6237\u540d", None))
        self.push_button_area_user_vip_subscription.setText(QCoreApplication.translate("Form", u"\u7eed\u8d39", None))
        self.label_area_user_vip_info.setText(QCoreApplication.translate("Form", u"\u6709\u6548\u671f:9999-01-01", None))
        self.label_area_user_vip_icon.setText("")
        self.label_user_login_title_14.setText(QCoreApplication.translate("Form", u"\u4f1a\u5458\u6743\u76ca", None))
        self.label_area_user_vip_info_2.setText(QCoreApplication.translate("Form", u"\u5f00\u901a\u4f1a\u5458\u4eab\u53d7\u6570\u636e\u540c\u6b65\u7b49\u591a\u9879\u670d\u52a1", None))
        self.push_button_area_user_vip_power_1.setText("")
        self.label_27.setText(QCoreApplication.translate("Form", u"\u4e91\u7aef\u6570\u636e\u5907\u4efd", None))
        self.push_button_area_user_vip_power_2.setText("")
        self.label_30.setText(QCoreApplication.translate("Form", u"\u6570\u636e\u591a\u7aef\u540c\u6b65", None))
        self.push_button_area_user_vip_power_3.setText("")
        self.label_29.setText(QCoreApplication.translate("Form", u"AI\u5927\u6a21\u578b\u5bf9\u8bdd", None))
        self.push_button_area_user_vip_power_4.setText("")
        self.label_32.setText(QCoreApplication.translate("Form", u"\u591a\u8bed\u8a00\u7ffb\u8bd1\u529f\u80fd", None))
        self.push_button_area_user_vip_power_5.setText("")
        self.label_33.setText(QCoreApplication.translate("Form", u"\u4e13\u5c5e\u5de5\u5355\u7cfb\u7edf", None))
        self.push_button_area_user_vip_power_6.setText("")
        self.label_31.setText(QCoreApplication.translate("Form", u"\u4f1a\u5458\u5c0a\u4eab\u6807\u8bc6", None))
        self.label_area_user_invite_icon.setText("")
        self.label_user_login_invite_title.setText(QCoreApplication.translate("Form", u" \u9080\u8bf7\u7528\u6237", None))
        self.push_button_area_user_invite_code.setText(QCoreApplication.translate("Form", u"\u590d\u5236\u9080\u8bf7\u7801", None))
        self.label_area_user_invite_info.setText(QCoreApplication.translate("Form", u"\u9080\u8bf7\u65b0\u7528\u6237\u53cc\u65b9\u5747\u53ef\u83b7\u5f97\u4e03\u5929\u5468\u5361\u4f1a\u5458\u54e6~", None))
        self.push_button_area_user_message_logout.setText("")
        self.label_area_user_message_logout.setText(QCoreApplication.translate("Form", u"\u9000\u51fa\u767b\u5f55", None))
        self.tab_widget_user.setTabText(self.tab_widget_user.indexOf(self.tab_11), QCoreApplication.translate("Form", u"\u8d26\u53f7", None))
        self.label_user_last_backup_time_title.setText(QCoreApplication.translate("Form", u"\u4e0a\u6b21\u540c\u6b65\uff1a", None))
        self.push_button_area_user_data_backup.setText(QCoreApplication.translate("Form", u"\u7acb\u5373\u5907\u4efd\u5230\u4e91\u7aef", None))
        self.push_button_area_user_data_recover.setText(QCoreApplication.translate("Form", u"\u6062\u590d\u5386\u53f2\u6570\u636e", None))
        self.push_button_area_user_data_import.setText(QCoreApplication.translate("Form", u"\u4ece\u672c\u5730\u5bfc\u5165\u6570\u636e", None))
        self.push_button_area_user_data_export.setText(QCoreApplication.translate("Form", u"\u5bfc\u51fa\u6570\u636e\u5230\u672c\u5730", None))
        self.push_button_area_user_data_synchronization.setText(QCoreApplication.translate("Form", u"\u4ece\u4e91\u7aef\u540c\u6b65\u6570\u636e\u5230\u672c\u5730", None))
        self.label_user_last_backup_time.setText(QCoreApplication.translate("Form", u"\u975eVIP\u7528\u6237\u6682\u4e0d\u652f\u6301\u540c\u6b65", None))
        self.push_button_area_user_join_group.setText(QCoreApplication.translate("Form", u"\u52a0\u5165\u7528\u6237\u4ea4\u6d41\u7fa4", None))
        self.tab_widget_user.setTabText(self.tab_widget_user.indexOf(self.tab_5), QCoreApplication.translate("Form", u"\u6570\u636e", None))
    # retranslateUi

