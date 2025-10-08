import os
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QDir


class ImageCacheManager:
    def __init__(self, image_path=None):
        self.cache = {}  # 图片缓存字典 {image_name: QPixmap}
        self.base_dir = image_path  # 图片基础目录

    def get_pixmap(self, image_name):
        """
        获取图片的QPixmap对象
        :param image_name: 图片名称（可包含相对路径）
        :return: QPixmap对象或None
        """
        # 检查缓存
        if image_name in self.cache:
            return self.cache[image_name]

        # 构建完整路径
        full_path = os.path.join(self.base_dir, image_name)

        # 检查文件是否存在
        if not os.path.exists(full_path):
            print(f"Image not found: {full_path}")
            return None

        # 加载图片
        pixmap = QPixmap()
        if not pixmap.load(full_path):
            print(f"Failed to load image: {full_path}")
            return None

        # 存入缓存
        self.cache[image_name] = pixmap
        return pixmap

    def save_pixmap(self, image_name, pixmap, format="PNG"):
        """
        保存图片到缓存和文件系统
        :param image_name: 图片名称（可包含相对路径）
        :param pixmap: 要保存的QPixmap对象
        :param format: 图片格式（如PNG, JPG等）
        """
        if pixmap.isNull():
            print("Cannot save null pixmap")
            return False

        # 更新缓存
        self.cache[image_name] = pixmap

        # 构建完整路径
        full_path = os.path.join(self.base_dir, image_name)
        dir_path = os.path.dirname(full_path)

        # 确保目录存在
        if not QDir().mkpath(dir_path):
            print(f"Failed to create directory: {dir_path}")
            return False

        # 保存到文件系统
        success = pixmap.save(full_path, format)
        if not success:
            print(f"Failed to save image: {full_path}")
        return success

    def get_pixmap_by_url(self, url):
        """
        根据url获取图片的QPixmap对象
        :param url: 网络名称
        :return: QPixmap对象或None
        """
        if url is None or not url.startswith("http"):
            return None
        image_name = os.path.basename(url)
        return self.get_pixmap(image_name)

    def save_pixmap_by_url(self, url, pixmap):
        """
        根据url保存图片到缓存和文件系统
        :param url: 网络名称
        :param pixmap: 要保存的QPixmap对象
        """
        if not url.startswith("http"):
            return False
        image_name = os.path.basename(url)
        _, ext = os.path.splitext(image_name)
        format = ext[1:].upper() if ext else "PNG"
        return self.save_pixmap(image_name, pixmap, format)

    def clear_cache(self):
        """清空图片缓存"""
        self.cache.clear()

    def set_base_dir(self, path):
        """设置图片基础目录"""
        self.base_dir = path
