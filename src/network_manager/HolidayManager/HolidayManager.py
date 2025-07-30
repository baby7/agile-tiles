import json

from PySide6.QtCore import Signal, Slot, QUrl, QObject
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from src.client import common


class HolidayManager(QObject):

    finished = Signal(str)

    def __init__(self, parent=None, use_parent=None):
        super().__init__(parent)
        self.use_parent = use_parent
        # 节假日管理器
        self.holiday_manager = QNetworkAccessManager(self)

    def get_holiday(self, date_list_str):
        """使用QNetworkRequest获取节假日"""
        # 创建请求
        url = QUrl(f"{common.BASE_URL}/holiday/normal?d=" + date_list_str + "&type=Y")
        print("获取节假日地址:", url)
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.use_parent.access_token.encode())
        # 发送请求
        self.current_get = self.holiday_manager.get(request)
        # 连接完成信号
        self.current_get.finished.connect(lambda : self.handle_finished(self.current_get))
        self.current_get.errorOccurred.connect(lambda : self.handle_error(self.current_get))

    @Slot(QNetworkReply)
    def handle_finished(self, reply):
        """处理上传完成"""
        try:
            # 检查是否有错误
            if reply.error() != QNetworkReply.NoError:
                return
            # 解析响应
            response_data = reply.readAll().data()
            result = json.loads(response_data.decode('utf-8'))
            if str(result.get('code')) == "0":
                print(f"获取到节假日信息:{result['data']}")
                self.finished.emit(json.dumps(result["data"]))
            else:
                print(result)
        except Exception as e:
            print(e)
        self.current_get = None

    def handle_error(self, current_get):
        print("上传失败")
