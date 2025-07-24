import os
import traceback

from PySide6.QtCore import Qt


def save_settings(music_card):
    settings = {
        "playlists": music_card.playlist_data,
        "current_playlist": music_card.current_playlist,
        "current_song_index": music_card.current_song_index,
        "volume": int(music_card.audio_output.volume() * 100),
        "last_folder": music_card.last_folder
    }
    music_card.music_data.update(settings)

def load_settings(music_card):
    # 加载设置的具体实现
    try:
        data = music_card.music_data
        # 恢复歌单数据
        music_card.playlist_data = data.get("playlists", {})

        # 1. 如果没有歌单，创建默认歌单
        if not music_card.playlist_data:
            default_playlist = "默认歌单"
            music_card.playlist_data[default_playlist] = []
            music_card.current_playlist = default_playlist
            # 保存设置以确保下次启动时保留默认歌单
            save_settings(music_card)

        music_card.playlists.clear()
        music_card.playlists.addItems(music_card.playlist_data.keys())

        # 2. 如果没有当前歌单，将第一个歌单设为当前歌单
        current_playlist = data.get("current_playlist")
        if not current_playlist or current_playlist not in music_card.playlist_data:
            # 获取第一个歌单
            if music_card.playlist_data:
                first_playlist = next(iter(music_card.playlist_data))
                music_card.current_playlist = first_playlist
                current_playlist = first_playlist
                if hasattr(music_card, 'song_list_title_label'):
                    music_card.song_list_title_label.setText(first_playlist)

        if current_playlist in music_card.playlist_data:
            music_card.current_playlist = current_playlist
            music_card.title_label.setText(current_playlist)
            music_card.songs_list.clear()
            music_card.songs_list.addItems([os.path.basename(path) for path in music_card.playlist_data[current_playlist]])
            # 在歌单列表中选中当前歌单
            items = music_card.playlists.findItems(current_playlist, Qt.MatchExactly)
            if items:
                music_card.playlists.setCurrentItem(items[0])
                music_card.playlists.setCurrentRow(music_card.playlists.row(items[0]))
                if hasattr(music_card, 'song_list_title_label'):
                    music_card.song_list_title_label.setText(current_playlist)
        # 恢复播放状态
        music_card.current_song_index = data.get("current_song_index", -1)
        if 0 <= music_card.current_song_index < len(music_card.playlist_data.get(music_card.current_playlist, [])):
            music_card.songs_list.setCurrentRow(music_card.current_song_index)
        # 恢复播放模式
        music_card.current_mode_index = data.get("playback_mode", 0)
        music_card.update_mode_icon()
        # 恢复音量
        volume = data.get("volume", 100)
        music_card.audio_output.setVolume(volume / 100)
        music_card.update_volume(volume)
        # 恢复最后文件夹
        music_card.last_folder = data.get("last_folder", "")
        # 恢复上次播放的歌曲信息（不自动播放）
        last_played_song = data.get("last_played_song")
        if last_played_song and last_played_song in music_card.playlist_data.get(music_card.current_playlist, []):
            music_card.current_song_index = music_card.playlist_data[music_card.current_playlist].index(last_played_song)
            music_card.songs_list.setCurrentRow(music_card.current_song_index)
            music_card.update_song_info(last_played_song)
    except FileNotFoundError:
        traceback.print_exc()