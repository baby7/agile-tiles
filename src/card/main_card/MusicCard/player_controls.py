import os
import random
import traceback

from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl, QCoreApplication, QSize

from src.ui import style_util


def init_player(music_card):
    music_card.player = QMediaPlayer()
    music_card.audio_output = QAudioOutput()
    music_card.player.setAudioOutput(music_card.audio_output)

def setup_player_signals(music_card):
    music_card.player.durationChanged.connect(music_card.update_duration)
    music_card.player.positionChanged.connect(music_card.update_progress)
    music_card.player.mediaStatusChanged.connect(music_card.on_media_status_changed)
    music_card.player.errorOccurred.connect(music_card.handle_player_error)

def play_song(music_card, item):
    # 播放歌曲的具体实现
    try:
        row = music_card.songs_list.row(item)
        music_card.current_song_index = row
        song_path = item.text()
        play_pause_button = music_card.button_list[2]
        for index, song in enumerate(music_card.playlist_data[music_card.current_playlist]):
            if os.path.basename(song) == song_path:
                music_card.current_song_index = index
                if music_card.player.isPlaying():
                    music_card.player.stop()
                QCoreApplication.processEvents()
                music_card.player.setSource(QUrl.fromLocalFile(song))
                music_card.player.play()
                style_util.set_button_style(play_pause_button, icon_path="Music/pause-one", is_dark=music_card.is_dark(),
                                            style_change=False)
                music_card.update_song_info(song)
                break
        # 重置时间显示
        music_card.current_time.setText("00:00")
        music_card.total_time.setText("00:00")
        music_card.playlist_widget.hide()  # 关闭歌单界面
        music_card.song_list_widget.hide()  # 关闭歌曲列表界面
        music_card.show_base()  # 显示基础界面
        music_card.save_settings()
    except Exception as e:
        traceback.print_exc()

def toggle_playback_mode(music_card):
    # 切换播放模式
    music_card.current_mode_index = (music_card.current_mode_index + 1) % len(music_card.playback_modes)
    music_card.update_mode_icon()

def prev_song(music_card):
    try:
        if music_card.current_playlist is None or music_card.current_song_index < 0:
            return
        if music_card.current_song_index > 0:
            music_card.current_song_index -= 1
        else:
            music_card.current_song_index = len(music_card.playlist_data[music_card.current_playlist]) - 1
        music_card.play_current_song()
        music_card.save_settings()
    except Exception as e:
        traceback.print_exc()

def next_song(music_card):
    try:
        if music_card.current_playlist is None or music_card.current_song_index < 0:
            return
        if music_card.current_mode_index == 1:  # 单曲循环
            music_card.current_song_index = music_card.current_song_index
        elif music_card.current_mode_index == 2:  # 随机播放
            new_index = music_card.current_song_index
            while new_index == music_card.current_song_index:
                new_index = random.randint(0, len(music_card.playlist_data[music_card.current_playlist]) - 1)
            music_card.current_song_index = new_index
        else:  # 歌单循环
            if music_card.current_song_index < len(music_card.playlist_data[music_card.current_playlist]) - 1:
                music_card.current_song_index += 1
            else:
                music_card.current_song_index = 0
        music_card.play_current_song()
        music_card.save_settings()
    except Exception as e:
        traceback.print_exc()

def toggle_play_pause(music_card):
    if music_card.player.source().isEmpty():
        if music_card.current_playlist and 0 <= music_card.current_song_index < len(
                music_card.playlist_data.get(music_card.current_playlist, [])):
            music_card.play_current_song()
        else:
            return
    play_pause_button = music_card.button_list[2]
    if music_card.player.playbackState() == QMediaPlayer.PlayingState:
        music_card.player.pause()
        style_util.set_button_style(play_pause_button, icon_path="Music/play", is_dark=music_card.is_dark(), style_change=False)
    else:
        music_card.player.play()
        style_util.set_button_style(play_pause_button, icon_path="Music/pause-one", is_dark=music_card.is_dark(), style_change=False)

