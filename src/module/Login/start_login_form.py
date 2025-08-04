# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'start_login_form.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(498, 762)
        self.gridLayout_8 = QGridLayout(Form)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tab_widget_login = QTabWidget(Form)
        self.tab_widget_login.setObjectName(u"tab_widget_login")
        font = QFont()
        font.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font.setPointSize(10)
        font.setBold(False)
        self.tab_widget_login.setFont(font)
        self.tab_widget_login.setStyleSheet(u"QWidget {\n"
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
        self.tab_widget_login.setTabPosition(QTabWidget.North)
        self.tab_widget_login.setTabShape(QTabWidget.Rounded)
        self.tab_widget_login.setIconSize(QSize(16, 16))
        self.tab_widget_login.setElideMode(Qt.ElideLeft)
        self.tab_widget_login.setUsesScrollButtons(True)
        self.tab_widget_login.setMovable(False)
        self.tab_widget_login.setTabBarAutoHide(False)
        self.tab_12 = QWidget()
        self.tab_12.setObjectName(u"tab_12")
        self.gridLayout_9 = QGridLayout(self.tab_12)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(20, -1, 20, -1)
        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_5)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_12)

        self.label_user_login_logo = QLabel(self.tab_12)
        self.label_user_login_logo.setObjectName(u"label_user_login_logo")
        self.label_user_login_logo.setMinimumSize(QSize(46, 46))
        self.label_user_login_logo.setMaximumSize(QSize(46, 46))
        self.label_user_login_logo.setScaledContents(True)

        self.horizontalLayout_8.addWidget(self.label_user_login_logo)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_11)


        self.verticalLayout_6.addLayout(self.horizontalLayout_8)

        self.label_user_login_top_space = QLabel(self.tab_12)
        self.label_user_login_top_space.setObjectName(u"label_user_login_top_space")
        self.label_user_login_top_space.setMinimumSize(QSize(0, 94))
        self.label_user_login_top_space.setMaximumSize(QSize(16777215, 94))

        self.verticalLayout_6.addWidget(self.label_user_login_top_space)

        self.label_user_login_title_2 = QLabel(self.tab_12)
        self.label_user_login_title_2.setObjectName(u"label_user_login_title_2")
        self.label_user_login_title_2.setFont(font)
        self.label_user_login_title_2.setStyleSheet(u"border: 0px solid #FF8D16;\n"
"border-radius: 0px;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.label_user_login_title_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_6.addWidget(self.label_user_login_title_2)

        self.line_edit_user_login_username = QLineEdit(self.tab_12)
        self.line_edit_user_login_username.setObjectName(u"line_edit_user_login_username")
        self.line_edit_user_login_username.setMinimumSize(QSize(0, 25))
        font1 = QFont()
        font1.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font1.setPointSize(12)
        font1.setBold(True)
        self.line_edit_user_login_username.setFont(font1)
        self.line_edit_user_login_username.setStyleSheet(u"")
        self.line_edit_user_login_username.setMaxLength(20)

        self.verticalLayout_6.addWidget(self.line_edit_user_login_username)

        self.label_user_login_username_prompt = QLabel(self.tab_12)
        self.label_user_login_username_prompt.setObjectName(u"label_user_login_username_prompt")
        self.label_user_login_username_prompt.setMinimumSize(QSize(0, 15))
        self.label_user_login_username_prompt.setMaximumSize(QSize(16777215, 15))
        font2 = QFont()
        font2.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font2.setPointSize(8)
        self.label_user_login_username_prompt.setFont(font2)
        self.label_user_login_username_prompt.setStyleSheet(u"border: none; background-color: transparent;")

        self.verticalLayout_6.addWidget(self.label_user_login_username_prompt)

        self.label_user_login_title_3 = QLabel(self.tab_12)
        self.label_user_login_title_3.setObjectName(u"label_user_login_title_3")
        self.label_user_login_title_3.setFont(font)
        self.label_user_login_title_3.setStyleSheet(u"border: 0px solid #FF8D16;\n"
"border-radius: 0px;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.label_user_login_title_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_6.addWidget(self.label_user_login_title_3)

        self.line_edit_user_login_password_widget = QWidget(self.tab_12)
        self.line_edit_user_login_password_widget.setObjectName(u"line_edit_user_login_password_widget")
        self.gridLayout = QGridLayout(self.line_edit_user_login_password_widget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.line_edit_user_login_password = QLineEdit(self.line_edit_user_login_password_widget)
        self.line_edit_user_login_password.setObjectName(u"line_edit_user_login_password")
        self.line_edit_user_login_password.setMinimumSize(QSize(0, 25))
        self.line_edit_user_login_password.setFont(font1)
        self.line_edit_user_login_password.setStyleSheet(u"")
        self.line_edit_user_login_password.setMaxLength(20)
        self.line_edit_user_login_password.setEchoMode(QLineEdit.Password)

        self.horizontalLayout.addWidget(self.line_edit_user_login_password)

        self.push_button_user_login_password_view_control = QPushButton(self.line_edit_user_login_password_widget)
        self.push_button_user_login_password_view_control.setObjectName(u"push_button_user_login_password_view_control")
        self.push_button_user_login_password_view_control.setMinimumSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.push_button_user_login_password_view_control)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.verticalLayout_6.addWidget(self.line_edit_user_login_password_widget)

        self.label_user_login_password_prompt = QLabel(self.tab_12)
        self.label_user_login_password_prompt.setObjectName(u"label_user_login_password_prompt")
        self.label_user_login_password_prompt.setMinimumSize(QSize(0, 15))
        self.label_user_login_password_prompt.setMaximumSize(QSize(16777215, 15))
        self.label_user_login_password_prompt.setFont(font2)
        self.label_user_login_password_prompt.setStyleSheet(u"border: none; background-color: transparent;")

        self.verticalLayout_6.addWidget(self.label_user_login_password_prompt)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_6)

        self.push_button_user_login_forget_password = QPushButton(self.tab_12)
        self.push_button_user_login_forget_password.setObjectName(u"push_button_user_login_forget_password")
        self.push_button_user_login_forget_password.setMinimumSize(QSize(75, 25))
        font3 = QFont()
        font3.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setKerning(False)
        self.push_button_user_login_forget_password.setFont(font3)
        self.push_button_user_login_forget_password.setLayoutDirection(Qt.LeftToRight)
        self.push_button_user_login_forget_password.setStyleSheet(u"border: 0px solid #FF8D16;\n"
"border-radius: 0px;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgba(0, 0, 0, 0.5);")

        self.horizontalLayout_5.addWidget(self.push_button_user_login_forget_password)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)

        self.label_user_login_bottom_space = QLabel(self.tab_12)
        self.label_user_login_bottom_space.setObjectName(u"label_user_login_bottom_space")
        self.label_user_login_bottom_space.setMinimumSize(QSize(0, 91))
        self.label_user_login_bottom_space.setMaximumSize(QSize(16777215, 91))

        self.verticalLayout_6.addWidget(self.label_user_login_bottom_space)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_8)

        self.push_button_user_login = QPushButton(self.tab_12)
        self.push_button_user_login.setObjectName(u"push_button_user_login")
        self.push_button_user_login.setMinimumSize(QSize(120, 40))
        font4 = QFont()
        font4.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font4.setPointSize(11)
        font4.setBold(True)
        self.push_button_user_login.setFont(font4)
        self.push_button_user_login.setStyleSheet(u"")

        self.horizontalLayout_6.addWidget(self.push_button_user_login)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_7)


        self.verticalLayout_6.addLayout(self.horizontalLayout_6)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_6)


        self.gridLayout_9.addLayout(self.verticalLayout_6, 0, 0, 1, 1)

        self.tab_widget_login.addTab(self.tab_12, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.gridLayout_7 = QGridLayout(self.tab_6)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(20, -1, 20, -1)
        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_7)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_14)

        self.label_user_register_logo = QLabel(self.tab_6)
        self.label_user_register_logo.setObjectName(u"label_user_register_logo")
        self.label_user_register_logo.setMinimumSize(QSize(46, 46))
        self.label_user_register_logo.setMaximumSize(QSize(46, 46))
        self.label_user_register_logo.setScaledContents(True)

        self.horizontalLayout_9.addWidget(self.label_user_register_logo)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_13)


        self.verticalLayout_4.addLayout(self.horizontalLayout_9)

        self.label_user_registers_top_space = QLabel(self.tab_6)
        self.label_user_registers_top_space.setObjectName(u"label_user_registers_top_space")
        self.label_user_registers_top_space.setMinimumSize(QSize(0, 30))

        self.verticalLayout_4.addWidget(self.label_user_registers_top_space)

        self.label_user_login_title_10 = QLabel(self.tab_6)
        self.label_user_login_title_10.setObjectName(u"label_user_login_title_10")
        self.label_user_login_title_10.setFont(font)
        self.label_user_login_title_10.setStyleSheet(u"border: 0px solid #FF8D16;\n"
"border-radius: 0px;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.label_user_login_title_10.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_4.addWidget(self.label_user_login_title_10)

        self.line_edit_user_register_nickname = QLineEdit(self.tab_6)
        self.line_edit_user_register_nickname.setObjectName(u"line_edit_user_register_nickname")
        self.line_edit_user_register_nickname.setMinimumSize(QSize(0, 25))
        self.line_edit_user_register_nickname.setFont(font4)
        self.line_edit_user_register_nickname.setStyleSheet(u"")
        self.line_edit_user_register_nickname.setMaxLength(20)

        self.verticalLayout_4.addWidget(self.line_edit_user_register_nickname)

        self.label_user_register_nickname_prompt = QLabel(self.tab_6)
        self.label_user_register_nickname_prompt.setObjectName(u"label_user_register_nickname_prompt")
        self.label_user_register_nickname_prompt.setMinimumSize(QSize(0, 15))
        self.label_user_register_nickname_prompt.setMaximumSize(QSize(16777215, 15))
        self.label_user_register_nickname_prompt.setFont(font2)
        self.label_user_register_nickname_prompt.setStyleSheet(u"border: none; background-color: transparent;")

        self.verticalLayout_4.addWidget(self.label_user_register_nickname_prompt)

        self.label_user_login_title_7 = QLabel(self.tab_6)
        self.label_user_login_title_7.setObjectName(u"label_user_login_title_7")
        self.label_user_login_title_7.setFont(font)
        self.label_user_login_title_7.setStyleSheet(u"border: 0px solid #FF8D16;\n"
"border-radius: 0px;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.label_user_login_title_7.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_4.addWidget(self.label_user_login_title_7)

        self.line_edit_user_register_username = QLineEdit(self.tab_6)
        self.line_edit_user_register_username.setObjectName(u"line_edit_user_register_username")
        self.line_edit_user_register_username.setMinimumSize(QSize(0, 25))
        self.line_edit_user_register_username.setFont(font4)
        self.line_edit_user_register_username.setStyleSheet(u"")
        self.line_edit_user_register_username.setMaxLength(20)

        self.verticalLayout_4.addWidget(self.line_edit_user_register_username)

        self.label_user_register_username_prompt = QLabel(self.tab_6)
        self.label_user_register_username_prompt.setObjectName(u"label_user_register_username_prompt")
        self.label_user_register_username_prompt.setMinimumSize(QSize(0, 15))
        self.label_user_register_username_prompt.setMaximumSize(QSize(16777215, 15))
        self.label_user_register_username_prompt.setFont(font2)
        self.label_user_register_username_prompt.setStyleSheet(u"border: none; background-color: transparent;")

        self.verticalLayout_4.addWidget(self.label_user_register_username_prompt)

        self.label_user_login_title_11 = QLabel(self.tab_6)
        self.label_user_login_title_11.setObjectName(u"label_user_login_title_11")
        self.label_user_login_title_11.setFont(font)
        self.label_user_login_title_11.setStyleSheet(u"border: 0px solid #FF8D16;\n"
"border-radius: 0px;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.label_user_login_title_11.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_4.addWidget(self.label_user_login_title_11)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.line_edit_register_validator_code = QLineEdit(self.tab_6)
        self.line_edit_register_validator_code.setObjectName(u"line_edit_register_validator_code")
        self.line_edit_register_validator_code.setMinimumSize(QSize(0, 25))
        self.line_edit_register_validator_code.setFont(font4)
        self.line_edit_register_validator_code.setStyleSheet(u"")
        self.line_edit_register_validator_code.setMaxLength(6)

        self.horizontalLayout_2.addWidget(self.line_edit_register_validator_code)

        self.push_button_register_validator_code = QPushButton(self.tab_6)
        self.push_button_register_validator_code.setObjectName(u"push_button_register_validator_code")
        self.push_button_register_validator_code.setMinimumSize(QSize(100, 25))

        self.horizontalLayout_2.addWidget(self.push_button_register_validator_code)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.label_register_validator_code_prompt = QLabel(self.tab_6)
        self.label_register_validator_code_prompt.setObjectName(u"label_register_validator_code_prompt")
        self.label_register_validator_code_prompt.setMinimumSize(QSize(0, 15))
        self.label_register_validator_code_prompt.setMaximumSize(QSize(16777215, 15))
        self.label_register_validator_code_prompt.setFont(font2)
        self.label_register_validator_code_prompt.setStyleSheet(u"border: none; background-color: transparent;")

        self.verticalLayout_4.addWidget(self.label_register_validator_code_prompt)

        self.label_user_login_title_8 = QLabel(self.tab_6)
        self.label_user_login_title_8.setObjectName(u"label_user_login_title_8")
        self.label_user_login_title_8.setFont(font)
        self.label_user_login_title_8.setStyleSheet(u"border: 0px solid #FF8D16;\n"
"border-radius: 0px;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.label_user_login_title_8.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_4.addWidget(self.label_user_login_title_8)

        self.line_edit_user_register_password_widget = QWidget(self.tab_6)
        self.line_edit_user_register_password_widget.setObjectName(u"line_edit_user_register_password_widget")
        self.gridLayout_2 = QGridLayout(self.line_edit_user_register_password_widget)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.line_edit_user_register_password = QLineEdit(self.line_edit_user_register_password_widget)
        self.line_edit_user_register_password.setObjectName(u"line_edit_user_register_password")
        self.line_edit_user_register_password.setMinimumSize(QSize(0, 25))
        self.line_edit_user_register_password.setFont(font4)
        self.line_edit_user_register_password.setStyleSheet(u"")
        self.line_edit_user_register_password.setMaxLength(20)
        self.line_edit_user_register_password.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_3.addWidget(self.line_edit_user_register_password)

        self.push_button_user_register_password_view_control = QPushButton(self.line_edit_user_register_password_widget)
        self.push_button_user_register_password_view_control.setObjectName(u"push_button_user_register_password_view_control")
        self.push_button_user_register_password_view_control.setMinimumSize(QSize(25, 25))

        self.horizontalLayout_3.addWidget(self.push_button_user_register_password_view_control)


        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)


        self.verticalLayout_4.addWidget(self.line_edit_user_register_password_widget)

        self.label_user_register_password_prompt = QLabel(self.tab_6)
        self.label_user_register_password_prompt.setObjectName(u"label_user_register_password_prompt")
        self.label_user_register_password_prompt.setMinimumSize(QSize(0, 15))
        self.label_user_register_password_prompt.setMaximumSize(QSize(16777215, 15))
        self.label_user_register_password_prompt.setFont(font2)
        self.label_user_register_password_prompt.setStyleSheet(u"border: none; background-color: transparent;")

        self.verticalLayout_4.addWidget(self.label_user_register_password_prompt)

        self.label_user_login_title_9 = QLabel(self.tab_6)
        self.label_user_login_title_9.setObjectName(u"label_user_login_title_9")
        self.label_user_login_title_9.setFont(font)
        self.label_user_login_title_9.setStyleSheet(u"border: 0px solid #FF8D16;\n"
"border-radius: 0px;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.label_user_login_title_9.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_4.addWidget(self.label_user_login_title_9)

        self.line_edit_user_register_password_check_widget = QWidget(self.tab_6)
        self.line_edit_user_register_password_check_widget.setObjectName(u"line_edit_user_register_password_check_widget")
        self.gridLayout_3 = QGridLayout(self.line_edit_user_register_password_check_widget)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.line_edit_user_register_password_check = QLineEdit(self.line_edit_user_register_password_check_widget)
        self.line_edit_user_register_password_check.setObjectName(u"line_edit_user_register_password_check")
        self.line_edit_user_register_password_check.setMinimumSize(QSize(0, 25))
        self.line_edit_user_register_password_check.setFont(font4)
        self.line_edit_user_register_password_check.setStyleSheet(u"")
        self.line_edit_user_register_password_check.setMaxLength(20)
        self.line_edit_user_register_password_check.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_10.addWidget(self.line_edit_user_register_password_check)

        self.push_button_user_register_password_check_view_control = QPushButton(self.line_edit_user_register_password_check_widget)
        self.push_button_user_register_password_check_view_control.setObjectName(u"push_button_user_register_password_check_view_control")
        self.push_button_user_register_password_check_view_control.setMinimumSize(QSize(25, 25))

        self.horizontalLayout_10.addWidget(self.push_button_user_register_password_check_view_control)


        self.gridLayout_3.addLayout(self.horizontalLayout_10, 0, 0, 1, 1)


        self.verticalLayout_4.addWidget(self.line_edit_user_register_password_check_widget)

        self.label_user_register_password_check_prompt = QLabel(self.tab_6)
        self.label_user_register_password_check_prompt.setObjectName(u"label_user_register_password_check_prompt")
        self.label_user_register_password_check_prompt.setMinimumSize(QSize(0, 15))
        self.label_user_register_password_check_prompt.setMaximumSize(QSize(16777215, 15))
        self.label_user_register_password_check_prompt.setFont(font2)
        self.label_user_register_password_check_prompt.setStyleSheet(u"border: none; background-color: transparent;")

        self.verticalLayout_4.addWidget(self.label_user_register_password_check_prompt)

        self.label_user_login_title_12 = QLabel(self.tab_6)
        self.label_user_login_title_12.setObjectName(u"label_user_login_title_12")
        self.label_user_login_title_12.setFont(font)
        self.label_user_login_title_12.setStyleSheet(u"border: 0px solid #FF8D16;\n"
"border-radius: 0px;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.label_user_login_title_12.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_4.addWidget(self.label_user_login_title_12)

        self.line_edit_user_register_invite_code = QLineEdit(self.tab_6)
        self.line_edit_user_register_invite_code.setObjectName(u"line_edit_user_register_invite_code")
        self.line_edit_user_register_invite_code.setMinimumSize(QSize(0, 25))
        self.line_edit_user_register_invite_code.setFont(font4)
        self.line_edit_user_register_invite_code.setStyleSheet(u"")
        self.line_edit_user_register_invite_code.setMaxLength(20)

        self.verticalLayout_4.addWidget(self.line_edit_user_register_invite_code)

        self.label_user_register_invite_code_prompt = QLabel(self.tab_6)
        self.label_user_register_invite_code_prompt.setObjectName(u"label_user_register_invite_code_prompt")
        self.label_user_register_invite_code_prompt.setMinimumSize(QSize(0, 15))
        self.label_user_register_invite_code_prompt.setMaximumSize(QSize(16777215, 15))
        self.label_user_register_invite_code_prompt.setFont(font2)
        self.label_user_register_invite_code_prompt.setStyleSheet(u"border: none; background-color: transparent;")

        self.verticalLayout_4.addWidget(self.label_user_register_invite_code_prompt)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.check_box_user_area_agree_protocol = QCheckBox(self.tab_6)
        self.check_box_user_area_agree_protocol.setObjectName(u"check_box_user_area_agree_protocol")

        self.horizontalLayout_4.addWidget(self.check_box_user_area_agree_protocol)

        self.label_2 = QLabel(self.tab_6)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 0))
        font5 = QFont()
        font5.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font5.setBold(True)
        self.label_2.setFont(font5)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_2)

        self.push_button_user_register_privacy_agreement = QPushButton(self.tab_6)
        self.push_button_user_register_privacy_agreement.setObjectName(u"push_button_user_register_privacy_agreement")
        self.push_button_user_register_privacy_agreement.setStyleSheet(u"border: none; background-color: transparent;color: rgb(20, 161, 248);")

        self.horizontalLayout_4.addWidget(self.push_button_user_register_privacy_agreement)

        self.label_7 = QLabel(self.tab_6)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font5)
        self.label_7.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_7)

        self.push_button_user_register_service_agreement = QPushButton(self.tab_6)
        self.push_button_user_register_service_agreement.setObjectName(u"push_button_user_register_service_agreement")
        self.push_button_user_register_service_agreement.setStyleSheet(u"border: none; background-color: transparent;color: rgb(20, 161, 248);")

        self.horizontalLayout_4.addWidget(self.push_button_user_register_service_agreement)

        self.label_10 = QLabel(self.tab_6)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font5)
        self.label_10.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_10)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.label_user_registers_bottom_space = QLabel(self.tab_6)
        self.label_user_registers_bottom_space.setObjectName(u"label_user_registers_bottom_space")
        self.label_user_registers_bottom_space.setMinimumSize(QSize(0, 30))

        self.verticalLayout_4.addWidget(self.label_user_registers_bottom_space)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_10)

        self.push_button_user_register = QPushButton(self.tab_6)
        self.push_button_user_register.setObjectName(u"push_button_user_register")
        self.push_button_user_register.setMinimumSize(QSize(120, 40))
        self.push_button_user_register.setFont(font4)
        self.push_button_user_register.setStyleSheet(u"")

        self.horizontalLayout_7.addWidget(self.push_button_user_register)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_9)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_9)


        self.gridLayout_7.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        self.tab_widget_login.addTab(self.tab_6, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_4 = QGridLayout(self.tab)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalLayout_17 = QVBoxLayout()
        self.verticalLayout_17.setSpacing(4)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(20, -1, 20, -1)
        self.verticalSpacer_15 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_17.addItem(self.verticalSpacer_15)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_22)

        self.label_user_forget_logo = QLabel(self.tab)
        self.label_user_forget_logo.setObjectName(u"label_user_forget_logo")
        self.label_user_forget_logo.setMinimumSize(QSize(46, 46))
        self.label_user_forget_logo.setMaximumSize(QSize(46, 46))
        self.label_user_forget_logo.setScaledContents(True)

        self.horizontalLayout_23.addWidget(self.label_user_forget_logo)

        self.horizontalSpacer_23 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_23)


        self.verticalLayout_17.addLayout(self.horizontalLayout_23)

        self.label_user_registers_top_space_2 = QLabel(self.tab)
        self.label_user_registers_top_space_2.setObjectName(u"label_user_registers_top_space_2")
        self.label_user_registers_top_space_2.setMinimumSize(QSize(0, 30))

        self.verticalLayout_17.addWidget(self.label_user_registers_top_space_2)

        self.label_user_login_title_13 = QLabel(self.tab)
        self.label_user_login_title_13.setObjectName(u"label_user_login_title_13")
        self.label_user_login_title_13.setFont(font)
        self.label_user_login_title_13.setStyleSheet(u"border: 0px solid #FF8D16;\n"
"border-radius: 0px;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.label_user_login_title_13.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_17.addWidget(self.label_user_login_title_13)

        self.line_edit_user_forget_username = QLineEdit(self.tab)
        self.line_edit_user_forget_username.setObjectName(u"line_edit_user_forget_username")
        self.line_edit_user_forget_username.setMinimumSize(QSize(0, 25))
        self.line_edit_user_forget_username.setFont(font4)
        self.line_edit_user_forget_username.setStyleSheet(u"")
        self.line_edit_user_forget_username.setMaxLength(20)

        self.verticalLayout_17.addWidget(self.line_edit_user_forget_username)

        self.label_user_forget_username_prompt = QLabel(self.tab)
        self.label_user_forget_username_prompt.setObjectName(u"label_user_forget_username_prompt")
        self.label_user_forget_username_prompt.setMinimumSize(QSize(0, 15))
        self.label_user_forget_username_prompt.setMaximumSize(QSize(16777215, 15))
        self.label_user_forget_username_prompt.setFont(font2)
        self.label_user_forget_username_prompt.setStyleSheet(u"border: none; background-color: transparent;")

        self.verticalLayout_17.addWidget(self.label_user_forget_username_prompt)

        self.label_user_login_title_15 = QLabel(self.tab)
        self.label_user_login_title_15.setObjectName(u"label_user_login_title_15")
        self.label_user_login_title_15.setFont(font)
        self.label_user_login_title_15.setStyleSheet(u"border: 0px solid #FF8D16;\n"
"border-radius: 0px;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.label_user_login_title_15.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_17.addWidget(self.label_user_login_title_15)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.line_edit_forget_validator_code = QLineEdit(self.tab)
        self.line_edit_forget_validator_code.setObjectName(u"line_edit_forget_validator_code")
        self.line_edit_forget_validator_code.setMinimumSize(QSize(0, 25))
        self.line_edit_forget_validator_code.setFont(font4)
        self.line_edit_forget_validator_code.setStyleSheet(u"")
        self.line_edit_forget_validator_code.setMaxLength(6)

        self.horizontalLayout_24.addWidget(self.line_edit_forget_validator_code)

        self.push_button_forget_validator_code = QPushButton(self.tab)
        self.push_button_forget_validator_code.setObjectName(u"push_button_forget_validator_code")
        self.push_button_forget_validator_code.setMinimumSize(QSize(100, 25))

        self.horizontalLayout_24.addWidget(self.push_button_forget_validator_code)


        self.verticalLayout_17.addLayout(self.horizontalLayout_24)

        self.label_forget_validator_code_prompt = QLabel(self.tab)
        self.label_forget_validator_code_prompt.setObjectName(u"label_forget_validator_code_prompt")
        self.label_forget_validator_code_prompt.setMinimumSize(QSize(0, 15))
        self.label_forget_validator_code_prompt.setMaximumSize(QSize(16777215, 15))
        self.label_forget_validator_code_prompt.setFont(font2)
        self.label_forget_validator_code_prompt.setStyleSheet(u"border: none; background-color: transparent;")

        self.verticalLayout_17.addWidget(self.label_forget_validator_code_prompt)

        self.label_user_login_title_16 = QLabel(self.tab)
        self.label_user_login_title_16.setObjectName(u"label_user_login_title_16")
        self.label_user_login_title_16.setFont(font)
        self.label_user_login_title_16.setStyleSheet(u"border: 0px solid #FF8D16;\n"
"border-radius: 0px;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.label_user_login_title_16.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_17.addWidget(self.label_user_login_title_16)

        self.line_edit_user_forget_password_widget = QWidget(self.tab)
        self.line_edit_user_forget_password_widget.setObjectName(u"line_edit_user_forget_password_widget")
        self.gridLayout_5 = QGridLayout(self.line_edit_user_forget_password_widget)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.line_edit_user_forget_password = QLineEdit(self.line_edit_user_forget_password_widget)
        self.line_edit_user_forget_password.setObjectName(u"line_edit_user_forget_password")
        self.line_edit_user_forget_password.setMinimumSize(QSize(0, 25))
        self.line_edit_user_forget_password.setFont(font4)
        self.line_edit_user_forget_password.setStyleSheet(u"")
        self.line_edit_user_forget_password.setMaxLength(20)
        self.line_edit_user_forget_password.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_11.addWidget(self.line_edit_user_forget_password)

        self.push_button_user_forget_password_view_control = QPushButton(self.line_edit_user_forget_password_widget)
        self.push_button_user_forget_password_view_control.setObjectName(u"push_button_user_forget_password_view_control")
        self.push_button_user_forget_password_view_control.setMinimumSize(QSize(25, 25))

        self.horizontalLayout_11.addWidget(self.push_button_user_forget_password_view_control)


        self.gridLayout_5.addLayout(self.horizontalLayout_11, 0, 0, 1, 1)


        self.verticalLayout_17.addWidget(self.line_edit_user_forget_password_widget)

        self.label_user_forget_password_prompt = QLabel(self.tab)
        self.label_user_forget_password_prompt.setObjectName(u"label_user_forget_password_prompt")
        self.label_user_forget_password_prompt.setMinimumSize(QSize(0, 15))
        self.label_user_forget_password_prompt.setMaximumSize(QSize(16777215, 15))
        self.label_user_forget_password_prompt.setFont(font2)
        self.label_user_forget_password_prompt.setStyleSheet(u"border: none; background-color: transparent;")

        self.verticalLayout_17.addWidget(self.label_user_forget_password_prompt)

        self.label_user_login_title_17 = QLabel(self.tab)
        self.label_user_login_title_17.setObjectName(u"label_user_login_title_17")
        self.label_user_login_title_17.setFont(font)
        self.label_user_login_title_17.setStyleSheet(u"border: 0px solid #FF8D16;\n"
"border-radius: 0px;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.label_user_login_title_17.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_17.addWidget(self.label_user_login_title_17)

        self.line_edit_user_forget_password_check_widget = QWidget(self.tab)
        self.line_edit_user_forget_password_check_widget.setObjectName(u"line_edit_user_forget_password_check_widget")
        self.gridLayout_6 = QGridLayout(self.line_edit_user_forget_password_check_widget)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.line_edit_user_forget_password_check = QLineEdit(self.line_edit_user_forget_password_check_widget)
        self.line_edit_user_forget_password_check.setObjectName(u"line_edit_user_forget_password_check")
        self.line_edit_user_forget_password_check.setMinimumSize(QSize(0, 25))
        self.line_edit_user_forget_password_check.setFont(font4)
        self.line_edit_user_forget_password_check.setStyleSheet(u"")
        self.line_edit_user_forget_password_check.setMaxLength(20)
        self.line_edit_user_forget_password_check.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_12.addWidget(self.line_edit_user_forget_password_check)

        self.push_button_user_forget_password_check_view_control = QPushButton(self.line_edit_user_forget_password_check_widget)
        self.push_button_user_forget_password_check_view_control.setObjectName(u"push_button_user_forget_password_check_view_control")
        self.push_button_user_forget_password_check_view_control.setMinimumSize(QSize(25, 25))

        self.horizontalLayout_12.addWidget(self.push_button_user_forget_password_check_view_control)


        self.gridLayout_6.addLayout(self.horizontalLayout_12, 0, 0, 1, 1)


        self.verticalLayout_17.addWidget(self.line_edit_user_forget_password_check_widget)

        self.label_user_forget_password_check_prompt = QLabel(self.tab)
        self.label_user_forget_password_check_prompt.setObjectName(u"label_user_forget_password_check_prompt")
        self.label_user_forget_password_check_prompt.setMinimumSize(QSize(0, 15))
        self.label_user_forget_password_check_prompt.setMaximumSize(QSize(16777215, 15))
        self.label_user_forget_password_check_prompt.setFont(font2)
        self.label_user_forget_password_check_prompt.setStyleSheet(u"border: none; background-color: transparent;")

        self.verticalLayout_17.addWidget(self.label_user_forget_password_check_prompt)

        self.label_user_registers_bottom_space_2 = QLabel(self.tab)
        self.label_user_registers_bottom_space_2.setObjectName(u"label_user_registers_bottom_space_2")
        self.label_user_registers_bottom_space_2.setMinimumSize(QSize(0, 30))

        self.verticalLayout_17.addWidget(self.label_user_registers_bottom_space_2)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalSpacer_24 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_24)

        self.push_button_user_forget = QPushButton(self.tab)
        self.push_button_user_forget.setObjectName(u"push_button_user_forget")
        self.push_button_user_forget.setMinimumSize(QSize(120, 40))
        self.push_button_user_forget.setFont(font4)
        self.push_button_user_forget.setStyleSheet(u"")

        self.horizontalLayout_25.addWidget(self.push_button_user_forget)

        self.horizontalSpacer_25 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_25)


        self.verticalLayout_17.addLayout(self.horizontalLayout_25)

        self.verticalSpacer_16 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_17.addItem(self.verticalSpacer_16)


        self.gridLayout_4.addLayout(self.verticalLayout_17, 0, 0, 1, 1)

        self.tab_widget_login.addTab(self.tab, "")

        self.verticalLayout.addWidget(self.tab_widget_login)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_3)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 0))
        self.label_3.setFont(font5)
        self.label_3.setStyleSheet(u"border: none; background-color: transparent;")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_13.addWidget(self.label_3)

        self.push_button_update_soft = QPushButton(Form)
        self.push_button_update_soft.setObjectName(u"push_button_update_soft")
        self.push_button_update_soft.setStyleSheet(u"border: none; background-color: transparent;color: rgb(20, 161, 248);")

        self.horizontalLayout_13.addWidget(self.push_button_update_soft)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_13)


        self.gridLayout_8.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(Form)

        self.tab_widget_login.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_user_login_logo.setText("")
        self.label_user_login_top_space.setText("")
        self.label_user_login_title_2.setText(QCoreApplication.translate("Form", u"\u624b\u673a\u53f7\uff1a", None))
        self.label_user_login_username_prompt.setText("")
        self.label_user_login_title_3.setText(QCoreApplication.translate("Form", u"\u5bc6\u7801\uff1a", None))
        self.push_button_user_login_password_view_control.setText("")
        self.label_user_login_password_prompt.setText("")
        self.push_button_user_login_forget_password.setText(QCoreApplication.translate("Form", u"\u5fd8\u8bb0\u5bc6\u7801\uff1f", None))
        self.label_user_login_bottom_space.setText("")
        self.push_button_user_login.setText(QCoreApplication.translate("Form", u"\u767b\u5f55", None))
        self.tab_widget_login.setTabText(self.tab_widget_login.indexOf(self.tab_12), QCoreApplication.translate("Form", u"\u767b\u5f55", None))
        self.label_user_register_logo.setText("")
        self.label_user_registers_top_space.setText("")
        self.label_user_login_title_10.setText(QCoreApplication.translate("Form", u"*\u6635\u79f0\uff1a", None))
        self.label_user_register_nickname_prompt.setText("")
        self.label_user_login_title_7.setText(QCoreApplication.translate("Form", u"*\u624b\u673a\u53f7\uff1a", None))
        self.label_user_register_username_prompt.setText("")
        self.label_user_login_title_11.setText(QCoreApplication.translate("Form", u"*\u9a8c\u8bc1\u7801\uff1a", None))
        self.push_button_register_validator_code.setText(QCoreApplication.translate("Form", u"\u53d1\u9001\u9a8c\u8bc1\u7801", None))
        self.label_register_validator_code_prompt.setText("")
        self.label_user_login_title_8.setText(QCoreApplication.translate("Form", u"*\u5bc6\u7801(10-20\u4f4d\u5b57\u7b26,\u5305\u542b\u5b57\u6bcd\u548c\u6570\u5b57)\uff1a", None))
        self.push_button_user_register_password_view_control.setText("")
        self.label_user_register_password_prompt.setText("")
        self.label_user_login_title_9.setText(QCoreApplication.translate("Form", u"*\u786e\u8ba4\u5bc6\u7801\uff1a", None))
        self.push_button_user_register_password_check_view_control.setText("")
        self.label_user_register_password_check_prompt.setText("")
        self.label_user_login_title_12.setText(QCoreApplication.translate("Form", u"\u9080\u8bf7\u7801(\u586b\u5199\u9080\u8bf7\u7801\u53cc\u65b9\u5747\u53ef\u83b7\u5f97\u4e03\u5929\u5468\u5361\u54e6~)\uff1a", None))
        self.label_user_register_invite_code_prompt.setText("")
        self.check_box_user_area_agree_protocol.setText("")
        self.label_2.setText(QCoreApplication.translate("Form", u"\u6211\u5df2\u9605\u8bfb\u5e76\u63a5\u53d7", None))
        self.push_button_user_register_privacy_agreement.setText(QCoreApplication.translate("Form", u"\u300a\u9690\u79c1\u653f\u7b56\u300b", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"&", None))
        self.push_button_user_register_service_agreement.setText(QCoreApplication.translate("Form", u"\u300a\u7528\u6237\u534f\u8bae\u300b", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"\u3002", None))
        self.label_user_registers_bottom_space.setText("")
        self.push_button_user_register.setText(QCoreApplication.translate("Form", u"\u6ce8\u518c", None))
        self.tab_widget_login.setTabText(self.tab_widget_login.indexOf(self.tab_6), QCoreApplication.translate("Form", u"\u6ce8\u518c", None))
        self.label_user_forget_logo.setText("")
        self.label_user_registers_top_space_2.setText("")
        self.label_user_login_title_13.setText(QCoreApplication.translate("Form", u"*\u624b\u673a\u53f7\uff1a", None))
        self.label_user_forget_username_prompt.setText("")
        self.label_user_login_title_15.setText(QCoreApplication.translate("Form", u"*\u9a8c\u8bc1\u7801\uff1a", None))
        self.push_button_forget_validator_code.setText(QCoreApplication.translate("Form", u"\u53d1\u9001\u9a8c\u8bc1\u7801", None))
        self.label_forget_validator_code_prompt.setText("")
        self.label_user_login_title_16.setText(QCoreApplication.translate("Form", u"*\u5bc6\u7801(10-20\u4f4d\u5b57\u7b26,\u5305\u542b\u5b57\u6bcd\u548c\u6570\u5b57)\uff1a", None))
        self.push_button_user_forget_password_view_control.setText("")
        self.label_user_forget_password_prompt.setText("")
        self.label_user_login_title_17.setText(QCoreApplication.translate("Form", u"*\u786e\u8ba4\u5bc6\u7801\uff1a", None))
        self.push_button_user_forget_password_check_view_control.setText("")
        self.label_user_forget_password_check_prompt.setText("")
        self.label_user_registers_bottom_space_2.setText("")
        self.push_button_user_forget.setText(QCoreApplication.translate("Form", u"\u786e\u8ba4\u4fee\u6539\u5bc6\u7801", None))
        self.tab_widget_login.setTabText(self.tab_widget_login.indexOf(self.tab), QCoreApplication.translate("Form", u"\u5fd8\u8bb0\u5bc6\u7801", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u9047\u5230\u95ee\u9898\uff1f\u60a8\u53ef\u4ee5\u5c1d\u8bd5", None))
        self.push_button_update_soft.setText(QCoreApplication.translate("Form", u"\u66f4\u65b0\u8f6f\u4ef6", None))
    # retranslateUi

