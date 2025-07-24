# MIT License
#
# Copyright (c) 2022 Leonid Gvozdev
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from PySide6 import QtWidgets, QtCore, QtGui


class BoxShadow(QtWidgets.QGraphicsEffect):
    def __init__(self, shadow_list: list = None, border: int = 0, smooth: bool = False):

        QtWidgets.QGraphicsEffect.__init__(self)
        self._shadow_list = []

        self._max_x_offset = 0
        self._max_y_offset = 0
        self._border = 0
        self._smooth = smooth
        self.setShadowList(shadow_list)
        self.setBorder(border)

    def setShadowList(self, shadow_list: list = None):
        if shadow_list is None:
            shadow_list = []
        self._shadow_list = shadow_list

        self._set_max_offset()

    def setBorder(self, border: int):
        if border > 0:
            self._border = border
        else:
            self._border = 0

    def necessary_indentation(self):
        return self._max_x_offset, self._max_y_offset

    def boundingRectFor(self, rect):
        return rect.adjusted(-self._max_x_offset, -self._max_y_offset,
                             self._max_x_offset, self._max_y_offset)

    def _set_max_offset(self):
        for shadow in self._shadow_list:
            if "outside" in shadow.keys():
                if self._max_x_offset < abs(shadow["offset"][0]) \
                        + shadow["blur"] * 2:
                    self._max_x_offset = abs(shadow["offset"][0]) \
                                         + shadow["blur"] * 2
                if self._max_y_offset < abs(shadow["offset"][1]) \
                        + shadow["blur"] * 2:
                    self._max_y_offset = abs(shadow["offset"][1]) \
                                         + shadow["blur"] * 2

    @staticmethod
    def _blur_pixmap(src, blur_radius):
        w, h = src.width(), src.height()

        effect = QtWidgets.QGraphicsBlurEffect(blurRadius=blur_radius)

        scene = QtWidgets.QGraphicsScene()
        item = QtWidgets.QGraphicsPixmapItem()
        item.setPixmap(QtGui.QPixmap(src))
        item.setGraphicsEffect(effect)
        scene.addItem(item)

        res = QtGui.QImage(QtCore.QSize(w, h),
                           QtGui.QImage.Format.Format_ARGB32)
        res.fill(QtCore.Qt.GlobalColor.transparent)

        ptr = QtGui.QPainter(res)
        ptr.setRenderHints(
                QtGui.QPainter.RenderHint.Antialiasing |
                QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        scene.render(ptr, QtCore.QRectF(), QtCore.QRectF(0, 0, w, h))
        ptr.end()

        return QtGui.QPixmap(res)

    @staticmethod
    def _colored_pixmap(color: QtGui.QColor, pixmap: QtGui.QPixmap):
        new_pixmap = QtGui.QPixmap(pixmap)
        new_pixmap.fill(color)
        painter = QtGui.QPainter(new_pixmap)
        painter.setTransform(QtGui.QTransform())
        painter.setRenderHints(
                QtGui.QPainter.RenderHint.Antialiasing |
                QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        painter.setCompositionMode(
                QtGui.QPainter.CompositionMode.CompositionMode_DestinationIn)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        return new_pixmap

    @staticmethod
    def _cut_shadow(pixmap: QtGui.QPixmap,
                    source: QtGui.QPixmap,
                    offset_x, offset_y):
        painter = QtGui.QPainter(pixmap)
        painter.setTransform(QtGui.QTransform())
        painter.setRenderHints(
                QtGui.QPainter.RenderHint.Antialiasing |
                QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        painter.setCompositionMode(
                QtGui.QPainter.CompositionMode.CompositionMode_DestinationOut)
        painter.drawPixmap(offset_x, offset_y, source)
        painter.end()
        return pixmap

    def _outside_shadow(self):

        source = self.sourcePixmap(
                QtCore.Qt.CoordinateSystem.DeviceCoordinates)

        if isinstance(source, tuple):
            source = source[0]

        mask = source.createMaskFromColor(
                QtGui.QColor(0, 0, 0, 0), QtCore.Qt.MaskMode.MaskInColor)

        _pixmap_shadow_list = []

        for _shadow in self._shadow_list:
            if "outside" in _shadow.keys():
                shadow = QtGui.QPixmap(mask.size())
                shadow.fill(QtCore.Qt.GlobalColor.transparent)
                shadow_painter = QtGui.QPainter(shadow)
                shadow_painter.setRenderHints(
                        QtGui.QPainter.RenderHint.Antialiasing |
                        QtGui.QPainter.RenderHint.SmoothPixmapTransform)
                shadow_painter.setTransform(QtGui.QTransform())
                shadow_painter.setPen(QtGui.QColor(_shadow["color"]))
                shadow_painter.drawPixmap(_shadow["offset"][0],
                                          _shadow["offset"][1], mask)
                shadow_painter.end()

                _pixmap_shadow_list.append(shadow)

        outside_shadow = QtGui.QPixmap(mask.size())
        outside_shadow.fill(QtCore.Qt.GlobalColor.transparent)

        outside_shadow_painter = QtGui.QPainter(outside_shadow)
        outside_shadow_painter.setTransform(QtGui.QTransform())
        outside_shadow_painter.setRenderHints(
                QtGui.QPainter.RenderHint.Antialiasing |
                QtGui.QPainter.RenderHint.SmoothPixmapTransform)

        for i, pixmap in enumerate(_pixmap_shadow_list):
            outside_shadow_painter.drawPixmap(
                    0, 0,
                    self._blur_pixmap(pixmap, self._shadow_list[i]["blur"]))

        outside_shadow_painter.end()

        source = self.sourcePixmap(
                QtCore.Qt.CoordinateSystem.DeviceCoordinates)

        if isinstance(source, tuple):
            source = source[0]

        mask = source.createMaskFromColor(
                QtGui.QColor(0, 0, 0, 0), QtCore.Qt.MaskMode.MaskOutColor)

        outside_shadow.setMask(mask)

        return outside_shadow

    def _inside_shadow(self):

        source = self.sourcePixmap(
                QtCore.Qt.CoordinateSystem.DeviceCoordinates)

        if isinstance(source, tuple):
            source = source[0]

        mask = source.createMaskFromColor(
                QtGui.QColor(0, 0, 0, 0), QtCore.Qt.MaskMode.MaskInColor)

        _pixmap_shadow_list = []

        for _shadow in self._shadow_list:
            if "inside" in _shadow.keys():
                shadow = QtGui.QPixmap(mask.size())
                shadow.fill(QtCore.Qt.GlobalColor.transparent)
                shadow_painter = QtGui.QPainter(shadow)
                shadow_painter.setRenderHints(
                        QtGui.QPainter.RenderHint.Antialiasing |
                        QtGui.QPainter.RenderHint.SmoothPixmapTransform)

                removed_color = "#000000"
                color = QtGui.QColor(_shadow["color"])
                if removed_color == color.name():
                    removed_color = "#FFFFFF"

                shadow_painter.setTransform(QtGui.QTransform())
                shadow_painter.setPen(color)
                shadow_painter.drawPixmap(0, 0, mask)
                shadow_painter.setPen(QtGui.QColor(removed_color))
                shadow_painter.drawPixmap(_shadow["offset"][0],
                                          _shadow["offset"][1], mask)

                shadow_mask = shadow.createMaskFromColor(
                        color,
                        QtCore.Qt.MaskMode.MaskOutColor)
                shadow.fill(QtCore.Qt.GlobalColor.transparent)
                shadow_painter.setPen(color)
                shadow_painter.drawPixmap(0, 0, shadow_mask)

                shadow_painter.end()

                shadow.scaled(mask.size())

                _pixmap_shadow_list.append(shadow)

        inside_shadow = QtGui.QPixmap(mask.size())
        inside_shadow.fill(QtCore.Qt.GlobalColor.transparent)

        inside_shadow_painter = QtGui.QPainter(inside_shadow)
        inside_shadow_painter.setTransform(QtGui.QTransform())
        inside_shadow_painter.setRenderHints(
                QtGui.QPainter.RenderHint.Antialiasing |
                QtGui.QPainter.RenderHint.SmoothPixmapTransform)

        for i, pixmap in enumerate(_pixmap_shadow_list):
            inside_shadow_painter.drawPixmap(
                    0, 0,
                    self._blur_pixmap(pixmap, self._shadow_list[i]["blur"]))

        inside_shadow_painter.end()

        inside_shadow.setMask(mask)

        return inside_shadow

    def _smooth_outside_shadow(self):
        source = self.sourcePixmap(
                QtCore.Qt.CoordinateSystem.DeviceCoordinates)

        if isinstance(source, tuple):
            source = source[0]

        if isinstance(source, tuple):
            source = source[0]

        w, h = source.width(), source.height()

        _pixmap_shadow_list = []

        for _shadow in self._shadow_list:
            if "outside" in _shadow.keys():
                shadow = QtGui.QPixmap(source.size())
                shadow.fill(QtCore.Qt.GlobalColor.transparent)
                shadow_painter = QtGui.QPainter(shadow)
                shadow_painter.setRenderHints(
                        QtGui.QPainter.RenderHint.Antialiasing |
                        QtGui.QPainter.RenderHint.SmoothPixmapTransform)
                shadow_painter.setTransform(QtGui.QTransform())
                shadow_painter.drawPixmap(
                        _shadow["offset"][0],
                        _shadow["offset"][1],
                        w, h,
                        self._colored_pixmap(_shadow["color"], source))
                shadow_painter.end()

                _pixmap_shadow_list.append(shadow)

        outside_shadow = QtGui.QPixmap(source.size())
        outside_shadow.fill(QtCore.Qt.GlobalColor.transparent)

        outside_shadow_painter = QtGui.QPainter(outside_shadow)
        outside_shadow_painter.setTransform(QtGui.QTransform())
        outside_shadow_painter.setRenderHints(
                QtGui.QPainter.RenderHint.Antialiasing |
                QtGui.QPainter.RenderHint.SmoothPixmapTransform)

        for i, pixmap in enumerate(_pixmap_shadow_list):
            outside_shadow_painter.drawPixmap(
                    0, 0, w, h,
                    self._blur_pixmap(pixmap, self._shadow_list[i]["blur"]))

        outside_shadow_painter.end()

        outside_shadow_painter = QtGui.QPainter(outside_shadow)
        outside_shadow_painter.setTransform(QtGui.QTransform())
        outside_shadow_painter.setRenderHints(
                QtGui.QPainter.RenderHint.Antialiasing |
                QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        outside_shadow_painter.setCompositionMode(
                QtGui.QPainter.CompositionMode.CompositionMode_DestinationOut)
        outside_shadow_painter.drawPixmap(0, 0, w, h, source)

        outside_shadow_painter.end()

        return outside_shadow

    def _smooth_inside_shadow(self):

        source = self.sourcePixmap(
                QtCore.Qt.CoordinateSystem.DeviceCoordinates)

        if isinstance(source, tuple):
            source = source[0]

        w, h = source.width(), source.height()

        _pixmap_shadow_list = []

        for _shadow in self._shadow_list:
            if "inside" in _shadow.keys():
                shadow = QtGui.QPixmap(source.size())
                shadow.fill(QtCore.Qt.GlobalColor.transparent)
                shadow_painter = QtGui.QPainter(shadow)
                shadow_painter.setRenderHints(
                        QtGui.QPainter.RenderHint.Antialiasing |
                        QtGui.QPainter.RenderHint.SmoothPixmapTransform)
                shadow_painter.setTransform(QtGui.QTransform())
                new_source = self._colored_pixmap(_shadow["color"], source)
                shadow_painter.drawPixmap(
                        0, 0, w, h,
                        self._cut_shadow(new_source, source,
                                         _shadow["offset"][0] / 2,
                                         _shadow["offset"][1] / 2))
                shadow_painter.end()

                _pixmap_shadow_list.append(shadow)

        inside_shadow = QtGui.QPixmap(source.size())
        inside_shadow.fill(QtCore.Qt.GlobalColor.transparent)

        inside_shadow_painter = QtGui.QPainter(inside_shadow)
        inside_shadow_painter.setTransform(QtGui.QTransform())
        inside_shadow_painter.setRenderHints(
                QtGui.QPainter.RenderHint.Antialiasing |
                QtGui.QPainter.RenderHint.SmoothPixmapTransform)

        for i, pixmap in enumerate(_pixmap_shadow_list):
            inside_shadow_painter.drawPixmap(
                    0, 0, w, h,
                    self._blur_pixmap(pixmap, self._shadow_list[i]["blur"]))

        inside_shadow_painter.end()

        inside_shadow_painter = QtGui.QPainter(inside_shadow)
        inside_shadow_painter.setTransform(QtGui.QTransform())
        inside_shadow_painter.setRenderHints(
                QtGui.QPainter.RenderHint.Antialiasing |
                QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        inside_shadow_painter.setCompositionMode(
                QtGui.QPainter.CompositionMode.CompositionMode_DestinationIn)
        inside_shadow_painter.drawPixmap(0, 0, w, h, source)

        inside_shadow_painter.end()

        return inside_shadow

    def draw(self, painter):

        painter.setRenderHints(
                QtGui.QPainter.RenderHint.Antialiasing |
                QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        restoreTransform = painter.worldTransform()

        source_rect = self.boundingRectFor(
                self.sourceBoundingRect(
                        QtCore.Qt.CoordinateSystem.DeviceCoordinates)).toRect()
        x, y, w, h = source_rect.getRect()

        source = self.sourcePixmap(
                QtCore.Qt.CoordinateSystem.DeviceCoordinates)

        if isinstance(source, tuple):
            source = source[0]

        painter.setTransform(QtGui.QTransform())

        if self._smooth:
            outside_shadow = self._smooth_outside_shadow()
            inside_shadow = self._smooth_inside_shadow()
        else:
            outside_shadow = self._outside_shadow()
            inside_shadow = self._inside_shadow()

        painter.setPen(QtCore.Qt.PenStyle.NoPen)

        painter.drawPixmap(x, y, w, h, outside_shadow)
        painter.drawPixmap(x, y, source)
        painter.drawPixmap(x + self._border, y + self._border,
                           w - self._border * 2, h - self._border * 2,
                           inside_shadow)
        painter.setWorldTransform(restoreTransform)

        painter.end()


class BoxShadowWrapper(QtWidgets.QWidget):
    def __init__(self, widget, shadow_list: list = None,
                 border: int = 0, disable_margins: bool = False,
                 margins = None,
                 smooth: bool = False):
        QtWidgets.QWidget.__init__(self)

        self._widget = widget
        self.mLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mLayout)

        self.mLayout.addWidget(self._widget)

        self.boxShadow = BoxShadow(shadow_list, border, smooth)
        self._widget.setGraphicsEffect(self.boxShadow)

        self.disable_margins = True if (disable_margins is True or
                                        margins is not None) else False

        if not self.disable_margins:
            X, Y = self.boxShadow.necessary_indentation()
            self.mLayout.setContentsMargins(X, Y, X, Y)
        elif margins is not None:
            if len(margins) == 2:
                self.mLayout.setContentsMargins(
                        margins[0], margins[1], margins[0], margins[1])
            elif len(margins) == 4:
                self.mLayout.setContentsMargins(
                        margins[0], margins[1], margins[2], margins[3])

    def setShadowList(self, shadow_list: list = None):
        self.boxShadow.setShadowList(shadow_list)
        if not self.disable_margins:
            X, Y = self.boxShadow.necessary_indentation()
            self.mLayout.setContentsMargins(X, Y, X, Y)

    def setBorder(self, border: int):
        self.boxShadow.setBorder(border)