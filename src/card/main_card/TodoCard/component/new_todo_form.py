# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_todo_form.ui'
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
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(490, 736)
        self.gridLayout_3 = QGridLayout(Form)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.top_widget = QWidget(Form)
        self.top_widget.setObjectName(u"top_widget")
        self.top_widget.setStyleSheet(u"    border-style: solid;\n"
"    border-radius: 10px;\n"
"    border: 0px solid black;\n"
"    color: rgb(0, 0, 0);\n"
"    border-color: rgba(255, 255, 255, 1);\n"
"    background-color: rgba(255, 255, 255, 160);")
        self.gridLayout = QGridLayout(self.top_widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_12 = QLabel(self.top_widget)
        self.label_12.setObjectName(u"label_12")
        font = QFont()
        font.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font.setPointSize(10)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet(u"background: transparent;")

        self.verticalLayout_3.addWidget(self.label_12)

        self.combo_box = QComboBox(self.top_widget)
        self.combo_box.setObjectName(u"combo_box")
        font1 = QFont()
        font1.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font1.setPointSize(11)
        self.combo_box.setFont(font1)
        self.combo_box.setStyleSheet(u"")

        self.verticalLayout_3.addWidget(self.combo_box)

        self.label_8 = QLabel(self.top_widget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)
        self.label_8.setStyleSheet(u"background: transparent;")

        self.verticalLayout_3.addWidget(self.label_8)

        self.line_edit_title = QLineEdit(self.top_widget)
        self.line_edit_title.setObjectName(u"line_edit_title")
        self.line_edit_title.setFont(font1)
        self.line_edit_title.setStyleSheet(u"")

        self.verticalLayout_3.addWidget(self.line_edit_title)

        self.label_9 = QLabel(self.top_widget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)
        self.label_9.setStyleSheet(u"background: transparent;")

        self.verticalLayout_3.addWidget(self.label_9)

        self.text_edit_des = QTextEdit(self.top_widget)
        self.text_edit_des.setObjectName(u"text_edit_des")
        self.text_edit_des.setFont(font)
        self.text_edit_des.setStyleSheet(u"")

        self.verticalLayout_3.addWidget(self.text_edit_des)

        self.label_16 = QLabel(self.top_widget)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font)
        self.label_16.setStyleSheet(u"background: transparent;")

        self.verticalLayout_3.addWidget(self.label_16)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setSpacing(5)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.push_button_importance_exigency = QPushButton(self.top_widget)
        self.push_button_importance_exigency.setObjectName(u"push_button_importance_exigency")
        self.push_button_importance_exigency.setMinimumSize(QSize(140, 25))
        self.push_button_importance_exigency.setFont(font)
        self.push_button_importance_exigency.setStyleSheet(u"    border-style: solid;\n"
"    border-radius: 10px;\n"
"    border: 1px solid black;\n"
"    color: rgb(255, 255, 255);\n"
"    border-color: rgb(0, 0, 0);\n"
"    background-color: rgba(255, 46, 44, 0.6);")

        self.gridLayout_2.addWidget(self.push_button_importance_exigency, 0, 0, 1, 1)

        self.push_button_importance_no_exigency = QPushButton(self.top_widget)
        self.push_button_importance_no_exigency.setObjectName(u"push_button_importance_no_exigency")
        self.push_button_importance_no_exigency.setMinimumSize(QSize(140, 25))
        self.push_button_importance_no_exigency.setFont(font)
        self.push_button_importance_no_exigency.setStyleSheet(u"    border-style: solid;\n"
"    border-radius: 10px;\n"
"    border: 0px groove gray;\n"
"    color: rgb(255, 255, 255);\n"
"    border-color: rgb(0, 0, 0);\n"
"    background-color: rgba(243, 207, 19, 0.6);")
        self.push_button_importance_no_exigency.setIconSize(QSize(30, 25))

        self.gridLayout_2.addWidget(self.push_button_importance_no_exigency, 0, 1, 1, 1)

        self.push_button_no_importance_exigency = QPushButton(self.top_widget)
        self.push_button_no_importance_exigency.setObjectName(u"push_button_no_importance_exigency")
        self.push_button_no_importance_exigency.setMinimumSize(QSize(140, 25))
        self.push_button_no_importance_exigency.setFont(font)
        self.push_button_no_importance_exigency.setStyleSheet(u"    border-style: solid;\n"
"    border-radius: 10px;\n"
"    border: 0px groove gray;\n"
"    color: rgb(255, 255, 255);\n"
"    border-color: rgb(0, 0, 0);\n"
"    background-color: rgba(20, 185, 62, 0.6);")

        self.gridLayout_2.addWidget(self.push_button_no_importance_exigency, 1, 0, 1, 1)

        self.push_button_no_importance_no_exigency = QPushButton(self.top_widget)
        self.push_button_no_importance_no_exigency.setObjectName(u"push_button_no_importance_no_exigency")
        self.push_button_no_importance_no_exigency.setMinimumSize(QSize(140, 25))
        self.push_button_no_importance_no_exigency.setFont(font)
        self.push_button_no_importance_no_exigency.setStyleSheet(u"    border-style: solid;\n"
"    border-radius: 10px;\n"
"    border: 0px groove gray;\n"
"    color: rgb(255, 255, 255);\n"
"    border-color: rgb(0, 0, 0);\n"
"    background-color: rgba(4, 115, 247, 0.6);")

        self.gridLayout_2.addWidget(self.push_button_no_importance_no_exigency, 1, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_11 = QLabel(self.top_widget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)
        self.label_11.setStyleSheet(u"background: transparent;")

        self.horizontalLayout_4.addWidget(self.label_11)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.check_box = QCheckBox(self.top_widget)
        self.check_box.setObjectName(u"check_box")
        self.check_box.setMinimumSize(QSize(20, 20))
        self.check_box.setMaximumSize(QSize(99999, 20))

        self.horizontalLayout_5.addWidget(self.check_box)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.push_button_date = QPushButton(self.top_widget)
        self.push_button_date.setObjectName(u"push_button_date")
        self.push_button_date.setMinimumSize(QSize(0, 25))
        self.push_button_date.setFont(font)
        self.push_button_date.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.push_button_date)

        self.push_button_time = QPushButton(self.top_widget)
        self.push_button_time.setObjectName(u"push_button_time")
        self.push_button_time.setMinimumSize(QSize(0, 25))
        self.push_button_time.setFont(font)
        self.push_button_time.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.push_button_time)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.label_2 = QLabel(self.top_widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 0))

        self.verticalLayout_3.addWidget(self.label_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.push_button_cancel = QPushButton(self.top_widget)
        self.push_button_cancel.setObjectName(u"push_button_cancel")
        self.push_button_cancel.setMinimumSize(QSize(80, 30))
        self.push_button_cancel.setMaximumSize(QSize(16777215, 30))
        font2 = QFont()
        font2.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setKerning(True)
        self.push_button_cancel.setFont(font2)
        self.push_button_cancel.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.push_button_cancel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.push_button_ok = QPushButton(self.top_widget)
        self.push_button_ok.setObjectName(u"push_button_ok")
        self.push_button_ok.setMinimumSize(QSize(80, 30))
        self.push_button_ok.setMaximumSize(QSize(16777215, 30))
        self.push_button_ok.setFont(font2)
        self.push_button_ok.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.push_button_ok)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.verticalLayout_15.addLayout(self.verticalLayout_3)


        self.gridLayout.addLayout(self.verticalLayout_15, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.top_widget)

        self.bottom_widget = QWidget(Form)
        self.bottom_widget.setObjectName(u"bottom_widget")
        self.bottom_widget.setStyleSheet(u"    border-style: solid;\n"
"    border-radius: 10px;\n"
"    border: 0px solid black;\n"
"    color: rgb(0, 0, 0);\n"
"    border-color: rgba(255, 255, 255, 1);\n"
"    background-color: rgba(255, 255, 255, 160);")
        self.gridLayout_4 = QGridLayout(self.bottom_widget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label_19 = QLabel(self.bottom_widget)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font)
        self.label_19.setStyleSheet(u"background: transparent;")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_19)

        self.label_show_create_time = QLabel(self.bottom_widget)
        self.label_show_create_time.setObjectName(u"label_show_create_time")
        self.label_show_create_time.setFont(font)
        self.label_show_create_time.setStyleSheet(u"background: transparent;")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.label_show_create_time)

        self.label_18 = QLabel(self.bottom_widget)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font)
        self.label_18.setStyleSheet(u"background: transparent;")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_18)

        self.label_show_complete = QLabel(self.bottom_widget)
        self.label_show_complete.setObjectName(u"label_show_complete")
        self.label_show_complete.setFont(font)
        self.label_show_complete.setStyleSheet(u"background: transparent;")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.label_show_complete)

        self.label_20 = QLabel(self.bottom_widget)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font)
        self.label_20.setStyleSheet(u"background: transparent;")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.label_20)

        self.label_show_complete_time = QLabel(self.bottom_widget)
        self.label_show_complete_time.setObjectName(u"label_show_complete_time")
        self.label_show_complete_time.setFont(font)
        self.label_show_complete_time.setStyleSheet(u"background: transparent;")

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.label_show_complete_time)


        self.gridLayout_4.addLayout(self.formLayout_3, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.bottom_widget)


        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"\u5206\u7c7b\uff1a", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u6807\u9898\uff1a", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"\u5185\u5bb9\uff1a", None))
        self.label_16.setText(QCoreApplication.translate("Form", u"\u7a0b\u5ea6\uff1a", None))
        self.push_button_importance_exigency.setText(QCoreApplication.translate("Form", u"\u91cd\u8981\u4e14\u7d27\u6025", None))
        self.push_button_importance_no_exigency.setText(QCoreApplication.translate("Form", u"\u91cd\u8981\u4e0d\u7d27\u6025", None))
        self.push_button_no_importance_exigency.setText(QCoreApplication.translate("Form", u"\u7d27\u6025\u4e0d\u91cd\u8981", None))
        self.push_button_no_importance_no_exigency.setText(QCoreApplication.translate("Form", u"\u4e0d\u91cd\u8981\u4e0d\u7d27\u6025", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"\u95f9\u949f(\u4e0d\u91cd\u590d)\uff1a", None))
        self.check_box.setText(QCoreApplication.translate("Form", u"\u542f\u7528\u95f9\u949f", None))
        self.push_button_date.setText(QCoreApplication.translate("Form", u"2024-05-13", None))
        self.push_button_time.setText(QCoreApplication.translate("Form", u"00:00:00", None))
        self.label_2.setText("")
        self.push_button_cancel.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
        self.push_button_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.label_19.setText(QCoreApplication.translate("Form", u"\u521b\u5efa\u65f6\u95f4\uff1a", None))
        self.label_show_create_time.setText(QCoreApplication.translate("Form", u"--", None))
        self.label_18.setText(QCoreApplication.translate("Form", u"\u662f\u5426\u5b8c\u6210\uff1a", None))
        self.label_show_complete.setText(QCoreApplication.translate("Form", u"--", None))
        self.label_20.setText(QCoreApplication.translate("Form", u"\u5b8c\u6210\u65f6\u95f4\uff1a", None))
        self.label_show_complete_time.setText(QCoreApplication.translate("Form", u"--", None))
    # retranslateUi

