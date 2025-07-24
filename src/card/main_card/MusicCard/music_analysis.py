import os

from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize

from mutagen import File
from mutagen.flac import FLAC

from src.ui import image_util


def get_music_info(song_path, cover_label):
    song_title, artist, cover_pixmap = None, None, None
    try:
        audio = File(song_path)
        # 最终手段：提取文件名作为歌曲标题
        supported_formats = (".mp3", ".wav", ".ogg", ".flac")
        song_title = os.path.basename(song_path)
        for supported_format in supported_formats:
            song_title = song_title.replace(supported_format, '')
        # 从标签中获取歌曲标题和歌手
        song_title_tags = ["title", "TIT2"]
        for tag in song_title_tags:
            if tag in audio.tags:
                song_title = audio.tags[tag][0]
                break
        artist_tags = ["artist", "TPE1"]
        for tag in artist_tags:
            if tag in audio.tags:
                artist = audio.tags[tag][0]
                break

        # 优化封面获取逻辑
        max_size = 0

        # 遍历所有APIC标签寻找最佳封面
        for key in audio.tags.keys():
            if key.startswith("APIC"):
                apic = audio.tags[key]
                # 优先选择封面类型为3（Front Cover）且分辨率最大的
                if apic.type == 3 and len(apic.data) > max_size:
                    cover_pixmap = apic.data
                    max_size = len(apic.data)
        audio.clear()
        del audio

        # 对于flac格式，尝试获取封面
        if not cover_pixmap and song_path.endswith(".flac"):
            flac_audio = FLAC(song_path)
            if flac_audio is not None and len(flac_audio.pictures) > 0:
                cover_pixmap = flac_audio.pictures[0].data

        # 如果没有找到封面，使用后备图片
        if not cover_pixmap:
            return song_title, artist, cover_pixmap

        # 高质量加载和缩放封面
        pixmap = QPixmap()
        pixmap.loadFromData(cover_pixmap)

        # 处理为圆角
        pixmap = image_util.create_rounded_pixmap(pixmap, 0.06)

        # 根据设备像素比例优化显示
        device_pixel_ratio = cover_label.devicePixelRatio()
        target_size = QSize(270, 270) * device_pixel_ratio

        # 保持原始宽高比的高质量缩放
        scaled_pixmap = pixmap.scaled(
            target_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        # 设置设备像素比例保证高清显示
        scaled_pixmap.setDevicePixelRatio(device_pixel_ratio)
        cover_pixmap = scaled_pixmap

        return song_title, artist, cover_pixmap
    except Exception as e:
        print(f"Error updating song info: {e}")
    return song_title, artist, cover_pixmap