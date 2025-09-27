import base64
import urllib
import uuid
from typing import Union

from PIL import Image, ImageDraw
from PySide6 import QtGui, QtCore
from PySide6.QtCore import QByteArray, Qt, QPoint, QRectF, QBuffer
from PySide6.QtGui import QPainter, QPixmap, QColor, QImage, QRegion, QPainterPath
from PySide6.QtSvg import QSvgRenderer
from io import BytesIO

from PySide6.QtWidgets import QWidget


def load_light_svg(file_path):
    with open(file_path, 'r') as file:
        svg_str = file.read()
    return modify_svg(svg_str, ["#2F88FF"], 0, scale_factor=2.0, is_dark=False)


def load_dark_svg(file_path):
    with open(file_path, 'r') as file:
        svg_str = file.read()
    return modify_svg(svg_str, ["#2F88FF"], 0, scale_factor=2.0, is_dark=True)


def modify_svg(svg_str: str, target_color_list, alpha: int = 127, scale_factor: float = 1.0, is_dark=False) -> QPixmap:
    modified_svg = svg_str
    for target_color in target_color_list:
        modified_color = f"rgba({int(target_color[1:3], 16)}, {int(target_color[3:5], 16)}, {int(target_color[5:7], 16)}, {alpha})"
        modified_svg = modified_svg.replace(target_color, modified_color)
    modified_svg = modified_svg.replace("black", "white") if not is_dark else modified_svg.replace("white", "black")

    renderer = QSvgRenderer(QByteArray(modified_svg.encode('utf-8')))
    pixmap_size = renderer.defaultSize() * scale_factor
    pixmap = QPixmap(pixmap_size)
    pixmap.fill(QColor(0, 0, 0, 0))
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return pixmap


def from_file_to_image(path, radius):
    # 直接打开图片文件
    image = Image.open(path)
    # 处理圆角
    rounded_image = round_corners_image(image, radius)
    # 转换到QPixmap
    output_buffer = BytesIO()
    rounded_image.save(output_buffer, format="PNG")
    result_img = QtGui.QPixmap()
    result_img.loadFromData(output_buffer.getvalue())
    return result_img


def round_corners_image(image, radius):
    """处理图片圆角并返回内存中的图像对象"""
    image = image.convert("RGBA")
    mask = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(mask)
    # 计算圆角半径
    radius_value = int(((image.width + image.height) / 2) * radius)
    draw.rounded_rectangle((0, 0, image.width, image.height), radius_value, fill=(255, 255, 255, 255))
    # 合成图像
    result = Image.new("RGBA", image.size)
    result.paste(image, mask=mask)
    return result


def create_rounded_pixmap(pixmap: QPixmap, radius: Union[int, float]) -> QPixmap:
    """创建带圆角的 QPixmap，支持百分比圆角参数

    Args:
        pixmap: 原始图像
        radius: 圆角值，支持两种模式：
                - 整数：绝对像素值
                - 0~1的浮点数：相对于图片尺寸的百分比
    """
    if pixmap.isNull():
        return pixmap

    # 获取设备像素比
    device_pixel_ratio = pixmap.devicePixelRatio()

    # 计算实际圆角半径
    if isinstance(radius, float) and 0 < radius < 1:
        # 百分比模式：取宽高中较小值的百分比
        base_size = min(pixmap.width(), pixmap.height())
        actual_radius = base_size * radius
    else:
        # 绝对像素模式
        actual_radius = float(radius)

    # 原始尺寸
    orig_width = pixmap.width()
    orig_height = pixmap.height()

    # 考虑设备像素比的实际尺寸
    actual_orig_width = orig_width / device_pixel_ratio
    actual_orig_height = orig_height / device_pixel_ratio

    # 设置最大尺寸限制
    MAX_SIZE = 2000
    if actual_orig_width > MAX_SIZE or actual_orig_height > MAX_SIZE:
        scale_factor = min(MAX_SIZE / actual_orig_width, MAX_SIZE / actual_orig_height)
        scaled_width = int(actual_orig_width * scale_factor)
        scaled_height = int(actual_orig_height * scale_factor)
        # 使用设备像素比创建正确尺寸的 pixmap
        scaled_pixmap = pixmap.scaled(
            scaled_width * device_pixel_ratio,
            scaled_height * device_pixel_ratio,
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        scaled_pixmap.setDevicePixelRatio(device_pixel_ratio)
    else:
        scaled_pixmap = pixmap
        scaled_width, scaled_height = int(actual_orig_width), int(actual_orig_height)

    # 创建目标图像，考虑设备像素比
    dest_image = QPixmap(scaled_width * device_pixel_ratio, scaled_height * device_pixel_ratio)
    dest_image.setDevicePixelRatio(device_pixel_ratio)
    dest_image.fill(Qt.transparent)

    painter = QPainter(dest_image)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.SmoothPixmapTransform)

    # 设置裁剪区域
    path = QPainterPath()
    rect = QRectF(0, 0, scaled_width, scaled_height)
    path.addRoundedRect(rect, actual_radius, actual_radius)
    painter.setClipPath(path)

    # 绘制图像
    painter.drawPixmap(0, 0, scaled_pixmap)
    painter.end()

    return dest_image

