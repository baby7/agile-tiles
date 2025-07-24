music_list_style = """
QListWidget {
  border-radius: 5px;
  border: none;
  background: transparent;
}
QListWidget::item {
  padding-left: 10px;
}
QListWidget::item:click {
  background: transparent;
}
QListWidget::item:hover {
  background-color: #e2e2e2;
}
QListWidget::item:selected {
  background-color: #4d4d4d;
  color: rgb(255, 255, 255);
  border-radius: 5px;
}
QListWidget::item:!alternate:!selected {
  background-color: rgba(100, 100, 100, 0.1);
  border-radius: 5px;
}
QScrollBar:vertical {
    border-width: 0px;
    border: none;
    background:rgba(179, 179, 179, 0);
    width:8px;
    margin: 0px 0px 0px 0px;
}
QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop: 0 #b3b3b3, stop: 0.5 #b3b3b3, stop:1 #b3b3b3);
    min-height: 20px;
    max-height: 20px;
    margin: 0px 0px 0px 0px;
    border-radius: 4px;
}
QScrollBar::add-line:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    stop: 0 rgba(179, 179, 179, 0), stop: 0.5 rgba(179, 179, 179, 0),  stop:1 rgba(179, 179, 179, 0));
    height: 0px;
    border: none;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    stop: 0  rgba(179, 179, 179, 0), stop: 0.5 rgba(179, 179, 179, 0),  stop:1 rgba(179, 179, 179, 0));
    height: 0 px;
    border: none;
    subcont"
    rol-position: top;
    subcontrol-origin: margin;
}
QScrollBar::sub-page:vertical {
    background: rgba(179, 179, 179, 0);
}

QScrollBar::add-page:vertical {
    background: rgba(179, 179, 179, 0);
}
"""

music_volume_style = """
QSlider {
    background-color: rgb(255, 255, 255);
    border-radius: 5px;
    padding: 5px;
    width: 20px;
}
QSlider::add-page:vertical {
    background-color: #00e1ff;
    width:5px;
    border-radius: 2px;
}
QSlider::sub-page:vertical {
    background-color: #b8b8b8;
    width:5px;
    border-radius: 2px;
}
QSlider::groove:vertical {
    background: transparent;
    width:6px;
}
QSlider::handle:vertical {
    height: 13px;
    width: 14px;
    margin: 0px -4px 0px -4px;
    border-radius: 7px;
    background: white;
    border: 1px solid black;
}"""

music_progress_style = """
QSlider {
    background: transparent
}
QSlider::groove:horizontal {
    background-color: #444444;
    height: 4px;
    border-radius: 2px;
}
QSlider::sub-page:horizontal {
    background-color: #666666;
    border-radius: 2px;
}
QSlider::add-page:horizontal {
    background-color: #333333;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background: #666666;
    width: 8px;      /* 竖条宽度 */
    height: 8px;    /* 竖条高度 */
    margin: -4px 0;  /* 垂直居中 */
    border-radius: 5px;
    border: 1px solid #888888;  /* 添加边框 */
}
"""