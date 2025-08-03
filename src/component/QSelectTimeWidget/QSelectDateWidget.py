from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor
from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import Signal
from src.component.QSelectTimeWidget.single.QSingleSelectTimeWidget import QSingleSelectTimeWidget
from src.component.QSelectTimeWidget.single.QSingleSelectTimeWidget import ENUM_TimeMode


class QSelectDateWidget(QWidget):

    m_widgetYear = None    # 年
    m_widgetMonth = None   # 月
    m_widgetDay = None     # 日

    commit_success = Signal(str)
    commit_cancel = Signal(str)

    is_dark = None

    def __init__(self, parent=None, is_dark=False):
        super(QSelectDateWidget, self).__init__(parent)
        self.is_dark = is_dark
        self.setWindowFlag(Qt.FramelessWindowHint)    # 去掉边框
        self.InitUI()
        self.InitDialogData()
        self.LoadConnectMsg()

    def SetSelectNewCalendarTime(self, qsCurrentTime):
        # 对传入的时间进行分割
        listTime = qsCurrentTime.split("-")
        if len(listTime) < 3:
            return  # 时间格式不对，不处理
        # 设置：年
        qsYear = listTime[0]
        self.m_widgetYear.SetCurrentShowTime(ENUM_TimeMode.TimeMode_Year, int(qsYear))
        # 设置：月
        qsMonth = listTime[1]
        self.m_widgetMonth.SetCurrentShowTime(ENUM_TimeMode.TimeMode_Month, int(qsMonth))
        # 设置：日
        qsDay = listTime[2]
        self.m_widgetDay.SetCurrentShowTime(ENUM_TimeMode.TimeMode_Day, int(qsDay))

    def OnBnClickedOK(self):
        # 组装数据进行发送
        nYear = self.m_widgetYear.GetCurrentContent()
        nMonth = self.m_widgetMonth.GetCurrentContent()
        nDay = self.m_widgetDay.GetCurrentContent()
        qsGroup = str(nYear).zfill(4) + "-" + str(nMonth).zfill(2) + "-" + str(nDay).zfill(2)
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
        #  < widget > 年
        if self.m_widgetYear is not None:
            self.m_widgetYear.clear()
            self.m_widgetYear = None
        self.m_widgetYear = QSingleSelectTimeWidget(self)
        self.m_widgetYear.setGeometry(20, 30, 60, 200)
        self.m_widgetYear.refresh_theme(self.is_dark)
        self.m_widgetYear.show()
        #  < widget > 月
        if self.m_widgetMonth is not None:
            self.m_widgetMonth.clear()
            self.m_widgetMonth = None
        self.m_widgetMonth = QSingleSelectTimeWidget(self)
        self.m_widgetMonth.setGeometry(80, 30, 60, 200)
        self.m_widgetMonth.refresh_theme(self.is_dark)
        self.m_widgetMonth.show()
        #  < widget > 日
        if self.m_widgetDay is not None:
            self.m_widgetDay.clear()
            self.m_widgetDay = None
        self.m_widgetDay = QSingleSelectTimeWidget(self)
        self.m_widgetDay.setGeometry(140, 30, 60, 200)
        self.m_widgetDay.refresh_theme(self.is_dark)
        self.m_widgetDay.show()

    def LoadConnectMsg(self):
        # < button > 确定
        self.btnOK.clicked.connect(self.OnBnClickedOK)
        # < button > 取消
        self.btnCancel.clicked.connect(self.OnBnClickedCanel)
