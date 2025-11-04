# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setting_menu_form.ui'
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
    QLabel, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(568, 522)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(12)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.left_layout = QVBoxLayout()
        self.left_layout.setObjectName(u"left_layout")
        self.title_left = QLabel(Form)
        self.title_left.setObjectName(u"title_left")

        self.left_layout.addWidget(self.title_left)


        self.horizontalLayout.addLayout(self.left_layout)

        self.button_layout = QVBoxLayout()
        self.button_layout.setObjectName(u"button_layout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.button_layout.addItem(self.verticalSpacer)

        self.add_btn = QPushButton(Form)
        self.add_btn.setObjectName(u"add_btn")

        self.button_layout.addWidget(self.add_btn)

        self.remove_btn = QPushButton(Form)
        self.remove_btn.setObjectName(u"remove_btn")

        self.button_layout.addWidget(self.remove_btn)

        self.up_btn = QPushButton(Form)
        self.up_btn.setObjectName(u"up_btn")

        self.button_layout.addWidget(self.up_btn)

        self.down_btn = QPushButton(Form)
        self.down_btn.setObjectName(u"down_btn")

        self.button_layout.addWidget(self.down_btn)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.button_layout.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addLayout(self.button_layout)

        self.right_layout = QVBoxLayout()
        self.right_layout.setObjectName(u"right_layout")
        self.title_right = QLabel(Form)
        self.title_right.setObjectName(u"title_right")

        self.right_layout.addWidget(self.title_right)


        self.horizontalLayout.addLayout(self.right_layout)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.label_9 = QLabel(Form)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(0, 20))
        font = QFont()
        font.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet(u"background: transparent;")

        self.horizontalLayout_2.addWidget(self.label_9)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.radio_button_menu_location_left = QRadioButton(Form)
        self.radio_button_menu_location_left.setObjectName(u"radio_button_menu_location_left")
        self.radio_button_menu_location_left.setMinimumSize(QSize(70, 20))
        self.radio_button_menu_location_left.setMaximumSize(QSize(70, 16777215))
        self.radio_button_menu_location_left.setSizeIncrement(QSize(0, 0))
        self.radio_button_menu_location_left.setFont(font)
        self.radio_button_menu_location_left.setStyleSheet(u"background: transparent;")
        self.radio_button_menu_location_left.setChecked(False)

        self.horizontalLayout_5.addWidget(self.radio_button_menu_location_left)

        self.radio_button_menu_location_right = QRadioButton(Form)
        self.radio_button_menu_location_right.setObjectName(u"radio_button_menu_location_right")
        self.radio_button_menu_location_right.setMinimumSize(QSize(0, 20))
        self.radio_button_menu_location_right.setFont(font)
        self.radio_button_menu_location_right.setStyleSheet(u"background: transparent;")
        self.radio_button_menu_location_right.setChecked(True)

        self.horizontalLayout_5.addWidget(self.radio_button_menu_location_right)


        self.horizontalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)

        self.label_10 = QLabel(Form)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(0, 20))
        self.label_10.setFont(font)
        self.label_10.setStyleSheet(u"background: transparent;")

        self.horizontalLayout_3.addWidget(self.label_10)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.check_box_side_popup = QCheckBox(Form)
        self.check_box_side_popup.setObjectName(u"check_box_side_popup")
        self.check_box_side_popup.setMinimumSize(QSize(0, 20))
        self.check_box_side_popup.setFont(font)
        self.check_box_side_popup.setStyleSheet(u"background: transparent;")
        self.check_box_side_popup.setChecked(True)

        self.horizontalLayout_7.addWidget(self.check_box_side_popup)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_7)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_7)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, 10, -1, -1)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.push_button_ok = QPushButton(Form)
        self.push_button_ok.setObjectName(u"push_button_ok")
        self.push_button_ok.setMinimumSize(QSize(80, 30))
        self.push_button_ok.setMaximumSize(QSize(16777215, 30))
        self.push_button_ok.setFont(font)

        self.horizontalLayout_6.addWidget(self.push_button_ok)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_5)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)


        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.title_left.setText(QCoreApplication.translate("Form", u"\u83dc\u5355\u5e93", None))
        self.add_btn.setText(QCoreApplication.translate("Form", u">", None))
        self.remove_btn.setText(QCoreApplication.translate("Form", u"<", None))
        self.up_btn.setText(QCoreApplication.translate("Form", u"\u4e0a\u79fb", None))
        self.down_btn.setText(QCoreApplication.translate("Form", u"\u4e0b\u79fb", None))
        self.title_right.setText(QCoreApplication.translate("Form", u"\u7528\u6237\u83dc\u5355 (\u53ef\u62d6\u62fd\u6392\u5e8f)", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"\u83dc\u5355\u680f\u4f4d\u7f6e\uff1a", None))
        self.radio_button_menu_location_left.setText(QCoreApplication.translate("Form", u"\u5de6\u4fa7", None))
        self.radio_button_menu_location_right.setText(QCoreApplication.translate("Form", u"\u53f3\u4fa7", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"\u81ea\u52a8\u5c55\u5f00\u6587\u5b57\uff1a", None))
        self.check_box_side_popup.setText(QCoreApplication.translate("Form", u"\u542f\u7528", None))
        self.push_button_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
    # retranslateUi

