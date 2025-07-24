# -- coding: utf-8 --
import datetime
import traceback
from PySide6.QtCore import QObject, QThread, QTimer, Signal, Slot, QMutexLocker, QMutex


class CardWorker(QObject):
    # 触发器信号
    refresh_trigger = Signal(str)
    stop_requested = Signal()       # 停止信号

    def __init__(self, card, parent=None):
        super().__init__(parent)
        self.card = card
        self.timer = None
        self.mutex = QMutex()
        self._active = True
        # 连接停止信号到实际停止方法
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
        """启动定时器并执行初始刷新"""
        # 初始刷新
        try:
            datetime_now = datetime.datetime.now()
            self.card.refresh_data(str(datetime_now.strftime("%Y-%m-%d %H:%M:%S")))
            self.refresh_trigger.emit(self.card.uuid)
        except Exception as e:
            print(f"CardWorker initial refresh error: {str(e)}")
            traceback.print_exc()

        # 设置每分钟触发一次（60000毫秒）
        self.timer = QTimer()
        self.timer.timeout.connect(self.execute_refresh)
        self.timer.start(60000)

    @Slot()
    def execute_refresh(self):
        """执行定时刷新任务"""
        if not self.active:
            return
        try:
            datetime_now = datetime.datetime.now()
            if self.card and self.card.uuid:
                self.card.refresh_data(str(datetime_now.strftime("%Y-%m-%d %H:%M:%S")))
                self.refresh_trigger.emit(self.card.uuid)
        except Exception as e:
            print(f"CardWorker refresh error: {str(e)}")
            traceback.print_exc()

    @Slot()
    def stop(self):
        """停止定时器"""
        self.timer.stop()


class CardThread(QObject):
    """卡片线程管理器（非线程本身）"""
    refresh_trigger = Signal(str)

    def __init__(self, parent=None, card=None):
        super().__init__(parent)
        self.card = card
        # 创建线程和工作对象
        self.thread = QThread()
        self.worker = CardWorker(self.card)
        # 将worker移至新线程
        self.worker.moveToThread(self.thread)
        # 连接信号
        self.worker.refresh_trigger.connect(self.refresh_trigger)
        # 设置线程启动时启动定时器
        self.thread.started.connect(self.worker.start_timer)

    def start(self):
        """启动卡片工作线程"""
        if not self.thread.isRunning():
            self.thread.start()

    def is_running(self):
        return self.thread.isRunning()

    def stop(self):
        """停止卡片工作线程"""
        # 通过信号安全停止worker
        self.worker.stop_requested.emit()
        # 退出线程并等待
        self.thread.quit()
        self.thread.wait(2000)
        if self.thread.isRunning():
            self.thread.terminate()
        print(f"卡片线程:{self.card.uuid if self.card else 'unknown'}退出")
