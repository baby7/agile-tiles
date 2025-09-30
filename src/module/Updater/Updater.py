import os
import json
import shutil
import traceback
from PySide6.QtCore import QObject, Signal, QSaveFile, QIODevice
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply


class Updater(QObject):
    progress = Signal(int)  # 下载进度信号
    finished = Signal(bool, dict)  # 完成信号(是否成功, 更新信息)
    message = Signal(str)  # 消息信号

    def __init__(self, api_url, app_version, update_dir):
        super().__init__()
        self.api_url = api_url + "&version=" + str(app_version)
        self.app_version = app_version
        self.downloaded_file_path = None
        self.update_dir = update_dir
        self.network_manager = QNetworkAccessManager(self)
        self.current_reply = None
        self.download_file = None

    def check_update(self):
        """检查更新"""
        try:
            request = QNetworkRequest(self.api_url)
            self.current_reply = self.network_manager.get(request)
            self.current_reply.finished.connect(self._handle_update_response)
        except Exception as e:
            self.message.emit(f"更新检查失败: {str(e)}")
            self.finished.emit(False, {})
            traceback.print_exc()

    def download_package(self, update_info):
        """下载更新包"""
        try:
            is_exe_tag = False
            # 根据updateTag决定下载内容
            if update_info.get("updateTag"):
                # 大版本更新，下载完整安装包
                download_url = update_info["url"]
            else:
                if "exeUrl" in update_info and update_info["exeUrl"] is not None and update_info["exeUrl"] != "":
                    # 小版本更新，只下载exe文件
                    download_url = update_info["exeUrl"]
                    is_exe_tag = True
                else:
                    # 没有小版本更新文件则默认下载完整安装包
                    download_url = update_info["url"]
            # 创建临时目录
            temp_dir = self.update_dir
            # 清理临时目录（如果存在）
            if os.path.exists(temp_dir):
                for filename in os.listdir(temp_dir):
                    file_path = os.path.join(temp_dir, filename)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print(f"清理文件失败: {file_path}, 错误: {e}")

            # 确保目录存在
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            # 提取文件名
            file_name = os.path.basename(download_url)
            # 如果是zip更新，确保文件名固定为AgileTiles.zip
            if is_exe_tag:
                file_name = "AgileTiles.zip"

            download_path = os.path.join(temp_dir, file_name)

            # 创建文件
            self.download_file = QSaveFile(download_path)
            if not self.download_file.open(QIODevice.WriteOnly):
                raise Exception(f"无法创建文件: {download_path}")

            # 发送请求
            request = QNetworkRequest(download_url)
            self.current_reply = self.network_manager.get(request)

            # 连接信号
            self.current_reply.readyRead.connect(self._handle_download_data)
            self.current_reply.downloadProgress.connect(self._handle_download_progress)
            self.current_reply.finished.connect(self._handle_download_finished)

        except Exception as e:
            self.message.emit(f"下载失败: {str(e)}")
            self.finished.emit(False, {})
            traceback.print_exc()

    def _handle_update_response(self):
        """处理更新检查响应"""
        try:
            if self.current_reply.error() != QNetworkReply.NoError:
                self.message.emit(f"网络错误: {self.current_reply.errorString()}")
                self.finished.emit(False, {})
                return

            data = self.current_reply.readAll()
            update_info = json.loads(data.data().decode('utf-8'))["data"]
            self.finished.emit(True, update_info)
        except Exception as e:
            self.message.emit(f"解析更新信息失败: {str(e)}")
            self.finished.emit(False, {})
            traceback.print_exc()
        finally:
            self.current_reply.deleteLater()
            self.current_reply = None

    def _handle_download_data(self):
        """处理下载数据"""
        if self.download_file and self.current_reply:
            data = self.current_reply.readAll()
            if data:
                self.download_file.write(data)

    def _handle_download_progress(self, bytes_received, bytes_total):
        """处理下载进度"""
        if bytes_total > 0:
            progress = int(bytes_received / bytes_total * 100)
            self.progress.emit(progress)

    def _handle_download_finished(self):
        """处理下载完成"""
        try:
            if self.current_reply.error() != QNetworkReply.NoError:
                self.message.emit(f"下载错误: {self.current_reply.errorString()}")
                self.finished.emit(False, {})
                return

            # 确保所有数据已写入
            self.download_file.commit()
            self.downloaded_file_path = self.download_file.fileName()
            self.finished.emit(True, {})
        except Exception as e:
            self.message.emit(f"保存文件失败: {str(e)}")
            self.finished.emit(False, {})
            traceback.print_exc()
        finally:
            self.current_reply.deleteLater()
            self.current_reply = None
            self.download_file = None