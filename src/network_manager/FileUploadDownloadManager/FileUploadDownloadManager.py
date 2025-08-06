import os
import json
import mimetypes
from PySide6.QtCore import Signal, Slot, QUrl, QFile, QObject
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply, QHttpMultiPart, QHttpPart

from src.client import common


class FileUploadDownloadManager(QObject):

    upload_finished = Signal(str)
    download_finished = Signal(str)
    # download_finished = Signal(str)
    current_upload_file_path = None
    current_download_url = None

    def __init__(self, parent=None, use_parent=None):
        super().__init__(parent)
        self.use_parent = use_parent
        # 下载和上传管理器
        self.upload_manager = QNetworkAccessManager(self)
        self.download_manager = QNetworkAccessManager(self)

    def upload_file(self, file_path=None, file_source=None):
        """使用QNetworkRequest上传文件"""
        # 获取文件类型
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = 'application/octet-stream'
        # 准备文件
        file_name = os.path.basename(file_path)
        file = QFile(file_path)
        if not file.open(QFile.ReadOnly):
            return False
        # 保存当前上传文件路径
        self.current_upload_file_path = file_path
        # 创建多部分请求
        multi_part = QHttpMultiPart(QHttpMultiPart.FormDataType)
        # 添加文件部分
        file_part = QHttpPart()
        file_part.setHeader(QNetworkRequest.ContentTypeHeader, mime_type)
        file_part.setHeader(QNetworkRequest.ContentDispositionHeader, f'form-data; name="file"; filename="{file_name}"')
        file_part.setBodyDevice(file)
        file.setParent(multi_part)  # 确保文件在multi_part销毁时关闭
        multi_part.append(file_part)
        # 创建请求
        url = QUrl(f"{common.BASE_URL}/file/normal/{file_source}/save")
        print("上传文件地址:", url)
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.use_parent.access_token.encode())
        # 发送请求
        self.current_upload = self.upload_manager.post(request, multi_part)
        multi_part.setParent(self.current_upload)  # 确保multi_part在请求完成后被删除
        # 连接完成信号
        self.current_upload.finished.connect(lambda : self.handle_upload_finished(self.current_upload))
        self.current_upload.errorOccurred.connect(lambda : self.handle_upload_error(self.current_upload))

    @Slot(QNetworkReply)
    def handle_upload_finished(self, reply):
        """处理上传完成"""
        try:
            # 检查是否有错误
            if reply.error() != QNetworkReply.NoError:
                return
            # 解析响应
            response_data = reply.readAll().data()
            result = json.loads(response_data.decode('utf-8'))
            if str(result.get('code')) == "0":
                real_url = result["data"]["url"]
                self.upload_finished.emit(real_url)
            else:
                print(result)
        except Exception as e:
            print(e)
        self.current_upload = None
        self.current_upload_file_path = None

    def handle_upload_error(self, current_upload):
        print("上传失败")

    def get_file_url(self, file_url=None, file_source=None):
        """使用QNetworkRequest获取文件链接"""
        if file_url is None:
            return False
        # 保存当前下载文件路径
        self.current_download_url = file_url
        # 创建请求
        url = QUrl(f"{common.BASE_URL}/file/normal/{file_source}/realtime?url=" + str(file_url))
        print("获取文件地址:", url)
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.use_parent.access_token.encode())
        # 发送请求
        self.current_download = self.download_manager.get(request)
        # 连接完成信号
        self.current_download.finished.connect(lambda : self.handle_download_finished(self.current_download))
        self.current_download.errorOccurred.connect(lambda : self.handle_download_error(self.current_download))

    @Slot(QNetworkReply)
    def handle_download_finished(self, reply):
        """处理下载完成"""
        try:
            # 检查是否有错误
            if reply.error() != QNetworkReply.NoError:
                return
            # 解析响应
            response_data = reply.readAll().data()
            result = json.loads(response_data.decode('utf-8'))
            if str(result.get('code')) == "0":
                real_url = result["data"]
                self.download_finished.emit(real_url)
            else:
                print(result)
        except Exception as e:
            print(e)
        self.current_download = None
        self.current_download_url = None

    def handle_download_error(self, current_download):
        print("下载失败")
