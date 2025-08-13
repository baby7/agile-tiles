# -*- coding: utf-8 -*-
import json

from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

import src.client.common as common


class CardStoreClient(QObject):
    # 定义信号，用于异步返回结果
    card_list_received = Signal(list)
    version_image_received = Signal(dict)
    request_error = Signal(str)
    main_object = None

    def __init__(self, main_object):
        super().__init__()
        self.main_object = main_object
        self.network_manager = QNetworkAccessManager(self)

    def fetch_card_store_list(self):
        """异步获取卡片商店列表"""
        url = common.BASE_URL + "/cardStore/normal"
        request = QNetworkRequest(QUrl(url))
        request.setRawHeader(b"Authorization", bytes(self.main_object.access_token, "utf-8"))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")

        reply = self.network_manager.get(request)
        reply.finished.connect(lambda: self._handle_card_list_reply(reply))

    def _handle_card_list_reply(self, reply):
        """处理卡片商店列表的响应"""
        try:
            if reply.error() == QNetworkReply.NoError:
                data = reply.readAll().data().decode()
                result = json.loads(data)
                if result['code'] == 0:
                    self.card_list_received.emit(result.get('data', []))
                else:
                    self.request_error.emit(f"Error code {result['code']}: {result.get('message', 'Unknown error')}")
            else:
                self.request_error.emit(reply.errorString())
        except Exception as e:
            self.request_error.emit(f"处理数据失败: {str(e)}")
        finally:
            reply.deleteLater()

    def fetch_store_version_image(self, card_name, card_size):
        """异步获取卡片版本图片"""
        url = common.BASE_URL + "/cardStore/normal/versionImage"
        request = QNetworkRequest(QUrl(url))
        request.setRawHeader(b"Authorization", bytes(self.main_object.access_token, "utf-8"))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")

        # 构造POST数据
        post_data = json.dumps({'name': card_name, 'cardSize': card_size}).encode('utf-8')
        reply = self.network_manager.post(request, post_data)
        reply.finished.connect(lambda: self._handle_version_image_reply(reply))

    def _handle_version_image_reply(self, reply):
        """处理版本图片的响应"""
        try:
            if reply.error() == QNetworkReply.NoError:
                data = reply.readAll().data().decode()
                result = json.loads(data)
                if result['code'] == 0:
                    self.version_image_received.emit(result.get('data', {}))
                else:
                    self.request_error.emit(f"Error code {result['code']}: {result.get('message', 'Unknown error')}")
            else:
                self.request_error.emit(reply.errorString())
        except Exception as e:
            self.request_error.emit(f"处理数据失败: {str(e)}")
        finally:
            reply.deleteLater()