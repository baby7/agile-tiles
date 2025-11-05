# coding:utf-8
import json
import sys

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QListWidget, QListWidgetItem
from PySide6.QtCore import Qt, Signal

from src.card.main_card.SettingCard.setting.setting_menu_form import Ui_Form
from src.constant import data_save_constant
from src.module.Box import message_box_util
from src.my_component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
import src.ui.style_util as style_util


class ProtectedListWidget(QListWidget):
    def __init__(self, use_parent, fixed_menu_ids, parent=None):
        super().__init__(parent)
        self.use_parent = use_parent
        self.fixed_menu_ids = fixed_menu_ids
        self.setDragDropMode(QListWidget.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionMode(QListWidget.SingleSelection)
        self.setAlternatingRowColors(False)  # 取消隔行变色

    def get_menu_id_at_row(self, row):
        """获取指定行的菜单ID"""
        if 0 <= row < self.count():
            item = self.item(row)
            if item:
                menu_data = item.data(Qt.UserRole)
                return menu_data.get('name', '')
        return ''

    def is_fixed_menu(self, row):
        """检查指定行是否为固定菜单"""
        menu_id = self.get_menu_id_at_row(row)
        return menu_id in self.fixed_menu_ids

    def dropEvent(self, event):
        """重写拖拽事件，实现固定菜单保护"""
        # 获取拖拽源
        source = event.source()

        # 如果不是从同一个列表拖拽，使用默认行为
        if source != self:
            super().dropEvent(event)
            return

        # 获取目标位置
        drop_pos = event.position().toPoint()
        target_row = self.indexAt(drop_pos).row()

        # 如果目标位置无效，放在最后
        if target_row == -1:
            target_row = self.count()

        # 获取被拖拽的项目
        dragged_items = self.selectedItems()
        if not dragged_items:
            return

        dragged_item = dragged_items[0]
        dragged_row = self.row(dragged_item)
        dragged_menu_data = dragged_item.data(Qt.UserRole)
        dragged_menu_id = dragged_menu_data.get('name', '')

        # 检查是否尝试移动固定菜单
        if dragged_menu_id in self.fixed_menu_ids:
            message_box_util.box_information(self.use_parent, "操作禁止", "固定菜单不能移动！")
            return

        # 检查是否尝试移动到固定菜单之上
        if target_row < self.count():
            target_menu_id = self.get_menu_id_at_row(target_row)
            if target_menu_id in self.fixed_menu_ids:
                message_box_util.box_information(self.use_parent, "操作禁止", "不能移动到固定菜单之上！")
                return

        # 检查是否尝试插入到固定菜单之间
        # 找到固定菜单的边界
        fixed_menu_count = 0
        for i in range(self.count()):
            if self.is_fixed_menu(i):
                fixed_menu_count += 1
            else:
                break

        # 如果目标位置在固定菜单区域内，且不是最后一个固定菜单之后的位置，则禁止
        if target_row < fixed_menu_count and dragged_row >= fixed_menu_count:
            message_box_util.box_information(self.use_parent, "操作禁止", "不能插入到固定菜单之间！")
            return

        # 允许拖拽
        super().dropEvent(event)

    def startDrag(self, supportedActions):
        """重写开始拖拽事件，检查是否为固定菜单"""
        dragged_items = self.selectedItems()
        if dragged_items:
            dragged_item = dragged_items[0]
            menu_data = dragged_item.data(Qt.UserRole)
            menu_id = menu_data.get('name', '')

            # 如果是固定菜单，禁止拖拽
            if menu_id in self.fixed_menu_ids:
                return

        super().startDrag(supportedActions)


class DraggableListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragDropMode(QListWidget.NoDragDrop)  # 左侧列表禁止拖拽
        self.setSelectionMode(QListWidget.SingleSelection)
        self.setAlternatingRowColors(False)  # 取消隔行变色


class SettingMenuWindow(AgileTilesAcrylicWindow, Ui_Form):

    use_parent = None
    setting_config = None
    setting_signal = Signal(str)
    official_list = None
    user_list = None
    fixed_menu_ids = []

    def __init__(self, parent=None, use_parent=None, setting_config=None):
        super(SettingMenuWindow, self).__init__(is_dark=use_parent.is_dark, form_theme_mode=use_parent.form_theme_mode,
                                                  form_theme_transparency=use_parent.form_theme_transparency)
        self.setupUi(self)
        # 初始化
        self.parent = parent
        self.use_parent = use_parent
        self.setting_config = setting_config
        # 初始化布局
        self.widget_base.setLayout(self.gridLayout)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        # 设置标题栏
        self.setWindowTitle("灵卡面板 - 菜单设置")
        self.titleBar.minBtn.close()
        self.titleBar.maxBtn.close()
        # 加载数据
        self.load_date()
        # 点击事件
        self.push_button_ok.clicked.connect(self.push_button_submit_clicked)
        # 官方菜单数据
        self.official_menu_data = [
            {"name": "user", "title": "用户管理", "fixed": True},
            {"name": "setting", "title": "设置", "fixed": True},
            {"name": "trending", "title": "热搜", "fixed": False},
            {"name": "translate", "title": "翻译", "fixed": False},
            {"name": "chat", "title": "智能助手", "fixed": False},
            {"name": "tool", "title": "工具箱", "fixed": False},
            {"name": "looking", "title": "信息聚合", "fixed": False},
            {"name": "search", "title": "本地搜索", "fixed": False},
            {"name": "ipn", "title": "局域网文件传输", "fixed": False},
            {"name": "todo", "title": "待办事项", "fixed": False},
            {"name": "book", "title": "阅读", "fixed": False},
            {"name": "music", "title": "音乐", "fixed": False},
            {"name": "website", "title": "更多", "fixed": False},
        ]
        # 用户菜单配置（不包含固定菜单）
        self.user_menu_config = [
            {"name": "trending", "sort": 1},
            {"name": "translate", "sort": 2},
            {"name": "chat", "sort": 3}
        ]
        self.fixed_menu_ids = ["user", "setting"]
        # 初始化控件
        self.init_ui()
        # 加载菜单数据
        self.load_menu_data(self.official_menu_data, self.user_menu_config)
        # 设置样式
        style_util.set_dialog_control_style(self, self.is_dark)
        # 初始化主题
        self.init_theme()

    def load_menu_data(self, official_menus, user_menus=None):
        """加载菜单数据
        Args:
            official_menus: 官方菜单列表，包含所有可用菜单
            user_menus: 用户菜单列表，包含用户已选择的菜单id和排序
        """
        try:
            # 清空列表
            self.official_list.clear()
            self.user_list.clear()

            # 构建用户菜单ID集合（用于快速查找）
            user_menu_ids = set()
            # 添加固定菜单ID
            user_menu_ids.update(self.fixed_menu_ids)
            # 添加用户选择的菜单ID
            if user_menus:
                for menu in user_menus:
                    user_menu_ids.add(menu.get('name', ''))

            # 加载官方菜单到左侧列表
            official_menu_dict = {}
            for menu in official_menus:
                menu_id = menu.get('name', '')
                official_menu_dict[menu_id] = menu

                # 只将非固定菜单添加到官方列表
                if menu_id not in self.fixed_menu_ids:
                    item = QListWidgetItem(menu.get('title', ''))

                    # 如果菜单已在用户菜单中，添加✅标记
                    if menu_id in user_menu_ids:
                        item.setText(f"{menu.get('title', '')} ✅")

                    item.setData(Qt.UserRole, menu)
                    self.official_list.addItem(item)

            # 加载固定菜单到用户列表
            for menu_id in self.fixed_menu_ids:
                if menu_id in official_menu_dict:
                    menu_data = official_menu_dict[menu_id]
                    self.add_menu_to_user_list(menu_data)

            # 加载用户菜单到右侧列表
            if user_menus:
                # 按sort排序
                sorted_user_menus = sorted(user_menus, key=lambda x: x.get('sort', 0))
                for user_menu in sorted_user_menus:
                    menu_id = user_menu.get('name', '')
                    if menu_id in official_menu_dict and menu_id not in self.fixed_menu_ids:
                        menu_data = official_menu_dict[menu_id]
                        self.add_menu_to_user_list(menu_data)

        except Exception as e:
            message_box_util.box_information(self.use_parent, "错误", f"加载菜单数据失败: {str(e)}")

    def update_official_list_display(self):
        """更新左侧官方菜单的显示，添加✅标记"""
        # 获取当前用户菜单中的所有菜单ID
        user_menu_ids = set()
        for i in range(self.user_list.count()):
            item = self.user_list.item(i)
            menu_data = item.data(Qt.UserRole)
            user_menu_ids.add(menu_data.get('name', ''))

        # 更新官方菜单的显示
        for i in range(self.official_list.count()):
            item = self.official_list.item(i)
            menu_data = item.data(Qt.UserRole)
            menu_id = menu_data.get('name', '')
            original_text = menu_data.get('title', '')

            # 根据是否在用户菜单中更新显示文本
            if menu_id in user_menu_ids:
                item.setText(f"{original_text} ✅")
            else:
                item.setText(original_text)

    def add_menu_to_user_list(self, menu_data):
        """将菜单添加到用户列表"""
        # 检查是否已存在
        exists = False
        for i in range(self.user_list.count()):
            existing_item = self.user_list.item(i)
            existing_data = existing_item.data(Qt.UserRole)
            if existing_data.get('name') == menu_data.get('name'):
                exists = True
                break

        if not exists:
            item = QListWidgetItem(menu_data.get('title', ''))
            item.setData(Qt.UserRole, menu_data)

            # 如果是固定菜单，设置特殊外观
            if menu_data.get('name') in self.fixed_menu_ids:
                item.setFlags(item.flags() & ~Qt.ItemIsDragEnabled)  # 禁止拖拽
                # 设置固定菜单的特殊样式
                item.setBackground(QColor(245, 245, 245))  # 浅灰色背景
                item.setForeground(QColor(120, 120, 120))  # 深灰色文字
                # 添加固定标识
                item.setText(f"{menu_data.get('title', '')} 🔒")

            self.user_list.addItem(item)

            # 更新左侧官方菜单的✅显示
            self.update_official_list_display()

    def add_selected(self):
        """添加选中的菜单到用户列表"""
        for item in self.official_list.selectedItems():
            menu_data = item.data(Qt.UserRole)
            self.add_menu_to_user_list(menu_data)

    def remove_selected(self):
        """从用户列表中移除选中的菜单（固定菜单除外）"""
        for item in self.user_list.selectedItems():
            menu_data = item.data(Qt.UserRole)
            menu_id = menu_data.get('name', '')

            # 检查是否为固定菜单
            if menu_id not in self.fixed_menu_ids:
                row = self.user_list.row(item)
                self.user_list.takeItem(row)
                # 更新左侧官方菜单的✅显示
                self.update_official_list_display()
            else:
                message_box_util.box_information(self.use_parent, "提示", "固定菜单不能移除！")

    def move_up(self):
        """上移选中的菜单项（固定菜单除外）"""
        current_row = self.user_list.currentRow()
        if current_row > 0:
            menu_data = self.user_list.item(current_row).data(Qt.UserRole)
            menu_id = menu_data.get('name', '')

            # 检查是否为固定菜单
            if menu_id in self.fixed_menu_ids:
                message_box_util.box_information(self.use_parent, "提示", "固定菜单不能移动！")
                return

            # 检查目标位置是否为固定菜单
            target_menu_data = self.user_list.item(current_row - 1).data(Qt.UserRole)
            target_menu_id = target_menu_data.get('name', '')

            if target_menu_id in self.fixed_menu_ids:
                message_box_util.box_information(self.use_parent, "提示", "不能移动到固定菜单之上！")
                return

            item = self.user_list.takeItem(current_row)
            self.user_list.insertItem(current_row - 1, item)
            self.user_list.setCurrentRow(current_row - 1)

    def move_down(self):
        """下移选中的菜单项（固定菜单除外）"""
        current_row = self.user_list.currentRow()
        if current_row < self.user_list.count() - 1:
            menu_data = self.user_list.item(current_row).data(Qt.UserRole)
            menu_id = menu_data.get('name', '')

            # 检查是否为固定菜单
            if menu_id in self.fixed_menu_ids:
                message_box_util.box_information(self.use_parent, "提示", "固定菜单不能移动！")
                return

            item = self.user_list.takeItem(current_row)
            self.user_list.insertItem(current_row + 1, item)
            self.user_list.setCurrentRow(current_row + 1)

    def get_user_menus(self):
        """获取用户菜单配置（不包含固定菜单）"""
        user_menus = []
        sort_index = 1

        for i in range(self.user_list.count()):
            item = self.user_list.item(i)
            menu_data = item.data(Qt.UserRole)
            menu_id = menu_data.get('name', '')

            # 只记录非固定菜单
            if menu_id not in self.fixed_menu_ids:
                user_menus.append({
                    "name": menu_id,
                    "sort": sort_index
                })
                sort_index += 1

        return user_menus

    def get_result_json(self):
        """获取完整菜单结果的JSON数据"""
        menus = []
        for i in range(self.user_list.count()):
            item = self.user_list.item(i)
            menu_data = item.data(Qt.UserRole)
            # 移除锁图标（如果存在）
            cleaned_data = menu_data.copy()
            if cleaned_data.get('name') in self.fixed_menu_ids:
                cleaned_data['title'] = cleaned_data['title'].replace(' 🔒', '')
            menus.append(cleaned_data)

        return json.dumps(menus, ensure_ascii=False, indent=2)

    def init_ui(self):
        title_style = "font-size: 14px; background:transparent; border:none;"
        self.title_left.setStyleSheet(title_style)
        self.title_right.setStyleSheet(title_style)
        self.official_list = DraggableListWidget()
        self.left_layout.addWidget(self.official_list)
        self.user_list = ProtectedListWidget(self.use_parent, self.fixed_menu_ids)
        self.right_layout.addWidget(self.user_list)
        self.add_btn.setMinimumWidth(100)
        self.remove_btn.setMinimumWidth(100)
        self.up_btn.setMinimumWidth(100)
        self.down_btn.setMinimumWidth(100)
        # 连接信号
        self.add_btn.clicked.connect(self.add_selected)
        self.remove_btn.clicked.connect(self.remove_selected)
        self.up_btn.clicked.connect(self.move_up)
        self.down_btn.clicked.connect(self.move_down)

    def init_theme(self):
        if self.is_dark:
            self.official_list.setStyleSheet("""
                QListWidget {
                    border: 1px solid #c0c0c0;
                    border-radius: 4px;
                    outline: none;
                }
                QListWidget::item {
                    border: none;
                    padding: 8px 12px;
                    border-bottom: 1px solid #f0f0f0;
                }
                QListWidget::item:selected {
                    background-color: rgba(165, 215, 253, 180);
                    border-radius: 3px;
                }
            """)
            self.user_list.setStyleSheet("""
                QListWidget {
                    border: 1px solid #c0c0c0;
                    border-radius: 4px;
                    outline: none;
                }
                QListWidget::item {
                    border: none;
                    padding: 8px 12px;
                    border-bottom: 1px solid #f0f0f0;
                }
                QListWidget::item:selected {
                    background-color: rgba(165, 215, 253, 180);
                    border-radius: 3px;
                }
            """)
        else:
            self.official_list.setStyleSheet("""
                QListWidget {
                    border: 1px solid #c0c0c0;
                    border-radius: 4px;
                    outline: none;
                    background:transparent;
                }
                QListWidget::item {
                    border: none;
                    padding: 8px 12px;
                    border-bottom: 1px solid #f0f0f0;
                }
                QListWidget::item:selected {
                    background-color: rgba(165, 215, 253, 180);
                    border-radius: 3px;
                }
            """)
            self.user_list.setStyleSheet("""
                QListWidget {
                    border: 1px solid #c0c0c0;
                    border-radius: 4px;
                    outline: none;
                    background:transparent;
                }
                QListWidget::item {
                    border: none;
                    padding: 8px 12px;
                    border-bottom: 1px solid #f0f0f0;
                }
                QListWidget::item:selected {
                    background-color: rgba(165, 215, 253, 180);
                    border-radius: 3px;
                }
            """)

    def load_date(self):
        """
        加载数据到界面
        """
        try:
            # 菜单栏位置
            if self.setting_config['menuPosition'] == "Left":
                self.radio_button_menu_location_left.setChecked(True)
            else:
                self.radio_button_menu_location_right.setChecked(True)
        except Exception as e:
            print(f"setting_screen load_date 2 error: {str(e)}")


    def push_button_submit_clicked(self):
        confirm = message_box_util.box_acknowledgement(self.use_parent, "注意", "确定要保存界面设置吗？")
        if confirm:
            try:
                # 菜单栏位置
                if self.radio_button_menu_location_left.isChecked():
                    self.setting_config['menuPosition'] = "Left"
                else:
                    self.setting_config['menuPosition'] = "Right"
                # 保存数据
                self.parent.save_setting_to_main(trigger_type=data_save_constant.TRIGGER_TYPE_SETTING_SCREEN, in_data=self.setting_config)
                self.close()
            except Exception as e:
                print(f"setting_screen push_button_submit_clicked 1 error: {str(e)}")
            return
        else:
            return

    def closeEvent(self, event):
        # 继续正常的关闭流程
        super().closeEvent(event)
