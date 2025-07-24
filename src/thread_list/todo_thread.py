# -- coding: utf-8 --
import datetime
from PySide6.QtCore import QObject, QThread, QTimer, Signal, Slot, QMutex, QMutexLocker


class TodoWorker(QObject):
    # 提醒信号
    remind_trigger = Signal(str, str)  # (title, time_str)

    # 停止请求信号
    stop_requested = Signal()

    def __init__(self, parent=None, task_list=None):
        super().__init__(parent)
        self.task_list = task_list if task_list is not None else []
        self.mutex = QMutex()
        self._active = True
        # 连接停止信号
        self.stop_requested.connect(self.stop)

    def set_task_list(self, task_list):
        with QMutexLocker(self.mutex):
            self.task_list = task_list

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
        """启动定时检查"""
        self.timer = QTimer()
        self.timer.setInterval(500)  # 0.5秒检查一次
        self.timer.timeout.connect(self.check_tasks)
        self.timer.start()

    @Slot()
    def check_tasks(self):
        """检查任务提醒"""
        if not self.active:
            return
        try:
            datetime_now = datetime.datetime.now()
            current_time_str = datetime_now.strftime("%Y-%m-%d %H:%M:%S")

            with QMutexLocker(self.mutex):
                if not self.task_list:
                    return

                for task in self.task_list:
                    if task['complete'] or not task['remind']:
                        continue
                    if task['remindTime'] == current_time_str:
                        # 发出提醒信号
                        self.remind_trigger.emit(task["title"], current_time_str)
        except Exception as e:
            print(f"TodoWorker error: {str(e)}")

    @Slot()
    def stop(self):
        """停止工作器"""
        self.timer.stop()
        self.active = False


class TodoThread(QObject):
    """待办事项线程管理器"""
    remind_trigger = Signal(str, str)  # 转发提醒信号

    def __init__(self, parent=None, task_list=None):
        super().__init__(parent)
        self.task_list = task_list
        # 创建线程和工作对象
        self.thread = QThread()
        self.worker = TodoWorker(task_list=self.task_list)
        # 将worker移至新线程
        self.worker.moveToThread(self.thread)
        # 连接信号
        self.worker.remind_trigger.connect(self.remind_trigger)
        # 设置线程启动时启动定时器
        self.thread.started.connect(self.worker.start_timer)

    def set_task_list(self, task_list):
        """设置任务列表"""
        if self.worker:
            self.worker.set_task_list(task_list)
        else:
            self.task_list = task_list

    def start(self):
        """启动待办事项线程"""
        if not self.thread.isRunning():
            self.thread.start()

    def is_running(self):
        return self.thread.isRunning()

    def stop(self):
        """停止待办事项线程"""
        # 安全停止定时器
        self.worker.stop_requested.emit()
        # 退出线程并等待
        self.thread.quit()
        self.thread.wait(2000)  # 最多等待2秒
        if self.thread.isRunning():
            self.thread.terminate()
        print("Todo线程已退出")
