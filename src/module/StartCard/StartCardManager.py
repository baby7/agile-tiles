import json
import os
import traceback
import zipfile
import tempfile
import shutil
import re
from src.util import my_shiboken_util
from urllib.parse import urlparse

from PySide6.QtCore import QObject, Signal, QUrl
from PySide6.QtNetwork import QNetworkRequest, QNetworkReply, QNetworkAccessManager

from src.client import common
from src.module.StartCard.start_analysis import analyze_card_list
from src.module.StartCard.start_file_utils import scan_local_cards


class CardManager(QObject):
    download_complete = Signal()
    cloud_ready = False
    local_ready = False
    card_list_reply = None
    download_reply_list = []

    def __init__(self, main_object):
        super().__init__()
        self.local_card_thread = None
        self.main_object = main_object
        self.nam = QNetworkAccessManager()  # 直接使用QNetworkAccessManager
        self.user_card_list = []
        self.cloud_card_list = {}
        self.local_card_list = {}
        self.download_list = []
        self.delete_list = []
        self.current_downloads = {}  # 跟踪当前下载任务: {reply: card_name}

        # 连接信号
        self.download_complete.connect(self.handle_download_complete)

    def check_card_on_start(self):
        # 直接从主对象获取用户卡片列表
        self.user_card_list = [card["name"] for card in self.main_object.main_data["card"]]
        # 异步获取云端卡片列表
        self.get_cloud_card_list()
        # 同步获取本地卡片列表
        self.get_local_card_list_sync()

    def get_cloud_card_list(self):
        url = common.BASE_URL + "/cardStore/public/simple?clientVersion=" + self.main_object.app_version
        request = QNetworkRequest(QUrl(url))
        request.setRawHeader(b"Authorization", self.main_object.access_token.encode())
        self.card_list_reply = self.nam.get(request)
        self.card_list_reply.finished.connect(self.handle_cloud_reply)

    def get_local_card_list_sync(self):
        """同步获取本地卡片列表"""
        try:
            local_data = scan_local_cards(self.main_object)  # 直接调用同步扫描函数
            self.handle_local_data(local_data)
        except Exception as e:
            print(f"Error getting local card list: {traceback.format_exc()}")
            self.handle_local_data({})

    def handle_cloud_reply(self):
        if self.card_list_reply.error() != QNetworkReply.NoError:
            print(f"Cloud data error: {self.card_list_reply.errorString()}")
            # 在执行删除操作前，检查C++对象是否存活
            if self.card_list_reply is not None and my_shiboken_util.is_qobject_valid(self.card_list_reply):
                self.card_list_reply.deleteLater()
            self.card_list_reply = None
            return
        try:
            data = self.card_list_reply.readAll().data().decode()
            result = json.loads(data)
            # 确保返回的数据结构正确
            if "data" in result:
                result_data = result["data"]
                self.handle_cloud_data(result_data)
            else:
                print(f"Invalid cloud data structure: {data}")
        except Exception as e:
            print(f"Error parsing cloud data: {traceback.format_exc()}")
        # 在执行删除操作前，检查C++对象是否存活
        if self.card_list_reply is not None and my_shiboken_util.is_qobject_valid(self.card_list_reply):
            self.card_list_reply.deleteLater()
        self.card_list_reply = None

    def handle_cloud_data(self, data):
        # 确保数据是列表
        if not isinstance(data, list):
            print(f"Invalid cloud card list format: {type(data)}")
            return

        # 转换为字典: {card_name: card_data}
        try:
            self.cloud_card_list = {item["name"]: item for item in data}
            print(f"Received cloud card list with {len(data)} items")
            self.cloud_ready = True
            self.try_analyze()
        except KeyError as e:
            print(f"Missing key in cloud card data: {traceback.format_exc()}")

    def handle_local_data(self, data):
        if not isinstance(data, dict):
            print(f"Invalid local card list format: {type(data)}")
            return
        self.local_card_list = data
        print(f"Received local card list with {len(data)} items")
        self.local_ready = True
        self.try_analyze()

    def try_analyze(self):
        # 确保云端和本地数据都已准备好
        if not self.cloud_ready or not self.local_ready:
            return
        self.delete_list, self.download_list = analyze_card_list(
            self.user_card_list,
            self.cloud_card_list,
            self.local_card_list
        )
        print(f"Analysis result: {len(self.download_list)} to download, {len(self.delete_list)} to delete")
        self.download_card_list()

    def download_card_list(self):
        if not self.download_list:
            print("No cards to download")
            self.download_complete.emit()
            return
        print(f"Starting download of {len(self.download_list)} cards")
        # 添加下载任务
        for card_name in self.download_list:
            card_data = self.cloud_card_list[card_name]
            url = card_data["currentVersion"]["url"]
            self.download_card(url, card_name)

    def download_card(self, url, card_name):
        request = QNetworkRequest(QUrl(url))
        reply = self.nam.get(request)
        self.current_downloads[reply] = card_name
        reply.finished.connect(lambda : self.handle_download_reply(reply))
        self.download_reply_list.append(reply)

    def handle_download_reply(self, reply):
        card_name = self.current_downloads.pop(reply, None)
        if reply.error() != QNetworkReply.NoError:
            print(f"Download failed for {card_name}: {reply.errorString()}")
            # 在执行删除操作前，检查C++对象是否存活
            if reply is not None and my_shiboken_util.is_qobject_valid(reply):
                reply.deleteLater()
            return
        try:
            # 获取下载内容
            content = reply.readAll().data()
            # 获取下载URL
            url = reply.url().toString()
            # 保存和解压缩卡片
            extracted_path = save_and_extract(content, url, use_parent=self.main_object)
            print(f"Downloaded card: {card_name} to {extracted_path}")
            # 从下载列表中移除
            if card_name in self.download_list:
                self.download_list.remove(card_name)
            # 检查是否所有下载完成
            if not self.download_list:
                self.download_complete.emit()
        except Exception as e:
            print(f"Error processing downloaded card {card_name}: {traceback.format_exc()}")
        # 清理该回复对象
        if reply is not None and my_shiboken_util.is_qobject_valid(reply):
            reply.deleteLater()
        # 从待处理列表中移除
        if reply in self.download_reply_list:
            self.download_reply_list.remove(reply)

    def handle_download_complete(self):
        print("All downloads completed")
        self.main_object.card_ready.emit()

