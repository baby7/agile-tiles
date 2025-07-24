# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'card_permutation_form.ui'
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
from PySide6.QtWidgets import (QApplication, QGraphicsView, QGridLayout, QHBoxLayout,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1017, 827)
        Form.setMinimumSize(QSize(500, 500))
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.manage_card_layout = QVBoxLayout()
        self.manage_card_layout.setObjectName(u"manage_card_layout")
        self.widget_menu = QWidget(Form)
        self.widget_menu.setObjectName(u"widget_menu")
        self.widget_menu.setMinimumSize(QSize(0, 0))
        self.widget_menu.setMaximumSize(QSize(16777215, 60))
        font = QFont()
        font.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
        font.setPointSize(10)
        self.widget_menu.setFont(font)
        self.widget_menu.setStyleSheet(u"QWidget {\n"
"    border-style: solid;\n"
"    border-radius: 10px;\n"
"    border: 0px solid black;\n"
"    color: rgb(0, 0, 0);\n"
"    border-color: rgba(255, 255, 255, 1);\n"
"    background-color: rgba(0, 0, 0,25);\n"
"}")
        self.gridLayout_7 = QGridLayout(self.widget_menu)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)

        self.widget_left = QWidget(self.widget_menu)
        self.widget_left.setObjectName(u"widget_left")
        self.widget_left.setMinimumSize(QSize(200, 0))
        self.widget_left.setStyleSheet(u"QWidget {\n"
"border-style: solid;\n"
"border-radius: 10px;\n"
"border: 1px solid white;\n"
"background-color:rgba(255, 255, 255, 200);\n"
"}")
        self.gridLayout_8 = QGridLayout(self.widget_left)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.add_btn = QPushButton(self.widget_left)
        self.add_btn.setObjectName(u"add_btn")
        self.add_btn.setMinimumSize(QSize(0, 20))
        self.add_btn.setMaximumSize(QSize(16777215, 16777215))
        self.add_btn.setStyleSheet(u"QPushButton {\n"
"border-radius: 10px;\n"
"border: none;\n"
"background: rgba(0, 0, 0, 0);\n"
"text-align:center;\n"
"}\n"
"QPushButton:hover {\n"
"font-weight: bold;\n"
"}")

        self.horizontalLayout_2.addWidget(self.add_btn)

        self.delete_btn = QPushButton(self.widget_left)
        self.delete_btn.setObjectName(u"delete_btn")
        self.delete_btn.setMinimumSize(QSize(0, 20))
        self.delete_btn.setMaximumSize(QSize(16777215, 16777215))
        self.delete_btn.setStyleSheet(u"QPushButton {\n"
"border-radius: 10px;\n"
"border: none;\n"
"background: rgba(0, 0, 0, 0);\n"
"text-align:center;\n"
"}\n"
"QPushButton:hover {\n"
"font-weight: bold;\n"
"}")

        self.horizontalLayout_2.addWidget(self.delete_btn)


        self.gridLayout_8.addLayout(self.horizontalLayout_2, 0, 1, 1, 1)


        self.horizontalLayout_5.addWidget(self.widget_left)

        self.widget_middle = QWidget(self.widget_menu)
        self.widget_middle.setObjectName(u"widget_middle")
        self.widget_middle.setMinimumSize(QSize(200, 0))
        self.widget_middle.setStyleSheet(u"QWidget {\n"
"border-style: solid;\n"
"border-radius: 10px;\n"
"border: 1px solid white;\n"
"background-color:rgba(255, 255, 255, 200);\n"
"}")
        self.gridLayout_6 = QGridLayout(self.widget_middle)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.push_button_add_box_width = QPushButton(self.widget_middle)
        self.push_button_add_box_width.setObjectName(u"push_button_add_box_width")
        self.push_button_add_box_width.setMinimumSize(QSize(0, 20))
        self.push_button_add_box_width.setMaximumSize(QSize(16777215, 16777215))
        self.push_button_add_box_width.setStyleSheet(u"QPushButton {\n"
"border-radius: 10px;\n"
"border: none;\n"
"background: rgba(0, 0, 0, 0);\n"
"text-align:center;\n"
"}\n"
"QPushButton:hover {\n"
"font-weight: bold;\n"
"}")

        self.horizontalLayout_3.addWidget(self.push_button_add_box_width)

        self.push_button_reduce_box_width = QPushButton(self.widget_middle)
        self.push_button_reduce_box_width.setObjectName(u"push_button_reduce_box_width")
        self.push_button_reduce_box_width.setMinimumSize(QSize(0, 20))
        self.push_button_reduce_box_width.setMaximumSize(QSize(16777215, 16777215))
        self.push_button_reduce_box_width.setStyleSheet(u"QPushButton {\n"
"border-radius: 10px;\n"
"border: none;\n"
"background: rgba(0, 0, 0, 0);\n"
"text-align:center;\n"
"}\n"
"QPushButton:hover {\n"
"font-weight: bold;\n"
"}")

        self.horizontalLayout_3.addWidget(self.push_button_reduce_box_width)


        self.gridLayout_6.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)


        self.horizontalLayout_5.addWidget(self.widget_middle)

        self.widget_right = QWidget(self.widget_menu)
        self.widget_right.setObjectName(u"widget_right")
        self.widget_right.setMinimumSize(QSize(90, 0))
        self.widget_right.setMaximumSize(QSize(250, 16777215))
        self.widget_right.setFont(font)
        self.widget_right.setStyleSheet(u"QWidget {\n"
"border-style: solid;\n"
"border-radius: 10px;\n"
"border: 1px solid white;\n"
"background-color:rgba(255, 255, 255, 200);\n"
"}")
        self.gridLayout_4 = QGridLayout(self.widget_right)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.push_button_ok = QPushButton(self.widget_right)
        self.push_button_ok.setObjectName(u"push_button_ok")
        self.push_button_ok.setMinimumSize(QSize(0, 20))
        self.push_button_ok.setMaximumSize(QSize(16777215, 16777215))
        self.push_button_ok.setFont(font)
        self.push_button_ok.setStyleSheet(u"QPushButton {\n"
"border-radius: 10px;\n"
"border: none;\n"
"background: rgba(0, 0, 0, 0);\n"
"text-align:center;\n"
"}\n"
"QPushButton:hover {\n"
"font-weight: bold;\n"
"}")

        self.horizontalLayout_4.addWidget(self.push_button_ok)


        self.gridLayout_4.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)


        self.horizontalLayout_5.addWidget(self.widget_right)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.gridLayout_7.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)


        self.manage_card_layout.addWidget(self.widget_menu)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 0))
        self.widget.setFont(font)
        self.widget.setStyleSheet(u"QWidget {\n"
"    border-style: solid;\n"
"    border-radius: 10px;\n"
"    border: 0px solid black;\n"
"    color: rgb(0, 0, 0);\n"
"    border-color: rgba(255, 255, 255, 1);\n"
"    background-color: rgba(0, 0, 0,25);\n"
"}")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.graphicsView = QGraphicsView(self.widget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setMinimumSize(QSize(0, 0))
        self.graphicsView.setStyleSheet(u"QWidget {\n"
"    border-style: solid;\n"
"    border-radius: 10px;\n"
"    border: 0px solid black;\n"
"    color: rgb(0, 0, 0);\n"
"    border-color: rgba(255, 255, 255, 1);\n"
"    background-color: rgba(255, 255, 255,0);\n"
"}")

        self.gridLayout.addWidget(self.graphicsView, 1, 0, 1, 1)


        self.horizontalLayout.addWidget(self.widget)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.manage_card_layout.addLayout(self.horizontalLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.manage_card_layout.addItem(self.verticalSpacer_2)


        self.gridLayout_2.addLayout(self.manage_card_layout, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.add_btn.setText(QCoreApplication.translate("Form", u"\u5361\u7247\u5546\u5e97", None))
        self.delete_btn.setText(QCoreApplication.translate("Form", u"\u5220\u9664\u9009\u4e2d", None))
        self.push_button_add_box_width.setText(QCoreApplication.translate("Form", u"\u5e03\u5c40\u53d8\u5bbd", None))
        self.push_button_reduce_box_width.setText(QCoreApplication.translate("Form", u"\u5e03\u5c40\u53d8\u7a84", None))
        self.push_button_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
    # retranslateUi

