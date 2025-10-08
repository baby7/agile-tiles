from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor
from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import Signal
from src.my_component.QSelectTimeWidget.single.QSingleSelectTimeWidget import QSingleSelectTimeWidget
from src.my_component.QSelectTimeWidget.single.QSingleSelectTimeWidget import ENUM_TimeMode


class QSelectTimeWidget(QWidget):

    m_widgetHour = None     # 时
    m_widgetMinute = None   # 分
    m_widgetSecond = None   # 秒

    commit_success = Signal(str)
    commit_cancel = Signal(str)

    is_dark = None

    def __init__(self, parent=None, is_dark=False):
        super(QSelectTimeWidget, self).__init__(parent)
        self.is_dark = is_dark
        self.setWindowFlags(Qt.FramelessWindowHint)    # 去掉边框
        self.InitUI()
        self.InitDialogData()
        self.LoadConnectMsg()

    def SetSelectNewCalendarTime(self, qsCurrentTime):
        # 对传入的时间进行分割
        listTime = qsCurrentTime.split(":")
        if len(listTime) < 3:
            return  # 时间格式不对，不处理
        # 设置：小时
        qsHour = listTime[0]
        self.m_widgetHour.SetCurrentShowTime(ENUM_TimeMode.TimeMode_Hour, int(qsHour))
        # 设置：分钟
        qsMinute = listTime[1]
        self.m_widgetMinute.SetCurrentShowTime(ENUM_TimeMode.TimeMode_Minute, int(qsMinute))
        # 设置：秒钟
        qsSecond = listTime[2]
        self.m_widgetSecond.SetCurrentShowTime(ENUM_TimeMode.TimeMode_Second, int(qsSecond))

    def OnBnClickedOK(self):
        # 组装数据进行发送
        nHour = self.m_widgetHour.GetCurrentContent()
        nMinute = self.m_widgetMinute.GetCurrentContent()
        nSecond = self.m_widgetSecond.GetCurrentContent()
        qsGroup = str(nHour).zfill(2) + ":" + str(nMinute).zfill(2) + ":" + str(nSecond).zfill(2)
        self.commit_success.emit(qsGroup)

    def OnBnClickedCanel(self):
        self.commit_cancel.emit("")

    def InitUI(self):
        qsBtnStyle = """
        QPushButton {
            border-radius: 10px;
            border: 1px solid black;
            background-color: rgb(255, 255, 255);
        }
        QPushButton:hover {
            background: rgba(0, 0, 0, 0.3);
            border: none;
        }"""
        # <label>分割线
        qsLineStyle = "QLabel{color:rgba(255, 255, 255, 125);background-color: rgba(255, 255, 255, 125);}"
        self.labLine = QtWidgets.QLabel(self)
        self.labLine.setGeometry(0, 240, 220, 2)
        self.labLine.setText("")
        self.labLine.setStyleSheet(qsLineStyle)
        # <button>确定
        font = QtGui.QFont()
        font.setPointSize(11)
        self.btnOK = QtWidgets.QPushButton(self)
        self.btnOK.setGeometry(120, 255, 80, 30)
        self.btnOK.setStyleSheet(qsBtnStyle)
        self.btnOK.setFont(font)
        self.btnOK.setText("确定")
        # <button>取消
        self.btnCancel = QtWidgets.QPushButton(self)
        self.btnCancel.setGeometry(20, 255, 80, 30)
        self.btnCancel.setStyleSheet(qsBtnStyle)
        self.btnCancel.setFont(font)
        self.btnCancel.setText("取消")
        # 背景
        self.setStyleSheet("background: transparent;")

    def InitDialogData(self):
        #  < widget > 时
        if self.m_widgetHour is not None:
            self.m_widgetHour.clear()
            self.m_widgetHour = None
        self.m_widgetHour = QSingleSelectTimeWidget(self)
        self.m_widgetHour.setGeometry(20, 30, 60, 200)
        self.m_widgetHour.refresh_theme(self.is_dark)
        self.m_widgetHour.show()
        #  < widget > 分
        if self.m_widgetMinute is not None:
            self.m_widgetMinute.clear()
            self.m_widgetMinute = None
        self.m_widgetMinute = QSingleSelectTimeWidget(self)
        self.m_widgetMinute.setGeometry(80, 30, 60, 200)
        self.m_widgetMinute.refresh_theme(self.is_dark)
        self.m_widgetMinute.show()
        #  < widget > 秒
        if self.m_widgetSecond is not None:
            self.m_widgetSecond.clear()
            self.m_widgetSecond = None
        self.m_widgetSecond = QSingleSelectTimeWidget(self)
        self.m_widgetSecond.setGeometry(140, 30, 60, 200)
        self.m_widgetSecond.refresh_theme(self.is_dark)
        self.m_widgetSecond.show()

    def LoadConnectMsg(self):
        # < button > 确定
        self.btnOK.clicked.connect(self.OnBnClickedOK)
        # < button > 取消
        self.btnCancel.clicked.connect(self.OnBnClickedCanel)

    def refresh_theme(self, is_dark):
        self.m_widgetHour.refresh_theme(is_dark)
        self.m_widgetMinute.refresh_theme(is_dark)
        self.m_widgetSecond.refresh_theme(is_dark)
