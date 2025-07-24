from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, QIcon

from src.module.Screen import screen_module
from src.ui import my_color


class UiSetting:
    def __init__(self, parent):
        self.parent = parent
        self.card_size = QSize(self.parent.card_width, self.parent.card_height)
        self.card_theme = self.parent.theme
        self.card_title_show = True

    def get_card_size(self):
        return self.card_size

    def get_card_theme(self):
        return self.card_theme

    def is_dark(self):
        return self.card_theme == 'Dark'

    def is_light(self):
        return self.card_theme == 'Light'

    def get_card_title_show(self):
        return self.card_title_show

    def set_card_title_show(self, card_title_show):
        self.card_title_show = card_title_show
        print(f"设置卡片标题显示:{self.card_title_show}")

    def get_park_path(self, icon_position):
        icon_theme_folder = "light" if self.is_dark() else "dark"
        return "./static/img/IconPark/" + icon_theme_folder + "/" + icon_position + ".png"

    def get_icon_park_path(self, icon_position):
        icon_theme_folder = "light" if self.is_dark() else "dark"
        return QIcon("./static/img/IconPark/" + icon_theme_folder + "/" + icon_position + ".png")

    def get_pixmap_park_path(self, icon_position):
        icon_theme_folder = "light" if self.is_dark() else "dark"
        return QPixmap("./static/img/IconPark/" + icon_theme_folder + "/" + icon_position + ".png")

    def get_prospect_color(self, rgb=False, rgba=False, hex=False, hexa=False, qt_type=False):
        return my_color.get_prospect_color(self.is_dark(), rgb, rgba, hex, hexa, qt_type)

    def get_background_color(self, rgb=False, rgba=False, hex=False, hexa=False, qt_type=False):
        return my_color.get_background_color(self.is_dark(), rgb, rgba, hex, hexa, qt_type)

    def get_screen(self):
        return screen_module.get_screen(self.parent.main_object)
