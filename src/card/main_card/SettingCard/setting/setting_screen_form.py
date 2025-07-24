# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setting_screen_form.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFontComboBox,
    QFormLayout, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(590, 662)
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.formLayout.setHorizontalSpacing(6)
        self.formLayout.setVerticalSpacing(20)
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
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
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

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 20))
        self.label.setFont(font)
        self.label.setStyleSheet(u"background: transparent;")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label)

        self.frame_4 = QFrame(Form)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setStyleSheet(u"")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_4)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.radio_button_form_animation_line = QRadioButton(self.frame_4)
        self.radio_button_form_animation_line.setObjectName(u"radio_button_form_animation_line")
        self.radio_button_form_animation_line.setMinimumSize(QSize(70, 20))
        self.radio_button_form_animation_line.setMaximumSize(QSize(70, 16777215))
        self.radio_button_form_animation_line.setSizeIncrement(QSize(0, 0))
        self.radio_button_form_animation_line.setFont(font)
        self.radio_button_form_animation_line.setStyleSheet(u"background: transparent;")
        self.radio_button_form_animation_line.setChecked(False)

        self.horizontalLayout_7.addWidget(self.radio_button_form_animation_line)

        self.radio_button_form_animation_elastic = QRadioButton(self.frame_4)
        self.radio_button_form_animation_elastic.setObjectName(u"radio_button_form_animation_elastic")
        self.radio_button_form_animation_elastic.setMinimumSize(QSize(0, 20))
        self.radio_button_form_animation_elastic.setFont(font)
        self.radio_button_form_animation_elastic.setStyleSheet(u"background: transparent;")
        self.radio_button_form_animation_elastic.setChecked(True)

        self.horizontalLayout_7.addWidget(self.radio_button_form_animation_elastic)


        self.gridLayout_6.addLayout(self.horizontalLayout_7, 0, 0, 1, 1)


        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.frame_4)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 20))
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(u"background: transparent;")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.spin_box_form_animation_time = QSpinBox(Form)
        self.spin_box_form_animation_time.setObjectName(u"spin_box_form_animation_time")
        self.spin_box_form_animation_time.setMinimumSize(QSize(0, 20))
        self.spin_box_form_animation_time.setFont(font)
        self.spin_box_form_animation_time.setMinimum(1)
        self.spin_box_form_animation_time.setMaximum(1000)
        self.spin_box_form_animation_time.setSingleStep(10)

        self.horizontalLayout_2.addWidget(self.spin_box_form_animation_time)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(0, 20))
        self.label_5.setFont(font)
        self.label_5.setStyleSheet(u"background: transparent;")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.check_box_side_popup = QCheckBox(Form)
        self.check_box_side_popup.setObjectName(u"check_box_side_popup")
        self.check_box_side_popup.setMinimumSize(QSize(0, 20))
        self.check_box_side_popup.setFont(font)
        self.check_box_side_popup.setStyleSheet(u"background: transparent;")
        self.check_box_side_popup.setChecked(True)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.check_box_side_popup)

        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(0, 20))
        self.label_6.setFont(font)
        self.label_6.setStyleSheet(u"background: transparent;")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_6)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.spin_box_side_popup_animation_time = QSpinBox(Form)
        self.spin_box_side_popup_animation_time.setObjectName(u"spin_box_side_popup_animation_time")
        self.spin_box_side_popup_animation_time.setMinimumSize(QSize(0, 20))
        self.spin_box_side_popup_animation_time.setFont(font)
        self.spin_box_side_popup_animation_time.setMinimum(1)
        self.spin_box_side_popup_animation_time.setMaximum(1000)
        self.spin_box_side_popup_animation_time.setSingleStep(10)

        self.horizontalLayout_3.addWidget(self.spin_box_side_popup_animation_time)


        self.formLayout.setLayout(5, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.label_8 = QLabel(Form)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(0, 20))
        self.label_8.setFont(font)
        self.label_8.setStyleSheet(u"background: transparent;")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_8)

        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setStyleSheet(u"")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.radio_button_form_hide_by_mouse_forever = QRadioButton(self.frame_2)
        self.radio_button_form_hide_by_mouse_forever.setObjectName(u"radio_button_form_hide_by_mouse_forever")
        self.radio_button_form_hide_by_mouse_forever.setMinimumSize(QSize(70, 20))
        self.radio_button_form_hide_by_mouse_forever.setMaximumSize(QSize(70, 16777215))
        self.radio_button_form_hide_by_mouse_forever.setSizeIncrement(QSize(0, 0))
        self.radio_button_form_hide_by_mouse_forever.setFont(font)
        self.radio_button_form_hide_by_mouse_forever.setStyleSheet(u"background: transparent;")
        self.radio_button_form_hide_by_mouse_forever.setChecked(False)

        self.horizontalLayout_4.addWidget(self.radio_button_form_hide_by_mouse_forever)

        self.radio_button_form_hide_by_mouse_only_mouse = QRadioButton(self.frame_2)
        self.radio_button_form_hide_by_mouse_only_mouse.setObjectName(u"radio_button_form_hide_by_mouse_only_mouse")
        self.radio_button_form_hide_by_mouse_only_mouse.setMinimumSize(QSize(0, 20))
        self.radio_button_form_hide_by_mouse_only_mouse.setFont(font)
        self.radio_button_form_hide_by_mouse_only_mouse.setStyleSheet(u"background: transparent;")
        self.radio_button_form_hide_by_mouse_only_mouse.setChecked(True)

        self.horizontalLayout_4.addWidget(self.radio_button_form_hide_by_mouse_only_mouse)


        self.gridLayout_3.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)


        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.frame_2)

        self.label_9 = QLabel(Form)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(0, 20))
        self.label_9.setFont(font)
        self.label_9.setStyleSheet(u"background: transparent;")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_9)

        self.frame_3 = QFrame(Form)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setStyleSheet(u"")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_3)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.radio_button_menu_location_left = QRadioButton(self.frame_3)
        self.radio_button_menu_location_left.setObjectName(u"radio_button_menu_location_left")
        self.radio_button_menu_location_left.setMinimumSize(QSize(70, 20))
        self.radio_button_menu_location_left.setMaximumSize(QSize(70, 16777215))
        self.radio_button_menu_location_left.setSizeIncrement(QSize(0, 0))
        self.radio_button_menu_location_left.setFont(font)
        self.radio_button_menu_location_left.setStyleSheet(u"background: transparent;")
        self.radio_button_menu_location_left.setChecked(False)

        self.horizontalLayout_5.addWidget(self.radio_button_menu_location_left)

        self.radio_button_menu_location_right = QRadioButton(self.frame_3)
        self.radio_button_menu_location_right.setObjectName(u"radio_button_menu_location_right")
        self.radio_button_menu_location_right.setMinimumSize(QSize(0, 20))
        self.radio_button_menu_location_right.setFont(font)
        self.radio_button_menu_location_right.setStyleSheet(u"background: transparent;")
        self.radio_button_menu_location_right.setChecked(True)

        self.horizontalLayout_5.addWidget(self.radio_button_menu_location_right)


        self.gridLayout_4.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)


        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.frame_3)

        self.label_10 = QLabel(Form)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(0, 20))
        self.label_10.setFont(font)
        self.label_10.setStyleSheet(u"background: transparent;")

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.label_10)

        self.font_combo_box = QFontComboBox(Form)
        self.font_combo_box.setObjectName(u"font_combo_box")
        self.font_combo_box.setEditable(False)

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.font_combo_box)

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
        self.label_2.setText(QCoreApplication.translate("Form", u"\u7a97\u53e3\u4f4d\u7f6e\uff1a", None))
        self.radio_button_form_location_left.setText(QCoreApplication.translate("Form", u"\u5de6\u4fa7", None))
        self.radio_button_form_location_right.setText(QCoreApplication.translate("Form", u"\u53f3\u4fa7", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u7a97\u53e3\u5f39\u51fa\u52a8\u753b\u7c7b\u578b\uff1a", None))
        self.radio_button_form_animation_line.setText(QCoreApplication.translate("Form", u"\u7ebf\u6027", None))
        self.radio_button_form_animation_elastic.setText(QCoreApplication.translate("Form", u"\u5f39\u529b\u5341\u8db3", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u7a97\u53e3\u5f39\u51fa\u52a8\u753b\u65f6\u95f4(\u6beb\u79d2)\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u662f\u5426\u542f\u52a8\u4fa7\u8fb9\u5f39\u51fa\u529f\u80fd\uff1a", None))
        self.check_box_side_popup.setText(QCoreApplication.translate("Form", u"\u542f\u7528", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u4fa7\u8fb9\u5f39\u51fa\u5ef6\u8fdf\u65f6\u95f4(\u6beb\u79d2)\uff1a", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u9f20\u6807\u79bb\u5f00\u9690\u85cf\u7a97\u53e3\uff1a", None))
        self.radio_button_form_hide_by_mouse_forever.setText(QCoreApplication.translate("Form", u"\u6c38\u8fdc", None))
        self.radio_button_form_hide_by_mouse_only_mouse.setText(QCoreApplication.translate("Form", u"\u4ec5\u9f20\u6807\u89e6\u53d1\u5f39\u51fa\u60c5\u51b5", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"\u83dc\u5355\u680f\u4f4d\u7f6e\uff1a", None))
        self.radio_button_menu_location_left.setText(QCoreApplication.translate("Form", u"\u5de6\u4fa7", None))
        self.radio_button_menu_location_right.setText(QCoreApplication.translate("Form", u"\u53f3\u4fa7", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"\u5b57\u4f53\u8bbe\u7f6e\uff1a", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u9009\u62e9\u5c4f\u5e55\uff1a", None))
        self.screenshot_label.setText("")
        self.push_button_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
    # retranslateUi

