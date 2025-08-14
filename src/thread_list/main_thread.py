# -- coding: utf-8 --
import datetime
import traceback
from PySide6.QtCore import QObject, QThread, QTimer, Signal, QMutex, QMutexLocker, Slot


class MainWorker(QObject):
    """主线程工作器（处理实际任务）"""
    time_task_trigger = Signal(str)
    stop_requested = Signal()  # 新增停止信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_datetime = datetime.datetime.now()
        self.timer = None
        self.mutex = QMutex()
        self._active = True
        # 连接停止信号
        self.stop_requested.connect(self.stop)  # 新增连接

    @property
    def active(self):
        with QMutexLocker(self.mutex):
            return self._active

    @active.setter
    def active(self, value):
        with QMutexLocker(self.mutex):
            self._active = value

    @Slot()
    def start_timer(self):
        """启动定时器"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_time)
        self.timer.start(1000)  # 每秒检查一次

    @Slot()
    def check_time(self):
        """定时检查时间并触发任务"""
        if not self.active:
            return
        try:
            datetime_now = datetime.datetime.now()
            if datetime_now - self.start_datetime >= datetime.timedelta(seconds=30):
                self.time_task_trigger.emit(datetime_now.strftime("%H:%M:%S"))
                self.start_datetime = datetime_now
        except Exception as e:
            print(f"MainWorker error: {str(e)}")
            traceback.print_exc()

    @Slot()
    def stop(self):
        """停止工作器"""
        self.timer.stop()
        self.active = False


class MainThread(QObject):
    """主线程管理器（管理线程生命周期）"""
    time_task_trigger = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.thread = QThread()
        self.worker = MainWorker()
        # 将worker移至新线程
        self.worker.moveToThread(self.thread)
        # 连接信号
        self.worker.time_task_trigger.connect(self.time_task_trigger)
        # 设置线程启动时启动定时器
        self.thread.started.connect(self.worker.start_timer)

    def start(self):
        """启动主工作线程"""
        if not self.thread.isRunning():
            self.thread.start()

    def is_running(self):
        return self.thread.isRunning()

    def stop(self):
        """停止主工作线程"""
        # 通过信号安全停止worker
        self.worker.stop_requested.emit()
        # 退出线程并等待
        self.thread.quit()
        self.thread.wait(2000)
        if self.thread.isRunning():
            self.thread.terminate()
        print("主线程已退出")
