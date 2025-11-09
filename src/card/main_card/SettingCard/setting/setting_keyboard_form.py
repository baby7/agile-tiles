# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setting_keyboard_form.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QGridLayout, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(479, 253)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.formLayout.setVerticalSpacing(15)
        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"background: transparent;")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_5)

        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setStyleSheet(u"background: transparent;")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_7)

        self.label_10 = QLabel(Form)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setStyleSheet(u"background: transparent;")
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_10)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.check_box_screenshot_keyboard = QCheckBox(Form)
        self.check_box_screenshot_keyboard.setObjectName(u"check_box_screenshot_keyboard")
        self.check_box_screenshot_keyboard.setMinimumSize(QSize(0, 20))
        font = QFont()
        font.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font.setPointSize(10)
        self.check_box_screenshot_keyboard.setFont(font)
        self.check_box_screenshot_keyboard.setChecked(True)

        self.horizontalLayout_3.addWidget(self.check_box_screenshot_keyboard)

        self.combo_box_screenshot_main_keyboard = QComboBox(Form)
        self.combo_box_screenshot_main_keyboard.setObjectName(u"combo_box_screenshot_main_keyboard")
        self.combo_box_screenshot_main_keyboard.setMinimumSize(QSize(0, 20))
        self.combo_box_screenshot_main_keyboard.setFont(font)
        self.combo_box_screenshot_main_keyboard.setStyleSheet(u"")
        self.combo_box_screenshot_main_keyboard.setEditable(False)
        self.combo_box_screenshot_main_keyboard.setDuplicatesEnabled(False)

        self.horizontalLayout_3.addWidget(self.combo_box_screenshot_main_keyboard)

        self.label_12 = QLabel(Form)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(0, 20))
        self.label_12.setMaximumSize(QSize(30, 16777215))
        self.label_12.setFont(font)
        self.label_12.setStyleSheet(u"background: transparent;")
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_12)

        self.combo_box_screenshot_vice_keyboard = QComboBox(Form)
        self.combo_box_screenshot_vice_keyboard.setObjectName(u"combo_box_screenshot_vice_keyboard")
        self.combo_box_screenshot_vice_keyboard.setMinimumSize(QSize(0, 20))
        self.combo_box_screenshot_vice_keyboard.setFont(font)
        self.combo_box_screenshot_vice_keyboard.setStyleSheet(u"")
        self.combo_box_screenshot_vice_keyboard.setEditable(False)
        self.combo_box_screenshot_vice_keyboard.setDuplicatesEnabled(False)

        self.horizontalLayout_3.addWidget(self.combo_box_screenshot_vice_keyboard)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.check_box_search_keyboard = QCheckBox(Form)
        self.check_box_search_keyboard.setObjectName(u"check_box_search_keyboard")
        self.check_box_search_keyboard.setMinimumSize(QSize(0, 20))
        self.check_box_search_keyboard.setFont(font)
        self.check_box_search_keyboard.setChecked(True)

        self.horizontalLayout_2.addWidget(self.check_box_search_keyboard)

        self.combo_box_search_main_keyboard = QComboBox(Form)
        self.combo_box_search_main_keyboard.setObjectName(u"combo_box_search_main_keyboard")
        self.combo_box_search_main_keyboard.setMinimumSize(QSize(0, 20))
        self.combo_box_search_main_keyboard.setFont(font)
        self.combo_box_search_main_keyboard.setStyleSheet(u"")
        self.combo_box_search_main_keyboard.setEditable(False)
        self.combo_box_search_main_keyboard.setDuplicatesEnabled(False)

        self.horizontalLayout_2.addWidget(self.combo_box_search_main_keyboard)

        self.label_11 = QLabel(Form)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(0, 20))
        self.label_11.setMaximumSize(QSize(30, 16777215))
        self.label_11.setFont(font)
        self.label_11.setStyleSheet(u"background: transparent;")
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_11)

        self.combo_box_search_vice_keyboard = QComboBox(Form)
        self.combo_box_search_vice_keyboard.setObjectName(u"combo_box_search_vice_keyboard")
        self.combo_box_search_vice_keyboard.setMinimumSize(QSize(0, 20))
        self.combo_box_search_vice_keyboard.setFont(font)
        self.combo_box_search_vice_keyboard.setStyleSheet(u"")
        self.combo_box_search_vice_keyboard.setEditable(False)
        self.combo_box_search_vice_keyboard.setDuplicatesEnabled(False)

        self.horizontalLayout_2.addWidget(self.combo_box_search_vice_keyboard)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.check_box_wake_up_keyboard = QCheckBox(Form)
        self.check_box_wake_up_keyboard.setObjectName(u"check_box_wake_up_keyboard")
        self.check_box_wake_up_keyboard.setMinimumSize(QSize(0, 20))
        self.check_box_wake_up_keyboard.setFont(font)
        self.check_box_wake_up_keyboard.setChecked(True)

        self.horizontalLayout_4.addWidget(self.check_box_wake_up_keyboard)

        self.combo_box_wake_up_main_keyboard = QComboBox(Form)
        self.combo_box_wake_up_main_keyboard.setObjectName(u"combo_box_wake_up_main_keyboard")
        self.combo_box_wake_up_main_keyboard.setMinimumSize(QSize(0, 20))
        self.combo_box_wake_up_main_keyboard.setFont(font)
        self.combo_box_wake_up_main_keyboard.setStyleSheet(u"")
        self.combo_box_wake_up_main_keyboard.setEditable(False)
        self.combo_box_wake_up_main_keyboard.setDuplicatesEnabled(False)

        self.horizontalLayout_4.addWidget(self.combo_box_wake_up_main_keyboard)

        self.label_13 = QLabel(Form)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(0, 20))
        self.label_13.setMaximumSize(QSize(30, 16777215))
        self.label_13.setFont(font)
        self.label_13.setStyleSheet(u"background: transparent;")
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_13)

        self.combo_box_wake_up_vice_keyboard = QComboBox(Form)
        self.combo_box_wake_up_vice_keyboard.setObjectName(u"combo_box_wake_up_vice_keyboard")
        self.combo_box_wake_up_vice_keyboard.setMinimumSize(QSize(0, 20))
        self.combo_box_wake_up_vice_keyboard.setFont(font)
        self.combo_box_wake_up_vice_keyboard.setStyleSheet(u"")
        self.combo_box_wake_up_vice_keyboard.setEditable(False)
        self.combo_box_wake_up_vice_keyboard.setDuplicatesEnabled(False)

        self.horizontalLayout_4.addWidget(self.combo_box_wake_up_vice_keyboard)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_4)


        self.verticalLayout.addLayout(self.formLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

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


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u754c\u9762\u5c55\u793a/\u9690\u85cf\u5feb\u6377\u952e\uff1a", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\u622a\u56fe\u5feb\u6377\u952e\uff1a", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"\u672c\u5730\u641c\u7d22\u5feb\u6377\u952e\uff1a", None))
        self.check_box_screenshot_keyboard.setText(QCoreApplication.translate("Form", u"\u542f\u7528", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"+", None))
        self.check_box_search_keyboard.setText(QCoreApplication.translate("Form", u"\u542f\u7528", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"+", None))
        self.check_box_wake_up_keyboard.setText(QCoreApplication.translate("Form", u"\u542f\u7528", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"+", None))
        self.push_button_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
    # retranslateUi

