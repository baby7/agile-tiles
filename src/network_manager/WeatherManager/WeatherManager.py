import json
import traceback

from PySide6.QtCore import Signal, Slot, QUrl, QObject
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from src.client import common


class WeatherManager(QObject):

    finished = Signal(str)

    def __init__(self, parent=None, use_parent=None):
        super().__init__(parent)
        self.use_parent = use_parent
        # 天气管理器
        self.weather_manager = QNetworkAccessManager(self)

    def get_weather_forecast(self, location_id):
        """使用QNetworkRequest获取天气"""
        # 创建请求
        url = QUrl(f"{common.BASE_URL}/weather/forecast?locationId=" + str(location_id))
        print("获取天气预报地址:", url)
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.use_parent.token.encode())
        # 发送请求
        self.current_get = self.weather_manager.get(request)
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
                self.finished.emit(json.dumps(result["data"]))
            else:
                print(result)
        except Exception as e:
            traceback.print_exc()
        self.current_get = None

    def handle_error(self, current_get):
        print("上传失败")
