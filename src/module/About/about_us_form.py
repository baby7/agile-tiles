# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about_us_form.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(337, 394)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.label_icon = QLabel(Form)
        self.label_icon.setObjectName(u"label_icon")
        self.label_icon.setMinimumSize(QSize(100, 100))
        self.label_icon.setMaximumSize(QSize(150, 150))
        self.label_icon.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_icon)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label_title = QLabel(Form)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setMaximumSize(QSize(16777215, 40))
        self.label_title.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_title)

        self.label_copyright = QLabel(Form)
        self.label_copyright.setObjectName(u"label_copyright")
        self.label_copyright.setMaximumSize(QSize(16777215, 40))
        self.label_copyright.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_copyright)

        self.push_button_link = QPushButton(Form)
        self.push_button_link.setObjectName(u"push_button_link")

        self.verticalLayout.addWidget(self.push_button_link)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.label_framework = QLabel(Form)
        self.label_framework.setObjectName(u"label_framework")
        self.label_framework.setMaximumSize(QSize(16777215, 40))
        self.label_framework.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_framework)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_icon.setText(QCoreApplication.translate("Form", u"\u56fe\u6807", None))
        self.label_title.setText(QCoreApplication.translate("Form", u"\u7075\u5361\u9762\u677f v0.1.1", None))
        self.label_copyright.setText(QCoreApplication.translate("Form", u"Copyright \u00a9 2025", None))
        self.push_button_link.setText(QCoreApplication.translate("Form", u"https://www.agiletiles.com/index.html", None))
        self.label_framework.setText(QCoreApplication.translate("Form", u"\u57fa\u4e8ePySide6\u5f00\u53d1", None))
    # retranslateUi