def play_current_song(music_card):
    if music_card.current_playlist is not None and music_card.current_song_index >= 0:
        song_path = music_card.playlist_data[music_card.current_playlist][music_card.current_song_index]
        if music_card.player.isPlaying():
            music_card.player.stop()
        QCoreApplication.processEvents()
        music_card.player.setSource(QUrl.fromLocalFile(song_path))
        music_card.player.play()
        play_pause_button = music_card.button_list[2]
        style_util.set_button_style(play_pause_button, icon_path="Music/pause-one", is_dark=music_card.is_dark(), style_change=False)
        music_card.update_song_info(song_path)
        # 新增：设置当前选中行
        music_card.songs_list.setCurrentRow(music_card.current_song_index)

def update_mode_icon(music_card):
    is_dark = music_card.is_dark()
    # 播放模式图标
    mode = music_card.playback_modes[music_card.current_mode_index]
    mode_button = music_card.button_list[0]
    if mode == 'playlist':
        style_util.set_button_style(mode_button, icon_path="Arrows/play-cycle", is_dark=is_dark, style_change=False)
    elif mode == 'single':
        style_util.set_button_style(mode_button, icon_path="Arrows/play-once", is_dark=is_dark, style_change=False)
    elif mode == 'random':
        style_util.set_button_style(mode_button, icon_path="Arrows/shuffle-one", is_dark=is_dark, style_change=False)
    # 播放/暂停图标
    play_pause_button = music_card.button_list[2]
    if music_card.player.playbackState() == QMediaPlayer.PlayingState:
        style_util.set_button_style(play_pause_button, icon_path="Music/pause-one", is_dark=is_dark, style_change=False)
    else:
        style_util.set_button_style(play_pause_button, icon_path="Music/play", is_dark=is_dark, style_change=False)
    # 上一首、下一首图标
    prev_button = music_card.button_list[1]
    next_button = music_card.button_list[3]
    style_util.set_button_style(prev_button, icon_path="Arrows/double-left", is_dark=is_dark, style_change=False)
    style_util.set_button_style(next_button, icon_path="Arrows/double-right", is_dark=is_dark, style_change=False)
    # 主页顶部图标
    style_util.set_button_style(music_card.playlist_button, icon_path="Music/music-list", is_dark=is_dark, style_change=False)
    style_util.set_button_style(music_card.song_list_button, icon_path="Music/music-one", is_dark=is_dark, style_change=False)
    # 歌单页顶部图标
    style_util.set_button_style(music_card.close_playlist_button, icon_path="Edit/next", is_dark=is_dark, style_change=False)
    style_util.set_button_style(music_card.edit_playlist_button, icon_path="Edit/edit", is_dark=is_dark, style_change=False)
    style_util.set_button_style(music_card.delete_playlist_button, icon_path="Edit/delete", is_dark=is_dark, style_change=False)
    style_util.set_button_style(music_card.add_playlist_button, icon_path="Music/list-add", is_dark=is_dark, style_change=False)
    # 歌曲列表页顶部图标
    style_util.set_button_style(music_card.close_song_list_button, icon_path="Edit/return", is_dark=is_dark, style_change=False)
    style_util.set_button_style(music_card.delete_song_button, icon_path="Edit/delete", is_dark=is_dark, style_change=False)
    style_util.set_button_style(music_card.import_button, icon_path="Arrows/afferent-three", is_dark=is_dark, style_change=False)
    # 歌曲控制模块背景
    music_card.progress_controls.setStyleSheet("background: transparent;")
    # if music_card.is_dark:
    #     music_card.progress_controls.setStyleSheet("border-size: 40; background-color: rgba(255, 255, 255, 0.2);")
    # else:
    #     music_card.progress_controls.setStyleSheet("border-size: 40; background-color: rgba(0, 0, 0, 0.6);")
