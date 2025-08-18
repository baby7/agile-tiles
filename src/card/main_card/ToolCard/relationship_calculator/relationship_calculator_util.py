from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QPushButton, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt

from src.card.main_card.ToolCard.relationship_calculator.RelationshipCalculator import RelationshipCalculator
from src.component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
from src.ui import style_util


class RelationshipCalculatorApp(AgileTilesAcrylicWindow):
    def __init__(self, parent=None, use_parent=None, title=None, content=None):
        super().__init__(parent=parent, is_dark=use_parent.is_dark, form_theme_mode=use_parent.form_theme_mode,
                         form_theme_transparency=use_parent.form_theme_transparency)
        # 初始化
        self.parent = parent
        self.use_parent = use_parent
        # 设置标题栏
        self.setWindowTitle(title)  # 设置到标题栏
        self.titleBar.minBtn.close()
        self.titleBar.maxBtn.close()
        self.setMinimumSize(600, 700)
        # 设置链接
        self.standard_title_bar.setLink("https://github.com/mumuy/relationship")
        # 存储关系链的列表（使用内部表示）
        self.relationship_chain = []
        # 初始化界面
        self.init_ui()
        # 设置样式
        style_util.set_dialog_control_style(self, self.is_dark)

    def init_ui(self):
        # 主部件和布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        self.widget_base.setLayout(main_layout)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 输入部分
        input_layout = QVBoxLayout()
        input_layout.setSpacing(10)

        input_label = QLabel("称呼方式(我称呼对方)：")
        input_label.setStyleSheet("background: transparent;")
        input_layout.addWidget(input_label)

        self.input_text = QTextEdit()
        self.input_text.setMinimumHeight(80)
        self.input_text.setReadOnly(True)
        input_layout.addWidget(self.input_text)

        # 关系按钮
        relation_buttons = self.create_relation_buttons()
        input_layout.addLayout(relation_buttons)

        # 操作按钮
        action_buttons = self.create_action_buttons()
        input_layout.addLayout(action_buttons)

        main_layout.addLayout(input_layout)

        # 分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #d1d5db;")
        main_layout.addWidget(separator)

        # 结果部分
        result_layout = QVBoxLayout()
        result_layout.setSpacing(10)

        result_label = QLabel("计算结果：")
        result_label.setStyleSheet("background: transparent;")
        result_layout.addWidget(result_label)

        self.result_text = QTextEdit()
        self.result_text.setMinimumHeight(100)
        self.result_text.setReadOnly(True)
        self.result_text.setObjectName("resultBox")
        result_layout.addWidget(self.result_text)

        main_layout.addLayout(result_layout)

        # 底部说明
        footer_label = QLabel("提示：点击关系按钮构建关系链，使用操作按钮进行管理")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("background: transparent; color: #7f8c8d; font-size: 14px; padding-top: 15px;")
        main_layout.addWidget(footer_label)

    def create_relation_buttons(self):
        relations = ["父", "母", "夫", "妻", "兄", "弟", "姐", "妹", "子", "女"]

        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        for rel in relations:
            btn = QPushButton(rel)
            btn.setObjectName("relationButton")
            btn.setFixedHeight(45)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(lambda checked=False, r=rel: self.add_relation(r))
            button_layout.addWidget(btn)

        return button_layout

    def create_action_buttons(self):
        actions = ["回退", "清空", "计算"]

        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        for action in actions:
            btn = QPushButton(action)
            btn.setObjectName("specialButtons")
            btn.setFixedHeight(45)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

            if action == "回退":
                btn.clicked.connect(self.undo_relation)
            elif action == "清空":
                btn.clicked.connect(self.clear_relations)
            elif action == "计算":
                btn.clicked.connect(self.calculate_relationship)

            button_layout.addWidget(btn)

        return button_layout

    def add_relation(self, relation):
        # 直接添加关系符号
        self.relationship_chain.append(relation)

        # 更新输入框显示
        self.update_input_display()

    def undo_relation(self):
        if not self.relationship_chain:
            return

        # 移除最后一个关系
        self.relationship_chain.pop()

        # 更新输入框显示
        self.update_input_display()

    def update_input_display(self):
        """将内部关系链转换为友好的显示文本"""
        if not self.relationship_chain:
            self.input_text.clear()
            return

        # 映射关系符号到友好名称
        relation_map = {
            "父": "爸爸",
            "母": "妈妈",
            "夫": "丈夫",
            "妻": "妻子",
            "兄": "哥哥",
            "弟": "弟弟",
            "姐": "姐姐",
            "妹": "妹妹",
            "子": "儿子",
            "女": "女儿"
        }

        # 转换关系链
        display_chain = [relation_map.get(rel, rel) for rel in self.relationship_chain]
        display_text = "的".join(display_chain)
        self.input_text.setPlainText(display_text)

    def clear_relations(self):
        self.relationship_chain = []
        self.input_text.clear()
        self.result_text.clear()

    def calculate_relationship(self):
        if not self.relationship_chain:
            self.result_text.setPlainText("请输入关系链")
            return

        # 创建关系字符串（使用内部表示）
        relation_str = "的".join(self.relationship_chain)

        # 这里应该导入您的RelationshipCalculator
        calculator = RelationshipCalculator()
        result = calculator.relationship({"text": relation_str})

        # 为了演示目的，我们创建一个模拟结果
        # 实际使用时请取消上面的注释并删除下面的模拟代码
        # result = self.mock_relationship_calculation(relation_str)

        # 显示结果
        if result:
            if len(result) > 1:
                display_result = " 或 ".join(result)
            else:
                display_result = result[0]

            # 获取友好显示的关系链
            relation_map = {
                "父": "爸爸",
                "母": "妈妈",
                "夫": "丈夫",
                "妻": "妻子",
                "兄": "哥哥",
                "弟": "弟弟",
                "姐": "姐姐",
                "妹": "妹妹",
                "子": "儿子",
                "女": "女儿"
            }
            display_chain = [relation_map.get(rel, rel) for rel in self.relationship_chain]
            display_text = "的".join(display_chain)

            self.result_text.setPlainText(f"【{display_text}】的称呼是：\n{display_result}")
        else:
            self.result_text.setPlainText("无法确定关系")

    def mock_relationship_calculation(self, relation_str):
        """模拟关系计算器的功能，实际使用时应该替换为真实计算"""
        # 这是一个简化的模拟实现
        relations = {
            "父": ["父亲"],
            "母": ["母亲"],
            "父的父": ["爷爷", "祖父"],
            "父的母": ["奶奶", "祖母"],
            "母的父": ["外公", "姥爷"],
            "母的母": ["外婆", "姥姥"],
            "父的兄": ["伯父"],
            "父的弟": ["叔叔"],
            "父的姐": ["姑妈"],
            "父的妹": ["姑姑"],
            "母的兄": ["舅舅"],
            "母的弟": ["舅舅"],
            "母的姐": ["姨妈"],
            "母的妹": ["姨妈"],
            "子的子": ["孙子"],
            "子的女": ["孙女"],
            "女的子": ["外孙"],
            "女的女": ["外孙女"],
            "兄的子": ["侄子"],
            "兄的女": ["侄女"],
            "弟的子": ["侄子"],
            "弟的女": ["侄女"],
            "姐的子": ["外甥"],
            "姐的女": ["外甥女"],
            "妹的子": ["外甥"],
            "妹的女": ["外甥女"],
            "父的父的父": ["曾祖父"],
            "父的父的母": ["曾祖母"],
            "妻的父": ["岳父"],
            "妻的母": ["岳母"],
            "夫的父": ["公公"],
            "夫的母": ["婆婆"],
        }

        # 返回匹配的关系，如果没有则返回未知
        return relations.get(relation_str, ["未知关系"])


def show_relationship_calculator_dialog(main_object, title, content):
    """显示记仇生成器对话框"""
    dialog = RelationshipCalculatorApp(None, main_object, title, content)
    dialog.refresh_geometry(main_object.toolkit.resolution_util.get_screen(main_object))
    dialog.show()
    return dialog