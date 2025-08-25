# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setting_system_form.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(338, 464)
        self.gridLayout_5 = QGridLayout(Form)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.check_box_self_starting = QCheckBox(Form)
        self.check_box_self_starting.setObjectName(u"check_box_self_starting")
        self.check_box_self_starting.setMinimumSize(QSize(0, 20))
        font = QFont()
        font.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font.setPointSize(10)
        self.check_box_self_starting.setFont(font)
        self.check_box_self_starting.setChecked(True)

        self.gridLayout_2.addWidget(self.check_box_self_starting, 0, 1, 1, 1)

        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setStyleSheet(u"background: transparent;")
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 20))
        self.label.setFont(font)
        self.label.setStyleSheet(u"background: transparent;")
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.check_box_wake_up_keyboard = QCheckBox(Form)
        self.check_box_wake_up_keyboard.setObjectName(u"check_box_wake_up_keyboard")
        self.check_box_wake_up_keyboard.setMinimumSize(QSize(0, 20))
        self.check_box_wake_up_keyboard.setFont(font)
        self.check_box_wake_up_keyboard.setChecked(True)

        self.gridLayout.addWidget(self.check_box_wake_up_keyboard, 0, 1, 1, 1)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"background: transparent;")
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)

        self.combo_box_wake_up_main_keyboard = QComboBox(Form)
        self.combo_box_wake_up_main_keyboard.setObjectName(u"combo_box_wake_up_main_keyboard")
        self.combo_box_wake_up_main_keyboard.setMinimumSize(QSize(0, 20))
        self.combo_box_wake_up_main_keyboard.setFont(font)
        self.combo_box_wake_up_main_keyboard.setStyleSheet(u"")
        self.combo_box_wake_up_main_keyboard.setEditable(False)
        self.combo_box_wake_up_main_keyboard.setDuplicatesEnabled(False)

        self.gridLayout.addWidget(self.combo_box_wake_up_main_keyboard, 1, 1, 1, 1)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 20))
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"background: transparent;")
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.combo_box_wake_up_vice_keyboard = QComboBox(Form)
        self.combo_box_wake_up_vice_keyboard.setObjectName(u"combo_box_wake_up_vice_keyboard")
        self.combo_box_wake_up_vice_keyboard.setMinimumSize(QSize(0, 20))
        self.combo_box_wake_up_vice_keyboard.setFont(font)
        self.combo_box_wake_up_vice_keyboard.setStyleSheet(u"")
        self.combo_box_wake_up_vice_keyboard.setEditable(False)
        self.combo_box_wake_up_vice_keyboard.setDuplicatesEnabled(False)

        self.gridLayout.addWidget(self.combo_box_wake_up_vice_keyboard, 2, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.line_2 = QFrame(Form)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 20))
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(u"background: transparent;")
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_3, 1, 0, 1, 1)

        self.check_box_screenshot_keyboard = QCheckBox(Form)
        self.check_box_screenshot_keyboard.setObjectName(u"check_box_screenshot_keyboard")
        self.check_box_screenshot_keyboard.setMinimumSize(QSize(0, 20))
        self.check_box_screenshot_keyboard.setFont(font)
        self.check_box_screenshot_keyboard.setChecked(True)

        self.gridLayout_3.addWidget(self.check_box_screenshot_keyboard, 0, 1, 1, 1)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 20))
        self.label_4.setFont(font)
        self.label_4.setStyleSheet(u"background: transparent;")
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_4, 2, 0, 1, 1)

        self.combo_box_screenshot_vice_keyboard = QComboBox(Form)
        self.combo_box_screenshot_vice_keyboard.setObjectName(u"combo_box_screenshot_vice_keyboard")
        self.combo_box_screenshot_vice_keyboard.setMinimumSize(QSize(0, 20))
        self.combo_box_screenshot_vice_keyboard.setFont(font)
        self.combo_box_screenshot_vice_keyboard.setStyleSheet(u"")
        self.combo_box_screenshot_vice_keyboard.setEditable(False)
        self.combo_box_screenshot_vice_keyboard.setDuplicatesEnabled(False)

        self.gridLayout_3.addWidget(self.combo_box_screenshot_vice_keyboard, 2, 1, 1, 1)

        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setStyleSheet(u"background: transparent;")
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)

        self.combo_box_screenshot_main_keyboard = QComboBox(Form)
        self.combo_box_screenshot_main_keyboard.setObjectName(u"combo_box_screenshot_main_keyboard")
        self.combo_box_screenshot_main_keyboard.setMinimumSize(QSize(0, 20))
        self.combo_box_screenshot_main_keyboard.setFont(font)
        self.combo_box_screenshot_main_keyboard.setStyleSheet(u"")
        self.combo_box_screenshot_main_keyboard.setEditable(False)
        self.combo_box_screenshot_main_keyboard.setDuplicatesEnabled(False)

        self.gridLayout_3.addWidget(self.combo_box_screenshot_main_keyboard, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_3)

        self.line_3 = QFrame(Form)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_8 = QLabel(Form)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(0, 20))
        self.label_8.setFont(font)
        self.label_8.setStyleSheet(u"background: transparent;")
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_8, 1, 0, 1, 1)

        self.check_box_search_keyboard = QCheckBox(Form)
        self.check_box_search_keyboard.setObjectName(u"check_box_search_keyboard")
        self.check_box_search_keyboard.setMinimumSize(QSize(0, 20))
        self.check_box_search_keyboard.setFont(font)
        self.check_box_search_keyboard.setChecked(True)

        self.gridLayout_4.addWidget(self.check_box_search_keyboard, 0, 1, 1, 1)

        self.label_9 = QLabel(Form)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(0, 20))
        self.label_9.setFont(font)
        self.label_9.setStyleSheet(u"background: transparent;")
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_9, 2, 0, 1, 1)

        self.combo_box_search_vice_keyboard = QComboBox(Form)
        self.combo_box_search_vice_keyboard.setObjectName(u"combo_box_search_vice_keyboard")
        self.combo_box_search_vice_keyboard.setMinimumSize(QSize(0, 20))
        self.combo_box_search_vice_keyboard.setFont(font)
        self.combo_box_search_vice_keyboard.setStyleSheet(u"")
        self.combo_box_search_vice_keyboard.setEditable(False)
        self.combo_box_search_vice_keyboard.setDuplicatesEnabled(False)

        self.gridLayout_4.addWidget(self.combo_box_search_vice_keyboard, 2, 1, 1, 1)

        self.label_10 = QLabel(Form)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setStyleSheet(u"background: transparent;")
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_10, 0, 0, 1, 1)

        self.combo_box_search_main_keyboard = QComboBox(Form)
        self.combo_box_search_main_keyboard.setObjectName(u"combo_box_search_main_keyboard")
        self.combo_box_search_main_keyboard.setMinimumSize(QSize(0, 20))
        self.combo_box_search_main_keyboard.setFont(font)
        self.combo_box_search_main_keyboard.setStyleSheet(u"")
        self.combo_box_search_main_keyboard.setEditable(False)
        self.combo_box_search_main_keyboard.setDuplicatesEnabled(False)

        self.gridLayout_4.addWidget(self.combo_box_search_main_keyboard, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.push_button_ok = QPushButton(Form)
        self.push_button_ok.setObjectName(u"push_button_ok")
        self.push_button_ok.setMinimumSize(QSize(80, 30))
        self.push_button_ok.setMaximumSize(QSize(16777215, 30))
        self.push_button_ok.setFont(font)

        self.horizontalLayout.addWidget(self.push_button_ok)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout_5.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.check_box_self_starting.setText(QCoreApplication.translate("Form", u"\u542f\u7528", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u5f00\u673a\u81ea\u542f\u52a8\uff1a", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u4e3b\u8981\u7684\uff1a", None))
        self.check_box_wake_up_keyboard.setText(QCoreApplication.translate("Form", u"\u542f\u7528", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u754c\u9762\u5c55\u793a/\u9690\u85cf\u5feb\u6377\u952e\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u6b21\u8981\u7684\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u4e3b\u8981\u7684\uff1a", None))
        self.check_box_screenshot_keyboard.setText(QCoreApplication.translate("Form", u"\u542f\u7528", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u6b21\u8981\u7684\uff1a", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\u622a\u56fe\u5feb\u6377\u952e\uff1a", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u4e3b\u8981\u7684\uff1a", None))
        self.check_box_search_keyboard.setText(QCoreApplication.translate("Form", u"\u542f\u7528", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"\u6b21\u8981\u7684\uff1a", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"\u672c\u5730\u641c\u7d22\u5feb\u6377\u952e\uff1a", None))
        self.push_button_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
    # retranslateUi

