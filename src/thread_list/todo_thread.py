# -- coding: utf-8 --
import datetime
from PySide6.QtCore import QObject, QThread, QTimer, Signal, Slot, QMutex, QMutexLocker


class TodoWorker(QObject):
    # 停止请求信号
    stop_requested = Signal()

    def __init__(self, parent=None, use_parent=None, task_list=None):
        super().__init__(parent)
        self.task_list = task_list if task_list is not None else []
        self.mutex = QMutex()
        self.use_parent = use_parent
        self._active = True
        self.last_check_time = None  # 新增：记录上次检查时间
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
            # 如果与上次检查时间相同，则跳过本次执行
            if self.last_check_time == current_time_str:
                return
            # 更新上次检查时间
            self.last_check_time = current_time_str
            with QMutexLocker(self.mutex):
                if not self.task_list:
                    return
                for task in self.task_list:
                    if task['complete'] or not task['remind']:
                        continue
                    if task['remindTime'] == current_time_str:
                        # 发出提醒信号
                        self.use_parent.send_message(title=f'待办事项 - {task["title"]}', descript=task["desc"])
        except Exception as e:
            print(f"TodoWorker error: {str(e)}")

    @Slot()
    def stop(self):
        """停止工作器"""
        self.timer.stop()
        self.active = False


class TodoThread(QObject):
    """待办事项线程管理器"""

    def __init__(self, parent=None, use_parent=None, task_list=None):
        super().__init__(parent)
        self.task_list = task_list
        # 创建线程和工作对象
        self.thread = QThread()
        self.worker = TodoWorker(use_parent=use_parent, task_list=self.task_list)
        # 将worker移至新线程
        self.worker.moveToThread(self.thread)
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
