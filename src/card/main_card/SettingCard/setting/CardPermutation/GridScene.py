# coding:utf-8
from PySide6.QtCore import QRect
from PySide6.QtWidgets import QGraphicsScene



class GridScene(QGraphicsScene):
    """带网格背景的图形场景"""

    def __init__(self, grid_size, grid_width, grid_height):
        """
        初始化网格场景
        :param grid_size: 单个网格的像素大小
        :param grid_width: 网格总列数
        :param grid_height: 网格总行数
        """
        super().__init__()
        self.grid_size = grid_size
        self.grid_width = grid_width
        self.grid_height = grid_height
        # 设置场景矩形大小
        self.setSceneRect(QRect(0, 0, grid_size * grid_width, grid_size * grid_height))

    def drawBackground(self, painter, rect):
        """绘制网格背景"""
        # 先调用父类方法确保正确绘制流程
        super().drawBackground(painter, rect)

    def set_grid_width(self, grid_width):
        self.grid_width = grid_width

    def set_grid_height(self, grid_height):
        self.grid_height = grid_height