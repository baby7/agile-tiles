# -*- coding: utf-8 -*-
import enum
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6 import QtWidgets


class ENUM_TimeMode(enum.Enum):
    TimeMode_Year = "TimeMode_Year"         # 年
    TimeMode_Month = "TimeMode_Month"       # 月
    TimeMode_Day = "TimeMode_Day"           # 日
    TimeMode_Hour = "TimeMode_Hour"           # 小时
    TimeMode_Minute = "TimeMode_Minute"     # 分钟
    TimeMode_Second = "TimeMode_Second"     # 秒钟


class QSingleSelectTimeWidget(QWidget):

    m_enumTime = None          # 时间模式
    m_nCurrentData = None      # 当前数值

    def __init__(self, parent=None):
        super(QSingleSelectTimeWidget, self).__init__(parent)
        self.m_enumTime = ENUM_TimeMode.TimeMode_Hour       # 默认，小时制
        self.InitUI()
        self.LoadConnectMsg()

    def InitUI(self):
        # < button > 上一个
        qsBtnUpStyle = "QPushButton{border: none; outline:none;}"
        self.btnUp = QtWidgets.QPushButton(self)
        self.btnUp.setGeometry(20, 7, 20, 20)
        self.btnUp.setStyleSheet(qsBtnUpStyle)
        self.btnUp.setText("∧")
        # < button > 下一个
        qsBtnDownStyle = "QPushButton{border: none; outline:none;}"
        self.btnDown = QtWidgets.QPushButton(self)
        self.btnDown.setGeometry(20, 173, 20, 20)
        self.btnDown.setStyleSheet(qsBtnDownStyle)
        self.btnDown.setText("∨")
        # < label > 上一个时间
        qsPreviousStyle = "QLabel{border: none; font-size:16px;color:#999999;background-color: transparent;}"
        self.labPrevious = QtWidgets.QLabel(self)
        self.labPrevious.setGeometry(0, 34, 60, 44)
        self.labPrevious.setStyleSheet(qsPreviousStyle)
        self.labPrevious.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.labPrevious.setText("0")
        # < label > 当前时间
        qsCurrent = "QLabel{border: none; font-size:16px; font:blod; color:rgb(200, 200, 200);background-color: transparent;}"
        self.labCurrent = QtWidgets.QLabel(self)
        self.labCurrent.setGeometry(0, 78, 60, 44)
        self.labCurrent.setStyleSheet(qsCurrent)
        self.labCurrent.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.labCurrent.setText("0")
        # < label > 下一个时间
        qsNext = "QLabel{border: none; font-size:16px;color:#999999;background-color: transparent;}"
        self.labNext = QtWidgets.QLabel(self)
        self.labNext.setGeometry(0, 122, 60, 44)
        self.labNext.setStyleSheet(qsNext)
        self.labNext.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.labNext.setText("0")

    def refresh_theme(self, is_dark, top_button_icon, bottom_button_icon):
        if is_dark:
            qsCurrent = "QLabel{border: none; font-size:16px; font:blod; color:rgb(255, 255, 255); background-color: transparent;}"
        else:
            qsCurrent = "QLabel{border: none; font-size:16px; font:blod; color:rgb(0, 0, 0); background-color: transparent;}"
        self.labCurrent.setStyleSheet(qsCurrent)
        # 图标
        self.btnUp.setIcon(top_button_icon)
        self.btnDown.setIcon(bottom_button_icon)
        # qsBtnStyle = "QPushButton{border: none; background-color: transparent; outline:none;}"
        # self.btnUp.setStyleSheet(qsBtnStyle)
        # self.btnDown.setStyleSheet(qsBtnStyle)
        self.btnUp.setText("")
        self.btnDown.setText("")

    def SetCurrentShowTime(self, enumTime, data):
        self.m_enumTime = enumTime
        self.m_nCurrentData = data
        self.SetTimeChange(enumTime, data)

    def GetCurrentContent(self):
        return self.m_nCurrentData

    def wheelEvent(self, event):
        ptDegrees = event.angleDelta()
        # 当前 ptDegrees.y 大于0，滚轮放大，反之缩小
        if ptDegrees.y() > 0:
            # 滚轮向上
            self.OnBnClickedUp()
        else:
            # 滚轮向下
            self.OnBnClickedDown()
        super().wheelEvent(event)

    def OnBnClickedUp(self):
        # 当前数值向上移动-1，获取上一个展示label的数值
        nPreviousData = int(self.labPrevious.text())
        self.m_nCurrentData = nPreviousData
        # 重新设置数据变化
        self.SetTimeChange(self.m_enumTime, self.m_nCurrentData)

    def OnBnClickedDown(self):
        # 当前数值向下移动+1，获取下一个展示label的数值
        nNextData = int(self.labNext.text())
        self.m_nCurrentData = nNextData
        # 重新设置数据变化
        self.SetTimeChange(self.m_enumTime, self.m_nCurrentData)

    def LoadConnectMsg(self):
        # < button > 上一个
        self.btnUp.clicked.connect(self.OnBnClickedUp)
        # < button > 下一个
        self.btnDown.clicked.connect(self.OnBnClickedDown)

    def SetTimeChange(self, enumTime, data):
        if enumTime == ENUM_TimeMode.TimeMode_Hour: # 小时制度
            # 区间范围：[0-24)
            # 设置：当前时间
            self.labCurrent.setText(str(data))
            # 设置：上一个时间
            nPreviousData = 23 if data == 0 else (data - 1)
            self.labPrevious.setText(str(nPreviousData))
            # 设置：下一个时间
            nNextData = 0 if data == 23 else (data + 1)
            self.labNext.setText(str(nNextData))
        elif enumTime == ENUM_TimeMode.TimeMode_Minute or enumTime == ENUM_TimeMode.TimeMode_Second:   # 分钟和秒
            # 区间范围：[0-60)
            # 设置：当前时间
            self.labCurrent.setText(str(data))
            # 设置：上一个时间
            nPreviousData = 59 if data == 0 else (data - 1)
            self.labPrevious.setText(str(nPreviousData))
            # 设置：下一个时间
            nNextData = 0 if data == 59 else (data + 1)
            self.labNext.setText(str(nNextData))
        elif enumTime == ENUM_TimeMode.TimeMode_Year:   # 年
            # 区间范围：[1970-2024)
            # 设置：当前时间
            self.labCurrent.setText(str(data))
            # 设置：上一个时间
            nPreviousData = 2024 if data == 1970 else (data - 1)
            self.labPrevious.setText(str(nPreviousData))
            # 设置：下一个时间
            nNextData = 1970 if data == 2024 else (data + 1)
            self.labNext.setText(str(nNextData))
        elif enumTime == ENUM_TimeMode.TimeMode_Month:   # 月
            # 区间范围：[1-12)
            # 设置：当前时间
            self.labCurrent.setText(str(data))
            # 设置：上一个时间
            nPreviousData = 12 if data == 1 else (data - 1)
            self.labPrevious.setText(str(nPreviousData))
            # 设置：下一个时间
            nNextData = 1 if data == 12 else (data + 1)
            self.labNext.setText(str(nNextData))
        elif enumTime == ENUM_TimeMode.TimeMode_Day:   # 月
            # 区间范围：[1-31)
            # 设置：当前时间
            self.labCurrent.setText(str(data))
            # 设置：上一个时间
            nPreviousData = 31 if data == 1 else (data - 1)
            self.labPrevious.setText(str(nPreviousData))
            # 设置：下一个时间
            nNextData = 1 if data == 31 else (data + 1)
            self.labNext.setText(str(nNextData))

            