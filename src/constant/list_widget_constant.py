scroll_bar_style = """
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
    margin: 0 0px 0 0px;
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
    subcontrol-position: top;
    subcontrol-origin: margin;
}
QScrollBar::sub-page:vertical {
    background: rgba(179, 179, 179, 0);
}

QScrollBar::add-page:vertical {
    background: rgba(179, 179, 179, 0);
}
"""