def screenshot(widget):
    try:
        widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        widget.setStyleSheet("background: transparent;")
        scale_factor = 3  # 推荐测试3倍缩放
        img = QImage(widget.size() * scale_factor, QImage.Format.Format_ARGB32)
        img.fill(QColor(0, 0, 0, 0))
        img.setDevicePixelRatio(1)  # 关键修改！必须设置为1才能实际放大尺寸
        painter = QPainter(img)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing |
                               QPainter.RenderHint.SmoothPixmapTransform |
                               QPainter.RenderHint.TextAntialiasing)
        # 在渲染前增加缓冲区清理
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
        painter.fillRect(widget.rect(), Qt.GlobalColor.transparent)  # 清理原有内容
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        painter.scale(scale_factor, scale_factor)
        # 添加必要的参数调用 render 方法
        target_offset = QPoint()  # 目标偏移量
        source_region = QRegion(widget.rect())  # 源区域
        render_flags = QWidget.RenderFlag(QWidget.RenderFlag.DrawChildren)
        widget.render(painter, target_offset, source_region, render_flags)
        # 生成uuid随机文件名
        image_path = "./" + str(uuid.uuid4()) + ".png"
        img.save(image_path, "PNG", 100)
        # 释放资源
        painter.end()
    except Exception as e:
        print(f"截图失败,error:{str(e)}")

def pixmap_to_base64(pixmap: QPixmap, image_format: str = "PNG") -> str:
    """
    将 QPixmap 转换为 Base64 编码字符串。

    Args:
        pixmap (QPixmap): 输入的 QPixmap 对象。
        image_format (str): 图像格式，默认为 "PNG"。

    Returns:
        str: Base64 编码的图像字符串。
    """
    if pixmap.isNull():
        raise ValueError("输入的 QPixmap 是空的，无法转换。")

    # 将 QPixmap 转换为 QImage
    image = pixmap.toImage()

    # 创建字节缓冲区
    buffer = QBuffer()
    buffer.open(QBuffer.ReadWrite)
    image.save(buffer, image_format)  # 将图像保存到缓冲区

    # 获取缓冲区中的数据并进行 Base64 编码
    base64_data = base64.b64encode(buffer.data().data()).decode('utf-8')

    # 关闭缓冲区
    buffer.close()

    return base64_data


def compress_pixmap_for_baidu(pixmap: QPixmap, max_size_bytes=9 * 1024 * 1024) -> str:
    """压缩并编码pixmap，返回base64字符串，直到符合百度上传限制"""

    def encode_pixmap(pixmap_obj):
        buffer = QtCore.QBuffer()
        buffer.open(QtCore.QBuffer.ReadWrite)
        # 你可以调节压缩质量，比如 JPEG 的 70%（但 PNG 通常更适合 OCR）
        pixmap_obj.save(buffer, "PNG")
        base64_data = base64.b64encode(buffer.data())
        return urllib.parse.quote(base64_data), len(base64_data)

    # 首先尝试直接编码
    encoded_data, size = encode_pixmap(pixmap)
    if size <= max_size_bytes:
        return encoded_data

    # 如果太大，缩小尺寸再尝试
    width = pixmap.width()
    height = pixmap.height()
    min_width = 15
    min_height = 15

    while width > min_width and height > min_height:
        width = int(width * 0.9)
        height = int(height * 0.9)

        scaled = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        encoded_data, size = encode_pixmap(scaled)

        if size <= max_size_bytes:
            return encoded_data

    raise ValueError("图像压缩后仍超过百度OCR上传限制")