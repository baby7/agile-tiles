# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setting_theme_form.ui'
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
    QRadioButton, QSizePolicy, QSlider, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(337, 202)
        self.gridLayout_3 = QGridLayout(Form)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.formLayout.setHorizontalSpacing(6)
        self.formLayout.setVerticalSpacing(15)
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 20))
        font = QFont()
        font.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"background: transparent;")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.radio_button_color_light = QRadioButton(self.frame)
        self.radio_button_color_light.setObjectName(u"radio_button_color_light")
        self.radio_button_color_light.setMinimumSize(QSize(80, 20))
        self.radio_button_color_light.setMaximumSize(QSize(80, 16777215))
        self.radio_button_color_light.setFont(font)
        self.radio_button_color_light.setCheckable(True)
        self.radio_button_color_light.setChecked(True)

        self.horizontalLayout.addWidget(self.radio_button_color_light)

        self.radio_button_color_dark = QRadioButton(self.frame)
        self.radio_button_color_dark.setObjectName(u"radio_button_color_dark")
        self.radio_button_color_dark.setMinimumSize(QSize(80, 20))
        self.radio_button_color_dark.setMaximumSize(QSize(80, 16777215))
        self.radio_button_color_dark.setSizeIncrement(QSize(55, 0))
        self.radio_button_color_dark.setFont(font)

        self.horizontalLayout.addWidget(self.radio_button_color_dark)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.frame)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 20))
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(u"background: transparent;")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(10)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.combo_box_mode = QComboBox(Form)
        self.combo_box_mode.setObjectName(u"combo_box_mode")

        self.horizontalLayout_7.addWidget(self.combo_box_mode)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_7)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 20))
        self.label_4.setFont(font)
        self.label_4.setStyleSheet(u"background: transparent;")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontal_slider_transparency = QSlider(Form)
        self.horizontal_slider_transparency.setObjectName(u"horizontal_slider_transparency")
        self.horizontal_slider_transparency.setMinimum(0)
        self.horizontal_slider_transparency.setMaximum(100)
        self.horizontal_slider_transparency.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.horizontal_slider_transparency)

        self.label_transparency = QLabel(Form)
        self.label_transparency.setObjectName(u"label_transparency")
        self.label_transparency.setMinimumSize(QSize(35, 0))
        self.label_transparency.setStyleSheet(u"background-color: transparent;")

        self.horizontalLayout_2.addWidget(self.label_transparency)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_2)


        self.verticalLayout_3.addLayout(self.formLayout)

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


        self.gridLayout_3.addLayout(self.verticalLayout_3, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u4e3b\u9898\u989c\u8272\uff1a", None))
        self.radio_button_color_light.setText(QCoreApplication.translate("Form", u"\u6d45\u8272", None))
        self.radio_button_color_dark.setText(QCoreApplication.translate("Form", u"\u6df1\u8272", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u4e3b\u9898\u6a21\u5f0f\uff1a", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u900f\u660e\u5ea6\uff1a", None))
        self.label_transparency.setText(QCoreApplication.translate("Form", u"100%", None))
        self.push_button_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
    # retranslateUi

