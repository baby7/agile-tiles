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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(256, 287)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.formLayout.setVerticalSpacing(15)
        self.formLayout.setContentsMargins(-1, 10, -1, 10)
        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setStyleSheet(u"background: transparent;")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_6)

        self.check_box_self_starting = QCheckBox(Form)
        self.check_box_self_starting.setObjectName(u"check_box_self_starting")
        self.check_box_self_starting.setMinimumSize(QSize(0, 20))
        font = QFont()
        font.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font.setPointSize(10)
        self.check_box_self_starting.setFont(font)
        self.check_box_self_starting.setChecked(True)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.check_box_self_starting)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"background: transparent;")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_5)

        self.check_box_keyboard = QCheckBox(Form)
        self.check_box_keyboard.setObjectName(u"check_box_keyboard")
        self.check_box_keyboard.setMinimumSize(QSize(0, 20))
        self.check_box_keyboard.setFont(font)
        self.check_box_keyboard.setChecked(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.check_box_keyboard)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 20))
        self.label.setFont(font)
        self.label.setStyleSheet(u"background: transparent;")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label)

        self.combo_box_main_keyboard = QComboBox(Form)
        self.combo_box_main_keyboard.setObjectName(u"combo_box_main_keyboard")
        self.combo_box_main_keyboard.setMinimumSize(QSize(0, 20))
        self.combo_box_main_keyboard.setFont(font)
        self.combo_box_main_keyboard.setStyleSheet(u"")
        self.combo_box_main_keyboard.setEditable(False)
        self.combo_box_main_keyboard.setDuplicatesEnabled(False)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.combo_box_main_keyboard)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 20))
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"background: transparent;")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_2)

        self.combo_box_vice_keyboard = QComboBox(Form)
        self.combo_box_vice_keyboard.setObjectName(u"combo_box_vice_keyboard")
        self.combo_box_vice_keyboard.setMinimumSize(QSize(0, 20))
        self.combo_box_vice_keyboard.setFont(font)
        self.combo_box_vice_keyboard.setStyleSheet(u"")
        self.combo_box_vice_keyboard.setEditable(False)
        self.combo_box_vice_keyboard.setDuplicatesEnabled(False)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.combo_box_vice_keyboard)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.line)


        self.verticalLayout.addLayout(self.formLayout)

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
        self.label_6.setText(QCoreApplication.translate("Form", u"\u5f00\u673a\u81ea\u542f\u52a8\uff1a", None))
        self.check_box_self_starting.setText(QCoreApplication.translate("Form", u"\u542f\u7528", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u754c\u9762\u5feb\u6377\u952e\uff1a", None))
        self.check_box_keyboard.setText(QCoreApplication.translate("Form", u"\u542f\u7528", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u4e3b\u8981\u7684\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u6b21\u8981\u7684\uff1a", None))
        self.push_button_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
    # retranslateUi

