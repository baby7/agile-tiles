# coding:utf-8
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QTextEdit


class EnterTextEdit(QTextEdit):
    """自定义文本编辑框，支持回车发送消息，Shift+Enter换行"""
    returnPressed = Signal()

    def keyPressEvent(self, event: QKeyEvent):
        # 处理回车键事件
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # 检查是否同时按下了Shift键
            if event.modifiers() & Qt.ShiftModifier:
                # Shift+Enter：插入换行符
                self.insertPlainText("\n")
            else:
                # 普通回车：发送消息
                self.returnPressed.emit()
                event.accept()  # 阻止事件继续传播
        else:
            # 其他按键使用默认处理
            super().keyPressEvent(event)