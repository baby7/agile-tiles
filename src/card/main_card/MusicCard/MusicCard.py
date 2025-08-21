import os

from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtWidgets import QDialog, QSlider, QVBoxLayout, QStackedWidget, QFileDialog
from PySide6.QtCore import Qt, QRect, QPoint
from src.card.MainCardManager.MainCard import MainCard
from src.constant import data_save_constant
from src.module.Box import message_box_util

from . import music_style, music_analysis
from .ui_components import init_base_ui, init_playlist_ui, init_songlist_ui, init_other_ui, delete_current_playlist
from .player_controls import (init_player, setup_player_signals, toggle_playback_mode, play_song, prev_song, next_song,
                              play_current_song, toggle_play_pause, update_mode_icon)
from .settings_manager import save_settings, load_settings
from .music_utils import format_time, handle_slider_event


class MusicCard(MainCard):
    title = "音乐"
    name = "MusicCard"
    support_size_list = ["Big"]
    # 控件
    button_list = []
    progress_slider = None
    audio_output = None
    total_time = None
    songs_list = None
    player = None
    song_list_widget = None
    song_list_layout = None
    playlist_widget = None
    playlist_layout = None
    base_widget = None
    base_layout = None
    current_time = None
    playlists = None
    title_label = None
    song_list_title_label = None

    def __init__(self, main_object=None, parent=None, theme=None, card=None, cache=None, data=None,
                 toolkit=None, logger=None, save_data_func=None):
        super().__init__(main_object=main_object, parent=parent, theme=theme, card=card, cache=cache, data=data,
                         toolkit=toolkit, logger=logger, save_data_func=save_data_func)
        self.loading_ok = False
        self.music_data = self.data.setdefault(self.hardware_id, {})
        self.last_folder = ""
        self.playlist_data = {}
        self.current_playlist = None
        self.current_song_index = -1
        self.playback_modes = ['playlist', 'single', 'random']
        self.current_mode_index = 0
        self.is_dragging = False
        self.default_pixmap = None
        self.button_list = []

    def clear(self):
        try:
            self.stacked_widget.setVisible(False)
            self.stacked_widget.deleteLater()
            # 基础
            self.base_widget.setVisible(False)
            self.base_widget.deleteLater()
            self.base_layout.setParent(None)
            self.base_layout.deleteLater()
            # 歌单列表
            self.playlist_widget.setVisible(False)
            self.playlist_widget.deleteLater()
            self.playlist_layout.setParent(None)
            self.playlist_layout.deleteLater()
            # 歌曲列表
            self.song_list_widget.setVisible(False)
            self.song_list_widget.deleteLater()
            self.song_list_layout.setParent(None)
            self.song_list_layout.deleteLater()
        except Exception as e:
            print(e)
        # 其他
        try:
            self.audio_output.deleteLater()
            self.player.deleteLater()
        except Exception as e:
            self.logger.card_error("音乐", "播放器销毁失败,错误信息:{}".format(e))
        super().clear()

    def init_ui(self):
        super().init_ui()
        self.stacked_widget = self._create_stacked_widget()
        init_base_ui(self)
        init_playlist_ui(self)
        init_songlist_ui(self)
        init_other_ui(self)
        init_player(self)
        setup_player_signals(self)
        load_settings(self)
        # 新增：检查并创建默认歌单
        if not self.playlist_data or len(self.playlist_data) == 0:
            self.add_default_playlist()
        # 新增：如果没有当前歌单，设置第一个歌单为当前歌单
        if not self.current_playlist and self.playlist_data:
            self.set_first_playlist_as_current()
        self.loading_ok = True

    def update_data(self, data=None):
        """
        更新持久数据事件
        """
        if self.data == data:
            return
        # 重新初始化配置
        self.data = data
        # 理论上更新时，更新的是其他主机的音乐数据，不需要更改此主机的音乐数据，由于直接更改可能导致正在播放的音乐出现问题，所以这里不处理
        # self.music_data = self.data.setdefault(self.hardware_id, {})

    # 新增方法：创建默认歌单
    def add_default_playlist(self):
        """添加默认歌单"""
        playlist_name = "默认歌单"
        self.playlists.addItem(playlist_name)
        self.playlist_data[playlist_name] = []
        self.current_playlist = playlist_name
        self.title_label.setText(playlist_name)
        if hasattr(self, 'song_list_title_label'):
            self.song_list_title_label.setText(playlist_name)
        self.save_settings(real_time_storage=False)

    # 新增方法：设置第一个歌单为当前歌单
    def set_first_playlist_as_current(self):
        """将第一个歌单设为当前歌单"""
        first_playlist_name = next(iter(self.playlist_data.keys()))
        self.current_playlist = first_playlist_name
        self.title_label.setText(first_playlist_name)
        if hasattr(self, 'song_list_title_label'):
            self.song_list_title_label.setText(first_playlist_name)
        # 更新歌曲列表显示
        self.songs_list.clear()
        if self.current_playlist in self.playlist_data:
            self.songs_list.addItems(
                [os.path.basename(path) for path in self.playlist_data[self.current_playlist]]
            )
        # 在歌单列表中选中第一个歌单
        items = self.playlists.findItems(first_playlist_name, Qt.MatchExactly)
        if items:
            self.playlists.setCurrentItem(items[0])

    def select_playlist(self, item):
        self.current_playlist = item.text()
        self.title_label.setText(self.current_playlist)
        # 新增以下两行
        if self.song_list_title_label:  # 确保UI组件已初始化
            self.song_list_title_label.setText(self.current_playlist)
        self.songs_list.clear()
        if self.current_playlist in self.playlist_data:
            self.songs_list.addItems(
                [os.path.basename(path) for path in self.playlist_data[self.current_playlist]]  # 只显示文件名
            )
            self.current_song_index = -1
        self.stacked_widget.setCurrentWidget(self.song_list_widget)  # 直接跳转到歌曲列表

    def add_playlist(self):
        song_list = message_box_util.box_input(self.main_object, "新增歌单", "请输入歌单名称：")
        if song_list is None:
            return
        if song_list == "":
            message_box_util.box_information(self.main_object, "提示", "歌单名称不能为空！")
            return
        self.playlists.addItem(song_list)
        self.playlist_data[song_list] = []
        # 新增自动显示新歌单
        self.current_playlist = song_list
        self.title_label.setText(song_list)
        self.song_list_title_label.setText(song_list)
        self.save_settings()

    def import_music(self):
        if self.playlist_data is None or self.playlist_data == {}:
            message_box_util.box_information(self.main_object, "告警", f"当前无歌单，请先创建歌单！")
            return
        folder_path = QFileDialog.getExistingDirectory(self.card, "选择音乐文件夹", self.last_folder)
        if not folder_path:
            return
        self.last_folder = folder_path
        supported_formats = (".mp3", ".wav", ".ogg", ".flac")
        for file in os.listdir(folder_path):
            if not file.lower().endswith(supported_formats):
                continue
            full_path = os.path.join(folder_path, file)
            self.songs_list.addItem(file)
            self.playlist_data[self.current_playlist].append(full_path)
        self.save_settings()

    def update_song_info(self, song_path):
        # 获取歌曲信息并显示
        song_title, artist, cover_pixmap = music_analysis.get_music_info(song_path, self.cover_label)
        self.song_title.setText(song_title)
        self.artist.setText(artist)
        self.cover_label.setPixmap(cover_pixmap if cover_pixmap else self.default_pixmap)

    def _create_stacked_widget(self):
        widget = QStackedWidget(self.card)
        widget.setGeometry(QRect(0, 0, self.card.width(), self.card.height()))
        widget.setStyleSheet("background-color:transparent;")
        return widget

    def on_media_status_changed(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.next_song()

    def handle_player_error(self, error):
        error_msg = self.player.errorString()
        with open("error.log", "a") as f:
            f.write(f"播放器错误: {error} - {error_msg}\n")

    def seek_position(self, position):
        """跳转到指定播放位置"""
        try:
            self.player.setPosition(position)
        except Exception as e:
            print(f"Error: {e}")

    def update_playlist_display(self):
        """更新歌单列表显示"""
        self.playlists.clear()
        self.playlists.addItems(self.playlist_data.keys())

    def update_song_list_display(self):
        """更新歌曲列表显示"""
        self.songs_list.clear()
        if self.current_playlist in self.playlist_data:
            self.songs_list.addItems(
                [os.path.basename(p) for p in self.playlist_data[self.current_playlist]]
            )

    # UI Navigation
    def show_base(self):
        self.stacked_widget.setCurrentWidget(self.base_widget)

    def show_playlist(self):
        self.stacked_widget.setCurrentWidget(self.playlist_widget)

    def show_song_list(self):
        self.stacked_widget.setCurrentWidget(self.song_list_widget)

    # Progress Handling
    def update_progress(self, position):
        if not self.progress_slider.isSliderDown():
            self.progress_slider.setValue(position)
        self.update_time_display(position)

    def update_time_display(self, position):
        """更新当前播放时间显示"""
        self.current_time.setText(format_time(position))

    def update_duration(self, duration):
        self.progress_slider.setRange(0, duration)
        self.total_time.setText(format_time(duration))

    # Event Handling
    def eventFilter(self, obj, event):
        return handle_slider_event(obj, event, self)

    # Theme Handling
    def refresh_theme(self):
        if not super().refresh_theme():
            return False
        self.update_mode_icon()
        self.update_volume(int(self.audio_output.volume() * 100))
        # Update button icons based on theme
        return True

    def adjust_volume(self):
        """调整音量的方法"""
        # 创建或复用音量对话框
        if not hasattr(self, 'volume_dialog'):
            self.volume_dialog = QDialog(self.stacked_widget)
            self.volume_dialog.setAttribute(Qt.WA_TranslucentBackground)
            self.volume_dialog.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
            self.volume_dialog.setFixedSize(40, 120)
            self.volume_dialog.setStyleSheet("background-color: transparent; border: none;")
            self.volume_dialog.setAttribute(Qt.WA_TranslucentBackground)

            # 创建垂直滑块
            self.volume_slider = QSlider(Qt.Orientation.Vertical)
            self.volume_slider.setRange(0, 100)
            self.volume_slider.setFixedSize(20, 100)
            self.volume_slider.setStyleSheet(music_style.music_volume_style)

            # 布局设置
            layout = QVBoxLayout(self.volume_dialog)
            layout.addWidget(self.volume_slider)

        # 设置滑块初始值
        self.volume_slider.setValue(int(self.audio_output.volume() * 100))
        self.volume_slider.valueChanged.connect(
            lambda value: (self.audio_output.setVolume(value / 100), self.update_volume(value))
        )

        # 定位对话框到音量按钮附近
        volume_button = self.button_list[4]
        button_global_pos = volume_button.mapToGlobal(QPoint(0, 0))
        dialog_x = button_global_pos.x() - self.volume_dialog.width() // 2 + volume_button.width() // 2
        dialog_y = button_global_pos.y() - self.volume_dialog.height()
        self.volume_dialog.move(dialog_x, dialog_y)

        self.volume_dialog.exec()

    # Player Controls
    def toggle_play_pause(self):
        toggle_play_pause(self)

    def toggle_playback_mode(self):
        toggle_playback_mode(self)

    def play_song(self, item):
        play_song(self, item)

    def prev_song(self):
        prev_song(self)

    def next_song(self):
        next_song(self)

    def play_current_song(self):
        play_current_song(self)

    def update_mode_icon(self):
        update_mode_icon(self)

    def update_volume(self, volume):
        """根据音量值更新音量"""
        volume = int(volume)
        if volume == 0:
            icon_name = "Music/volume-mute"
        elif volume <= 50:
            icon_name = "Music/volume-small"
        else:
            icon_name = "Music/volume-notice"
        volume_button = self.button_list[4]
        volume_button.setIcon(self.get_icon_park_path(icon_name))
        if self.loading_ok:
            self.save_settings()

    def save_settings(self, real_time_storage=True):
        print("保存设置")
        # 更新设置
        save_settings(self)
        # 保存数据
        self.save_data_func(need_upload=real_time_storage,
                            in_data=self.data,
                            card_name=self.name,
                            data_type=data_save_constant.DATA_TYPE_ENDURING)

    def delete_current_playlist(self):
        delete_current_playlist(self)

    def hide_form(self):
        if hasattr(self, 'volume_dialog') and self.volume_dialog.isVisible():
            self.volume_dialog.close()
