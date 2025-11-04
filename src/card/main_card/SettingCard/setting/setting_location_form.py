# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setting_location_form.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(498, 363)
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.formLayout.setHorizontalSpacing(6)
        self.formLayout.setVerticalSpacing(20)
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"background: transparent;")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_4)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.screen_combo_box = QComboBox(Form)
        self.screen_combo_box.setObjectName(u"screen_combo_box")

        self.verticalLayout_2.addWidget(self.screen_combo_box)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_4)

        self.screenshot_label = QLabel(Form)
        self.screenshot_label.setObjectName(u"screenshot_label")
        self.screenshot_label.setMinimumSize(QSize(288, 162))
        self.screenshot_label.setMaximumSize(QSize(288, 162))
        self.screenshot_label.setScaledContents(True)

        self.horizontalLayout_8.addWidget(self.screenshot_label)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.verticalLayout_2)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 20))
        font = QFont()
        font.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"background: transparent;")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.radio_button_form_location_left = QRadioButton(self.frame)
        self.radio_button_form_location_left.setObjectName(u"radio_button_form_location_left")
        self.radio_button_form_location_left.setMinimumSize(QSize(70, 20))
        self.radio_button_form_location_left.setMaximumSize(QSize(70, 16777215))
        self.radio_button_form_location_left.setSizeIncrement(QSize(0, 0))
        self.radio_button_form_location_left.setFont(font)
        self.radio_button_form_location_left.setStyleSheet(u"background: transparent;")
        self.radio_button_form_location_left.setChecked(False)

        self.horizontalLayout.addWidget(self.radio_button_form_location_left)

        self.radio_button_form_location_right = QRadioButton(self.frame)
        self.radio_button_form_location_right.setObjectName(u"radio_button_form_location_right")
        self.radio_button_form_location_right.setMinimumSize(QSize(0, 20))
        self.radio_button_form_location_right.setFont(font)
        self.radio_button_form_location_right.setStyleSheet(u"background: transparent;")
        self.radio_button_form_location_right.setChecked(True)

        self.horizontalLayout.addWidget(self.radio_button_form_location_right)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.frame)


        self.verticalLayout_3.addLayout(self.formLayout)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, 10, -1, -1)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.push_button_ok = QPushButton(Form)
        self.push_button_ok.setObjectName(u"push_button_ok")
        self.push_button_ok.setMinimumSize(QSize(100, 30))
        self.push_button_ok.setMaximumSize(QSize(16777215, 30))
        self.push_button_ok.setFont(font)

        self.horizontalLayout_6.addWidget(self.push_button_ok)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)


        self.gridLayout_2.addLayout(self.verticalLayout_3, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u9009\u62e9\u5c4f\u5e55\uff1a", None))
        self.screenshot_label.setText("")
        self.label_2.setText(QCoreApplication.translate("Form", u"\u7a97\u53e3\u4f4d\u7f6e\uff1a", None))
        self.radio_button_form_location_left.setText(QCoreApplication.translate("Form", u"\u5de6\u4fa7", None))
        self.radio_button_form_location_right.setText(QCoreApplication.translate("Form", u"\u53f3\u4fa7", None))
        self.push_button_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
    # retranslateUi