def save_and_extract(content, download_url, use_parent=None):
    """
    保存并解压卡片内容，使用下载地址中的文件名作为文件夹名称
    """
    # 从URL中提取文件名（最后一个'/'之后的部分）
    parsed_url = urlparse(download_url)
    filename = os.path.basename(parsed_url.path)
    # 移除可能的查询参数
    if '?' in filename:
        filename = filename.split('?')[0]
    # 移除.zip后缀（如果存在）
    base_name = re.sub(r'\.zip$', '', filename, flags=re.IGNORECASE)
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    try:
        # 保存下载内容到临时文件
        zip_path = os.path.join(temp_dir, f"{filename}")
        with open(zip_path, 'wb') as f:
            f.write(content)
        # 目标目录 (./plugin/base_name)
        plugin_path = use_parent.app_data_plugin_path
        card_dir = os.path.join(plugin_path, base_name)
        # 确保目录存在
        os.makedirs(card_dir, exist_ok=True)
        # 解压zip文件
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(card_dir)
        print(f"成功解压卡片到: {card_dir}")
        # 返回实际解压路径
        return str(card_dir)
    except Exception as e:
        print(f"解压卡片失败: {traceback.format_exc()}")
        # 清理临时文件
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise
    finally:
        # 清理临时文件
        shutil.rmtree(temp_dir, ignore_errors=True)