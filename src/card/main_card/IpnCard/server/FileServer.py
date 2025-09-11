from http.server import HTTPServer


class FileServer(HTTPServer):
    """自定义HTTP服务器"""

    def __init__(self, server_address, handler_class, file_data, upload_dir, update_callback=None):
        super().__init__(server_address, handler_class)
        self.file_data = file_data
        self.upload_dir = upload_dir
        self.update_callback = update_callback  # 新增：数据更新回调函数
        # 设置handler类的base_path属性
        handler_class.base_path = ""
