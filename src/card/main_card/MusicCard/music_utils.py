# File 5: utils.py
from PySide6.QtCore import QEvent
from PySide6.QtWidgets import QStyle, QStyleOptionSlider

def format_time(milliseconds):
    seconds = milliseconds // 1000
    return f"{seconds//60:02d}:{seconds%60:02d}"

def handle_slider_event(obj, event, music_card):
    if obj != music_card.progress_slider or event.type() != QEvent.MouseButtonPress:
        return False
    style_option = QStyleOptionSlider()
    music_card.progress_slider.initStyleOption(style_option)
    groove_rect = music_card.progress_slider.style().subControlRect(
        QStyle.CC_Slider, style_option, QStyle.SC_SliderGroove)
    handle_rect = music_card.progress_slider.style().subControlRect(
        QStyle.CC_Slider, style_option, QStyle.SC_SliderHandle)
    local_pos = event.pos()
    if groove_rect.contains(local_pos) and not handle_rect.contains(local_pos):
        new_position = QStyle.sliderValueFromPosition(
            music_card.progress_slider.minimum(),
            music_card.progress_slider.maximum(),
            local_pos.x() - groove_rect.x(),
            groove_rect.width()
        )
        music_card.progress_slider.setValue(new_position)
        music_card.seek_position(new_position)
        return True
    return False