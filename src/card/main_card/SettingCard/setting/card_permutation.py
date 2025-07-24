# coding:utf-8

from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, Signal, QDateTime

from src.component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
from src.card.main_card.SettingCard.setting.CardPermutation.CardStore import CardStore
from src.card.main_card.SettingCard.setting.card_permutation_form import Ui_Form
from src.card.main_card.SettingCard.setting.CardPermutation.CardItemSignals import CardDesignItem
from src.card.main_card.SettingCard.setting.CardPermutation.GridScene import GridScene
from src.module.Box import message_box_util


class CardPermutationWindow(AgileTilesAcrylicWindow, Ui_Form):
    """卡片设计器主窗口"""

    parent = None
    use_parent = None
    setting_signal = Signal(str)
    parent_user_card_data_list = []  # 用户卡片数据列表(用于保存)
    # 卡片宽度
    grid_size = 68
    # 其他数据
    menu_width = 160    # 菜单宽度
    spacing_width = 10  # 间隔宽度
    tab_height = 20
    # 定义卡片盒子的总宽度和总高度的网格数
    box_card_width = 8  # 盒子的总宽度（列数）
    box_card_height = 13  # 盒子的总高度（行数）
    # 卡片商店数据
    card_store_data_list = [{
        "name": "CalendarCard",
        "title": "日期卡片",
        "category": "工具",
        "size_list": [
            "1_1",
            "2_1"
        ]
    }]
    add_card_widget = None
    add_button_list = []
    do_not_ask_me = False            # 关闭前是否不再询问
    is_install_or_update = False    # 是否需要安装、更新卡片

    def __init__(self, parent=None, use_parent=None, user_card_list=None, setting_config=None):
        super(CardPermutationWindow, self).__init__(is_dark=use_parent.is_dark, form_theme_mode=use_parent.form_theme_mode,
                                                 form_theme_transparency=use_parent.form_theme_transparency)
        self.parent = parent
        self.use_parent = use_parent
        # 初始化UI
        self.setupUi(self)
        # 样式初始化
        if self.is_dark:
            self.widget_base.setStyleSheet("""
            QWidget {
                border-radius: 15px;
                border: 5px solid black;
                color: rgb(255, 255, 255);
                background-color: transparent;
            }""")
            widget_style = """
            QWidget {
                border-radius: 10px;
                border: none;
                background-color: rgba(255, 255, 255, 25);
            }"""
            self.widget.setStyleSheet(widget_style)
            self.widget_menu.setStyleSheet(widget_style)
            button_bg_style = """
            QWidget {
                border-radius: 10px;
                border: 1px solid black;
                background-color:rgba(0, 0, 0, 200);
            }"""
            self.widget_left.setStyleSheet(button_bg_style)
            self.widget_middle.setStyleSheet(button_bg_style)
            self.widget_right.setStyleSheet(button_bg_style)
        # 布局初始化
        self.widget_base.setLayout(self.gridLayout_2)
        self.gridLayout_2.setContentsMargins(10, 10, 10, 10)
        # 默认禁止右键菜单
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.parent_user_card_data_list = user_card_list
        # 大小
        setting_data = setting_config
        self.box_card_width = setting_data["width"]
        self.box_card_height = setting_data["height"]
        # 设置标题栏
        self.setWindowTitle("灵卡面板 - 卡片排列设置")
        self.titleBar.minBtn.close()
        self.titleBar.maxBtn.close()
        # 初始化网格占用状态（使用常量定义尺寸）
        self.card_items = []  # 存储所有卡片项的列表
        # 创建图形视图和场景
        self.scene = GridScene(self.grid_size, self.box_card_width, self.box_card_height)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.change_size()
        # 按钮点击事件
        self.push_button_ok.clicked.connect(self.push_button_ok_click)
        self.add_btn.clicked.connect(self.open_add_card_widget)
        self.delete_btn.clicked.connect(self.delete_card)
        self.push_button_add_box_width.clicked.connect(self.push_button_add_box_width_click)
        self.push_button_reduce_box_width.clicked.connect(self.push_button_reduce_box_width_click)
        # 渲染卡片列表
        self.render_card_list()
        # 最大化
        self.showMaximized()
        # 背景
        self.label_background.resize(self.width(), self.height())
        # 按钮防抖机制
        self.last_click_time = 0  # 上次点击时间戳
        self.click_delay = 500    # 防抖延迟(毫秒)

    def set_main_visible(self, visible: bool):
        """设置主界面可见性"""
        self.widget_base.setVisible(visible)
        self.widget_menu.setVisible(visible)

    def open_add_card_widget(self):
        if self.add_card_widget is None:
            self.add_card_widget = CardStore(self, use_parent=self.use_parent, is_dark=self.is_dark)
            self.add_card_widget.cardAdded.connect(self.auto_add_card)
            # 连接关闭信号
            self.add_card_widget.storeClose.connect(lambda: self.set_main_visible(True))
        # 隐藏主界面
        self.set_main_visible(False)
        self.add_card_widget.show()

    def render_card_list(self):
        """渲染卡片列表"""
        card = None
        for user_card_map in self.parent_user_card_data_list:
            # print(user_card_map)
            card_data = user_card_map
            x = int(int(user_card_map["x"]) - 1)
            y = int(int(user_card_map["y"]) - 1)
            card_width = int(user_card_map["size"].split("_")[0])
            card_height = int(user_card_map["size"].split("_")[1])
            card = self.add_card(card_data, x, y, card_width, card_height)
        self.set_card_select(card)

    def auto_add_card(self, card_data):
        """自动判断添加新卡片到场景"""
        print(f"尝试添加卡片: {card_data['name']}, 大小: {card_data['size']}")
        cols = int(card_data["size"].split("_")[0])
        rows = int(card_data["size"].split("_")[1])
        # 寻找第一个可放置位置
        for start_col in range(self.box_card_width):
            # 判断是否越限
            if start_col + cols > self.box_card_width:
                continue
            for start_row in range(self.box_card_height):
                # 判断是否越限
                if start_row + rows > self.box_card_height:
                    continue
                if not self.check_overlay(None, start_col, start_row, cols, rows):
                    card_data["x"] = start_col + 1
                    card_data["y"] = start_row + 1
                    card = self.add_card(card_data, start_col, start_row, cols, rows)
                    self.set_card_select(card)
                    self.add_card_widget.hide()
                    return
        print(f"找不到可用位置! 需要空间: {cols}x{rows}, 当前网格: {self.box_card_width}x{self.box_card_height}")
        message_box_util.box_information(self.use_parent, "警告", "没有足够的空间添加卡片")

    def add_card(self, card_data, start_col, start_row, cols, rows):
        """添加新卡片到场景"""
        card_name = card_data["name"]
        # 创建并添加卡片项
        card = CardDesignItem(self.use_parent, card_data, start_col, start_row, cols, rows, self.grid_size, is_dark=self.is_dark)
        card.card_name = card_name  # 存储卡片名称
        card.signals.moveRequested.connect(self.handle_move)
        self.scene.addItem(card)
        self.card_items.append(card)
        # print(f"添加卡片：{card_name} at ({start_col}, {start_row}) with size ({cols}, {rows})")
        self.refresh_card_data_list()
        return card

    def set_card_select(self, card):
        # 先让所有的卡片取消选中状态
        for item in self.card_items:
            item.setSelected(False)
        # 设置当前卡片为选中状态
        card.setSelected(True)

    def refresh_card_data_list(self):
        self.parent_user_card_data_list = []
        for card_item in self.card_items:
            self.parent_user_card_data_list.append(card_item.get_card_data())

    def handle_move(self, old_col, old_row, new_col, new_row, cols, rows):
        """处理卡片移动请求"""
        # print(f"移动请求：从 ({old_col}, {old_row}) 到 ({new_col}, {new_row}) with size ({cols}, {rows})")
        # 获取卡片
        card = self.get_card(old_col, old_row, cols, rows)
        if not card:
            print("找不到卡片")
            return

        # 边界检查，防止越界
        if new_col < 0: new_col = 0
        if new_row < 0: new_row = 0
        if new_col + cols > self.box_card_width: new_col = self.box_card_width - cols
        if new_row + rows > self.box_card_height: new_row = self.box_card_height - rows

        # 检查新位置是否可用
        if not self.check_overlay(card, new_col, new_row, cols, rows):
            # 无重叠，直接移动
            self.update_position(card.get_card_data(), old_col, old_row, new_col, new_row, cols, rows)
        else:
            # 寻找可交换的目标卡片
            target_card = self.find_swappable_card(card, new_col, new_row, cols, rows)
            if target_card:
                # 有重叠但可以交换
                self.swap_cards(card, target_card, old_col, old_row, new_col, new_row)
            else:
                # 无法交换，移回原位置
                self.move_back(old_col, old_row, cols, rows)

        # 强制更新视图
        self.graphicsView.viewport().update()

    def check_overlay(self, card, new_col, new_row, cols, rows):
        """
        检查卡片在指定位置是否与其他卡片重叠
        """
        for item in self.card_items:
            # 跳过自身卡片
            if card is not None and item == card:
                continue

            item_col = item.get_col()
            item_row = item.get_row()
            rect1 = (item_col, item_row, item_col + item.cols, item_row + item.rows)
            rect2 = (new_col, new_row, new_col + cols, new_row + rows)

            if is_overlap(rect1, rect2):
                return True
        return False

    def find_swappable_card(self, card, new_col, new_row, cols, rows):
        """
        寻找可以交换位置的目标卡片
        """
        for item in self.card_items:
            # 跳过自身卡片
            if item == card:
                continue

            item_col = item.get_col()
            item_row = item.get_row()
            rect1 = (item_col, item_row, item_col + item.cols, item_row + item.rows)
            rect2 = (new_col, new_row, new_col + cols, new_row + rows)

            if is_overlap(rect1, rect2):
                # 检查目标卡片能否移动到原位置而不重叠
                if not self.check_overlay(item, card.col, card.row, item.cols, item.rows):
                    return item
        return None

    def update_position(self, card_date, old_col, old_row, new_col, new_row, cols, rows):
        """更新卡片到新位置"""
        for item in self.card_items:
            if (item.col == old_col and item.row == old_row and
                    item.cols == cols and item.rows == rows):
                item.col = new_col
                item.row = new_row
                print(f"更新{item.card_name}卡片位置：从 ({old_col}, {old_row}) 到 ({new_col}, {new_row}) with size ({cols}, {rows})")
                item.setPos(new_col * self.grid_size, new_row * self.grid_size)
                card_date["x"] = new_col + 1
                card_date["y"] = new_row + 1
                break
        self.refresh_card_data_list()

    def swap_cards(self, card1, card2, card1_old_col, card1_old_row, card2_new_col, card2_new_row):
        """交换两张卡片的位置"""
        # 保存原始位置
        card1_col, card1_row = card1.col, card1.row
        card2_col, card2_row = card2.col, card2.row

        # 更新卡片1位置（移动到卡片2的原位置）
        self.update_position(
            card1.get_card_data(),
            card1_old_col,
            card1_old_row,
            card2_col,
            card2_row,
            card1.cols,
            card1.rows
        )

        # 更新卡片2位置（移动到卡片1的原位置）
        self.update_position(
            card2.get_card_data(),
            card2_col,
            card2_row,
            card1_col,
            card1_row,
            card2.cols,
            card2.rows
        )

        # 检查交换后卡片1的新位置是否与其他卡片重叠
        overlay1 = self.check_overlay(card1, card2_col, card2_row, card1.cols, card1.rows)
        # 检查交换后卡片2的新位置是否与其他卡片重叠
        overlay2 = self.check_overlay(card2, card1_col, card1_row, card2.cols, card2.rows)

        # 新增：检查交换后是否超出边界
        out_of_bound1 = self.is_card_out_of_bound(card1)
        out_of_bound2 = self.is_card_out_of_bound(card2)

        # 如果任一卡片在新位置与其他卡片重叠或超出边界，恢复原始位置
        if overlay1 or overlay2 or out_of_bound1 or out_of_bound2:
            # 恢复卡片1位置
            self.update_position(
                card1.get_card_data(),
                card2_col,
                card2_row,
                card1_old_col,
                card1_old_row,
                card1.cols,
                card1.rows
            )
            # 恢复卡片2位置
            self.update_position(
                card2.get_card_data(),
                card1_col,
                card1_row,
                card2_col,
                card2_row,
                card2.cols,
                card2.rows
            )
            reason = ""
            if overlay1 or overlay2:
                reason += "与其他卡片重叠"
            if out_of_bound1 or out_of_bound2:
                if reason: reason += "且"
                reason += "超出布局区域"
            print(f"交换失败: {card1.card_name} 和 {card2.card_name} {reason}")
        else:
            print(f"交换成功: {card1.card_name} 和 {card2.card_name}")

    # 新增辅助函数：检查卡片是否超出边界
    def is_card_out_of_bound(self, card):
        """检查卡片是否超出布局边界"""
        right_bound = card.col + card.cols
        bottom_bound = card.row + card.rows
        return (card.col < 0 or
                card.row < 0 or
                right_bound > self.box_card_width or
                bottom_bound > self.box_card_height)

    def move_back(self, col, row, cols, rows):
        """将卡片移回原位置"""
        for item in self.card_items:
            if item.col == col and item.row == row and item.cols == cols and item.rows == rows:
                # print(f"将{item.card_name}卡片移回原位置：({col}, {row})")
                item.setPos(col * self.grid_size, row * self.grid_size)
                break
        self.refresh_card_data_list()

    def delete_card(self):
        """删除选中的卡片"""
        # print("删除选中的卡片")
        selected = self.scene.selectedItems()
        for item in selected:
            if isinstance(item, CardDesignItem):
                # 从场景和列表中移除
                self.scene.removeItem(item)
                self.card_items.remove(item)
        self.refresh_card_data_list()

    def get_card(self, col, row, cols, rows):
        """获取指定位置的卡片"""
        for item in self.card_items:
            if item.col == col and item.row == row and item.cols == cols and item.rows == rows:
                return item

    def change_size(self):
        self.scene.set_grid_width(self.box_card_width)
        self.scene.set_grid_height(self.box_card_height)
        box_width = self.grid_size * self.box_card_width
        box_height = self.grid_size * self.box_card_height
        self.graphicsView.setFixedSize(box_width, box_height)
        self.graphicsView.setMinimumWidth(box_width)
        self.graphicsView.setMaximumWidth(box_width)
        self.graphicsView.setMinimumHeight(box_height)
        self.graphicsView.setMaximumHeight(box_height)
        widget_width = box_width + self.spacing_width * 2
        widget_height = box_height + self.spacing_width * 2
        self.widget.setMinimumWidth(widget_width)
        self.widget.setMaximumWidth(widget_width)
        self.widget.setMinimumHeight(widget_height)
        self.widget.setMaximumHeight(widget_height)
        self.widget_menu.setMaximumHeight(widget_height)

    # 布局变宽
    def push_button_add_box_width_click(self):
        # 检测点击间隔
        current_time = QDateTime.currentMSecsSinceEpoch()
        if current_time - self.last_click_time < self.click_delay:
            return
        self.last_click_time = current_time
        # 判断是否超过最大宽度
        if self.box_card_width >= 26:
            message_box_util.box_information(self.use_parent, "提示", "布局宽度不能再扩展了")
            return
        self.box_card_width += 1
        self.refresh_window_show()

    # 布局变窄
    def push_button_reduce_box_width_click(self):
        # 检测点击间隔
        current_time = QDateTime.currentMSecsSinceEpoch()
        if current_time - self.last_click_time < self.click_delay:
            return
        self.last_click_time = current_time
        # 检测是否超过最小宽度
        min_width = self.get_box_has_card_max_width()
        if self.box_card_width <= min_width:
            message_box_util.box_information(self.use_parent, "提示", "布局宽度不能再缩小了，若想变窄需要删除边缘卡片")
            return
        if self.box_card_width > 1:
            self.box_card_width -= 1
            if self.scene is not None:
                self.scene.clear()
            self.refresh_window_show()

    def get_box_has_card_max_width(self):
        """获取有卡片的最大宽度"""
        max_width = 0
        for card_item in self.card_items:
            card_data = card_item.get_card_data()
            # print(card_data)
            card_width = int(card_data["size"].split("_")[0]) + int(card_data["x"]) - 1
            if card_width > max_width:
                max_width = card_width
        return max_width

    def refresh_window_show(self):
        # 刷新视图场景
        if self.scene is not None:
            for card_item in self.card_items:
                card_item.signals.moveRequested.disconnect()
            self.card_items.clear()
            self.scene.clear()
        self.scene = GridScene(self.grid_size, self.box_card_width, self.box_card_height)
        self.graphicsView.setScene(self.scene)
        self.change_size()
        # 渲染卡片列表
        self.render_card_list()
        # 刷新
        self.update()

    def check_all_cards_overlay(self):
        """检查所有卡片是否有重叠"""
        for i, card1 in enumerate(self.card_items):
            for j, card2 in enumerate(self.card_items):
                if i == j:  # 跳过自身
                    continue

                # 获取卡片位置和尺寸
                col1, row1 = card1.col, card1.row
                cols1, rows1 = card1.cols, card1.rows
                col2, row2 = card2.col, card2.row
                cols2, rows2 = card2.cols, card2.rows

                # 创建矩形区域
                rect1 = (col1, row1, col1 + cols1, row1 + rows1)
                rect2 = (col2, row2, col2 + cols2, row2 + rows2)

                # 检查是否重叠
                if is_overlap(rect1, rect2):
                    print(f"发现重叠卡片: {card1.card_name} 和 {card2.card_name}")
                    return True, card1, card2

        return False, None, None

    def push_button_ok_click(self):
        # 是否存在卡片
        if self.card_items is None or len(self.card_items) == 0:
            message_box_util.box_information(self.use_parent, "提示", "请添加卡片，最少需要一个主卡片")
            return

        # 检查是否有主卡片
        has_main_card = False
        for item in self.card_items:
            if item.card_name == "MainCard":
                has_main_card = True
                break
        if not has_main_card:
            message_box_util.box_information(self.use_parent, "提示", "请添加主卡片")
            return

        # 检测是否有部分卡片有多个（部分卡片限制同时只能存在一个）
        only_on_card_name_list = ["MainCard", "DrinkingCard"]
        for item in self.card_items:
            if item.card_name in only_on_card_name_list:
                count = 0
                for item2 in self.card_items:
                    if item2.card_name == item.card_name:
                        count += 1
                if count > 1:
                    title = ""
                    if item.card_name  == "MainCard":
                        title = "主界面"
                    elif item.card_name == "DrinkingCard":
                        title = "喝水"
                    message_box_util.box_information(self.use_parent, "提示", f"{title}卡片最多只能存在一个哦~")
                    return

        # 新增：检查卡片是否超出布局区域
        out_of_bound_cards = []
        for item in self.card_items:
            # 计算卡片右边界和下边界
            right_bound = item.col + item.cols
            bottom_bound = item.row + item.rows

            # 检查是否超出布局范围
            if (item.col < 0 or
                item.row < 0 or
                right_bound > self.box_card_width or
                bottom_bound > self.box_card_height):
                out_of_bound_cards.append(item.card_name)

        if out_of_bound_cards:
            card_names = ", ".join(out_of_bound_cards)
            message_box_util.box_information(
                self.use_parent,
                "警告",
                f"以下卡片超出布局区域：{card_names}，请调整位置后再保存"
            )
            return

        # 全局重叠检查
        has_overlay, card1, card2 = self.check_all_cards_overlay()
        if has_overlay:
            message_box_util.box_information(
                self.use_parent,
                "警告",
                f"卡片 '{card1.card_name}' 和 '{card2.card_name}' 重叠，请调整位置后再保存"
            )
            return

        # 保存卡片数据
        card_list = []
        for item in self.card_items:
            card_list.append(item.get_card_data())
        data = {
            "width": self.box_card_width,
            "height": self.box_card_height,
        }
        self.do_not_ask_me = True                      # 关闭的时候不要再弹窗
        self.parent.save_card_data(card_list, data)
        self.close()

    def closeEvent(self, event):
        # 对于已经点了确定保存的用户不再询问和刷新
        if self.do_not_ask_me:
            super().closeEvent(event)
            return
        # 对于未点保存的用户，如果安装过更新，需要进行询问
        if not self.do_not_ask_me and self.is_install_or_update:
            confirm = message_box_util.box_acknowledgement(self.use_parent, "注意", "注意到您已安装或更新过卡片版本，是否要进行保存呢？")
            if confirm:
                # 如果需要更新，则进行模拟确定操作
                self.push_button_ok_click()
                return
        # 对于未点保存的用户，如果[未安装过更新]或[安装过更新但是不需要保存]，则直接进行关闭
        super().closeEvent(event)

def is_overlap(box1, box2):
    # box1: 设备win框，偏小
    # box2: spec中win的ROI框，偏大
    x_min1, y_min1, x_max1, y_max1 = box1
    x_min2, y_min2, x_max2, y_max2 = box2
    if x_max1 > x_min2 and x_max2 > x_min1 and y_max1 > y_min2 and y_max2 > y_min1:
        return True
    else:
        return False

def get_icon_park_path(icon_position, is_dark):
    icon_theme_folder = "light" if is_dark else "dark"
    return QIcon("./static/img/IconPark/" + icon_theme_folder + "/" + icon_position + ".png")
