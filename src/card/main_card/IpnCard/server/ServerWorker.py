import select
from PySide6.QtCore import Signal, QObject


class ServerWorker(QObject):
    """服务器工作器"""
    error_occurred = Signal(str)
    server_started = Signal()
    server_stopped = Signal()
    data_updated = Signal()  # 新增：数据更新信号

    def __init__(self, server):
        super().__init__()
        self.server = server
        self._active = False
        self._stop_requested = False

    def start_server(self):
        """启动服务器"""
        try:
            self._active = True
            self._stop_requested = False
            self.server.timeout = 1.0    # 设置合理的超时时间
            self.server_started.emit()

            # 使用非阻塞方式运行服务器
            while self._active and not self._stop_requested:
                try:
                    # 使用select检查是否有连接请求
                    readable, _, _ = select.select([self.server.socket], [], [], 0.5)
                    if readable:
                        # 有连接请求，处理它
                        self.server.handle_request()
                    # 没有请求时，继续循环检查停止标志
                except Exception as e:
                    if self._active:  # 只在服务器应运行时报告错误
                        self.error_occurred.emit(f"服务器错误: {e}")

        except Exception as e:
            self.error_occurred.emit(f"服务器错误: {e}")
        finally:
            self._active = False
            # 确保服务器socket关闭
            if hasattr(self.server, 'socket'):
                try:
                    self.server.socket.close()
                except:
                    pass
            self.server_stopped.emit()

    def stop_server(self):
        """停止服务器"""
        self._stop_requested = True
        self._active = False

    def trigger_data_update(self):
        """触发数据更新信号"""
        self.data_updated.emit()