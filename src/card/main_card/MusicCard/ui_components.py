# File 2: ui_components.py
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                               QListWidget, QSlider, QWidget, QMenu)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize
import src.card.main_card.MusicCard.music_style as music_style
from src.module import dialog_module
from src.ui import image_util, style_util


def init_base_ui(music_card):
    # 基础界面
    music_card.base_widget = QWidget()
    music_card.base_layout = QVBoxLayout()
    music_card.base_layout.setContentsMargins(20, 10, 20, 40)

    # Top Bar
    top_layout = QHBoxLayout()
    music_card.playlist_button = _create_icon_button(music_card, "Music/music-list", 20)
    music_card.playlist_button.setText("歌单列表")
    music_card.playlist_button.clicked.connect(music_card.show_playlist)
    music_card.title_label = QLabel("未选择歌单", alignment=Qt.AlignCenter)
    music_card.song_list_button = _create_icon_button(music_card, "Music/music-one", 20)
    music_card.song_list_button.setText("歌曲列表")
    music_card.song_list_button.clicked.connect(music_card.show_song_list)
    top_layout.addWidget(music_card.playlist_button)
    top_layout.addWidget(music_card.title_label, alignment=Qt.AlignmentFlag.AlignCenter)
    top_layout.addWidget(music_card.song_list_button)
    music_card.base_layout.addLayout(top_layout)
    music_card.base_layout.addStretch()

    # Cover Art
    music_card.base_layout.addStretch()
    music_card.cover_label = QLabel()
    music_card.default_pixmap = QPixmap(":static/img/music/cover.png").scaled(
        270, 270, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    music_card.default_pixmap = image_util.create_rounded_pixmap(music_card.default_pixmap, 0.06)
    music_card.cover_label.setPixmap(music_card.default_pixmap)
    music_card.cover_label.setMinimumWidth(270)
    music_card.cover_label.setMinimumHeight(270)
    music_card.cover_label.setMaximumWidth(270)
    music_card.cover_label.setMaximumHeight(270)
    music_card.base_layout.addWidget(music_card.cover_label, alignment=Qt.AlignCenter)
    music_card.base_layout.addStretch()

    music_card.song_title = QLabel("歌曲标题", alignment=Qt.AlignmentFlag.AlignCenter)
    music_card.song_title.setStyleSheet("font-size: 18px;")
    music_card.base_layout.addWidget(music_card.song_title)
    music_card.artist = QLabel("演唱者", alignment=Qt.AlignmentFlag.AlignCenter)
    music_card.artist.setStyleSheet("font-size: 14px;")
    music_card.base_layout.addWidget(music_card.artist)
    music_card.base_layout.addStretch()

    # 播放控制模块
    _setup_progress_controls(music_card)

    music_card.base_widget.setLayout(music_card.base_layout)
    music_card.stacked_widget.addWidget(music_card.base_widget)

    # 背景图片
    music_card.background_label = QLabel(music_card.base_widget)
    music_card.background_label.setScaledContents(True)
    music_card.background_label.lower()


def _setup_progress_controls(music_card):
    music_card.progress_controls = QWidget()
    music_card.progress_controls_layout = QVBoxLayout()
    music_card.progress_controls.setLayout(music_card.progress_controls_layout)

    # 上面的两个时间
    time_layout = QHBoxLayout()
    music_card.current_time = QLabel("00:00")
    music_card.current_time.setStyleSheet("background: transparent")
    music_card.total_time = QLabel("00:00")
    music_card.total_time.setStyleSheet("background: transparent")
    time_layout.addWidget(music_card.current_time)
    time_layout.addStretch()
    time_layout.addWidget(music_card.total_time)

    # 中间的音乐进度条
    music_card.progress_slider = QSlider(Qt.Horizontal)
    music_card.progress_slider.setStyleSheet(music_style.music_progress_style)
    music_card.progress_slider.installEventFilter(music_card)
    music_card.progress_slider.setMinimumHeight(20)

    # 下面的五个控制按钮
    control_layout = QHBoxLayout()
    buttons = [
        ("Arrows/play-cycle", 20, music_card.toggle_playback_mode),
        ("Arrows/double-left", 35, music_card.prev_song),
        ("Music/play", 35, music_card.toggle_play_pause),
        ("Arrows/double-right", 35, music_card.next_song),
        ("Music/volume-notice", 20, music_card.adjust_volume)
    ]
    for icon, size, callback in buttons:
        btn = _create_icon_button(music_card, icon, size)
        btn.clicked.connect(callback)
        control_layout.addWidget(btn)
        music_card.button_list.append(btn)

    # 一起加到主布局中
    music_card.progress_controls_layout.addLayout(time_layout)
    music_card.progress_controls_layout.addWidget(music_card.progress_slider)
    music_card.progress_controls_layout.addLayout(control_layout)
    music_card.base_layout.addWidget(music_card.progress_controls)


def _create_icon_button(music_card, icon_name, size):
    btn = QPushButton()
    style_util.set_button_style(btn, icon_path=icon_name, is_dark=music_card.is_dark(), style_change=False)
    btn.setIconSize(QSize(size, size))
    btn.setMinimumHeight(size)
    btn.setStyleSheet("background-color: transparent; border: none;")
    return btn

# (完整实现需要包含歌单列表和歌曲列表的UI组件初始化)
def init_playlist_ui(music_card):
    # 创建歌单列表界面
    music_card.playlist_widget = QWidget()
    music_card.playlist_widget.setFixedSize(music_card.card.width(), music_card.card.height())
    music_card.playlist_layout = QVBoxLayout()
    music_card.playlist_layout.setContentsMargins(8, 8, 8, 8)  # 设置边距
    music_card.playlist_layout.setSpacing(4)
    # 顶部按钮布局
    music_card.close_playlist_button = _create_icon_button(music_card, "Edit/back", 20)
    music_card.close_playlist_button.setText("返回")
    music_card.close_playlist_button.clicked.connect(music_card.show_base)

    music_card.playlist_title_label = QLabel("歌单列表", alignment=Qt.AlignmentFlag.AlignCenter)

    music_card.edit_playlist_button = _create_icon_button(music_card, "Edit/edit", 20)
    music_card.edit_playlist_button.setText("编辑")
    music_card.edit_playlist_button.clicked.connect(lambda: edit_current_playlist(music_card))

    music_card.delete_playlist_button = _create_icon_button(music_card, "Edit/delete", 20)
    music_card.delete_playlist_button.setText("删除")
    music_card.delete_playlist_button.clicked.connect(lambda: delete_current_playlist(music_card))
    music_card.edit_playlist_button.setVisible(False)

    music_card.add_playlist_button = _create_icon_button(music_card, "Music/list-add", 20)
    music_card.add_playlist_button.setText("添加")
    music_card.add_playlist_button.clicked.connect(music_card.add_playlist)
    music_card.delete_playlist_button.setVisible(False)

    playlist_button_layout = QHBoxLayout()
    playlist_button_layout.addWidget(music_card.close_playlist_button)
    playlist_button_layout.addWidget(music_card.playlist_title_label)
    playlist_button_layout.addWidget(music_card.edit_playlist_button)
    playlist_button_layout.addWidget(music_card.delete_playlist_button)
    playlist_button_layout.addWidget(music_card.add_playlist_button)
    # 歌单列表
    music_card.playlists = QListWidget()
    music_card.playlists.itemSelectionChanged.connect(lambda: update_playlist_buttons(music_card))
    music_card.playlists.itemDoubleClicked.connect(music_card.select_playlist)
    # 设置右键菜单
    music_card.playlists.setContextMenuPolicy(Qt.CustomContextMenu)
    music_card.playlists.customContextMenuRequested.connect(lambda pos: show_playlist_context_menu(music_card, pos))
    music_card.playlist_layout.addLayout(playlist_button_layout)
    music_card.playlist_layout.addWidget(music_card.playlists)
    music_card.playlist_widget.setLayout(music_card.playlist_layout)
    music_card.stacked_widget.addWidget(music_card.playlist_widget)
    # 歌单列表样式
    music_card.playlists.setStyleSheet(music_style.music_list_style)
    music_card.playlists.setSpacing(2)  # 设置项间距


def update_playlist_buttons(music_card):
    selected = music_card.playlists.selectedItems()
    has_selection = len(selected) > 0

    # 同步当前歌单（可选）
    if has_selection:
        music_card.current_playlist = selected[0].text()

    music_card.edit_playlist_button.setVisible(has_selection)
    music_card.delete_playlist_button.setVisible(has_selection)


def show_playlist_context_menu(music_card, pos):
    item = music_card.playlists.itemAt(pos)
    if not item:
        return

    menu = QMenu()
    edit_action = menu.addAction("编辑歌单")
    delete_action = menu.addAction("删除歌单")

    # 获取当前歌单名称
    current_playlist = item.text()

    # 连接动作
    edit_action.triggered.connect(lambda: edit_playlist(music_card, current_playlist))
    delete_action.triggered.connect(lambda: delete_current_playlist(music_card))

    menu.exec_(music_card.playlists.mapToGlobal(pos))


def edit_playlist(music_card, old_name):
    # 未登录的判断
    music_card.main_object.show_login_tip()
    if music_card.main_object.current_user['username'] == "LocalUser":
        return
    new_name = dialog_module.box_input(music_card.main_object, "编辑歌单", "请输入歌单名称：", old_text=old_name)
    if new_name is None:
        return
    if new_name == "":
        dialog_module.box_information(music_card.main_object, "提示", "歌单名称不能为空！")
        return

    if new_name in music_card.playlist_data:
        dialog_module.box_information(music_card.main_object, "提示", "歌单名称已存在！")
        return

    # 更新数据结构
    music_card.playlist_data[new_name] = music_card.playlist_data.pop(old_name)
    if music_card.current_playlist == old_name:
        music_card.current_playlist = new_name

    # 更新列表项
    items = music_card.playlists.findItems(old_name, Qt.MatchExactly)
    if items:
        row = music_card.playlists.row(items[0])
        music_card.playlists.takeItem(row)
        music_card.playlists.insertItem(row, new_name)

    # 新增标题同步
    if music_card.current_playlist == new_name:
        music_card.title_label.setText(new_name)
        music_card.song_list_title_label.setText(new_name)

    music_card.save_settings()


def delete_playlist(music_card, name):
    confirm = dialog_module.box_acknowledgement(
        music_card.main_object, "确认删除", f"确定要删除歌单 {name} 吗？")

    if confirm:
        # 删除数据结构
        del music_card.playlist_data[name]

        # 更新当前歌单
        if music_card.current_playlist == name:
            music_card.current_playlist = None
            music_card.title_label.setText("未选择歌单")
            music_card.songs_list.clear()
            # 新增歌曲列表标题重置
            music_card.song_list_title_label.setText("未命名歌单")

        # 更新列表
        items = music_card.playlists.findItems(name, Qt.MatchExactly)
        if items:
            row = music_card.playlists.row(items[0])
            music_card.playlists.takeItem(row)

        music_card.save_settings()

def init_songlist_ui(music_card):
    # 创建歌曲列表界面
    music_card.song_list_widget = QWidget()
    music_card.song_list_widget.setFixedSize(music_card.card.width(), music_card.card.height())
    # 顶部按钮布局
    music_card.song_list_layout = QVBoxLayout()
    music_card.song_list_layout.setContentsMargins(8, 8, 8, 8)  # 设置边距
    music_card.song_list_layout.setSpacing(10)

    # 新增水平布局容纳导入按钮和关闭按钮
    music_card.close_song_list_button = _create_icon_button(music_card, "Edit/back", 20)
    music_card.close_song_list_button.setText("返回")
    music_card.close_song_list_button.clicked.connect(music_card.show_base)

    music_card.song_list_title_label = QLabel(
        music_card.current_playlist if music_card.current_playlist else "未命名歌单",
        alignment=Qt.AlignmentFlag.AlignCenter
    )
    music_card.song_list_title_label.setFixedWidth(200)

    music_card.delete_song_button = _create_icon_button(music_card, "Edit/delete", 20)
    music_card.delete_song_button.setText("删除")
    music_card.delete_song_button.clicked.connect(lambda: delete_selected_song(music_card))
    music_card.delete_song_button.setVisible(False)

    music_card.import_button = _create_icon_button(music_card, "Arrows/afferent-three", 20)
    music_card.import_button.setText("导入歌曲")
    music_card.import_button.clicked.connect(music_card.import_music)

    songlist_button_layout = QHBoxLayout()
    songlist_button_layout.addWidget(music_card.close_song_list_button)
    songlist_button_layout.addWidget(music_card.song_list_title_label, alignment=Qt.AlignmentFlag.AlignCenter)
    songlist_button_layout.addWidget(music_card.delete_song_button)
    songlist_button_layout.addWidget(music_card.import_button)
    # 歌曲列表
    music_card.songs_list = QListWidget()
    music_card.songs_list.itemSelectionChanged.connect(lambda: update_song_delete_button(music_card))
    music_card.songs_list.itemDoubleClicked.connect(music_card.play_song)
    # 设置右键菜单
    music_card.songs_list.setContextMenuPolicy(Qt.CustomContextMenu)
    music_card.songs_list.customContextMenuRequested.connect(lambda pos: show_song_context_menu(music_card, pos))
    music_card.song_list_layout.addLayout(songlist_button_layout)
    music_card.song_list_layout.addWidget(music_card.songs_list)
    music_card.song_list_widget.setLayout(music_card.song_list_layout)
    music_card.stacked_widget.addWidget(music_card.song_list_widget)
    # 歌曲列表样式
    music_card.songs_list.setStyleSheet(music_style.music_list_style)
    music_card.songs_list.setSpacing(1)  # 设置项间距

def update_song_delete_button(music_card):
    has_selection = len(music_card.songs_list.selectedItems()) > 0
    music_card.delete_song_button.setVisible(has_selection)

def delete_selected_song(music_card):
    selected_items = music_card.songs_list.selectedItems()
    if not selected_items:
        return
    delete_song(music_card, selected_items[0])


def show_song_context_menu(music_card, pos):
    item = music_card.songs_list.itemAt(pos)
    if not item:
        return

    menu = QMenu()
    delete_action = menu.addAction("删除歌曲")

    # 连接删除动作
    delete_action.triggered.connect(lambda: delete_song(music_card, item))

    menu.exec_(music_card.songs_list.mapToGlobal(pos))


def delete_song(music_card, item):
    confirm = dialog_module.box_acknowledgement(
        music_card.main_object, "确认删除", "确定要从歌单中移除这首歌曲吗？")

    if not confirm:
        return

    # 获取当前歌曲信息
    song_name = item.text()
    row = music_card.songs_list.row(item)

    # 更新数据结构
    if music_card.current_playlist in music_card.playlist_data:
        del music_card.playlist_data[music_card.current_playlist][row]

        # 更新当前歌曲索引
        if music_card.current_song_index >= row:
            music_card.current_song_index -= 1

        # 更新列表显示
        music_card.songs_list.takeItem(row)
        music_card.save_settings()

def init_other_ui(music_card):
    # 设置按钮样式
    button_style = """
    QPushButton { border-radius: 10px; background-color: transparent; }
    QPushButton:hover { background-color: rgba(0, 0, 0, 0.1); }
    QPushButton:pressed { background-color: rgba(0, 0, 0, 0.2); }
    """
    base_btn_list = music_card.button_list
    for button in base_btn_list:
        button.setStyleSheet(button_style)
    top_button_style = """
    QPushButton { border-radius: 10px; background-color: transparent; border: 1px solid #888888; padding-left: 2px; padding-right: 2px;}
    QPushButton:hover { background-color: rgba(0, 0, 0, 0.1); }
    QPushButton:pressed { background-color: rgba(0, 0, 0, 0.2); }
    """
    base_top_btn_list = [music_card.playlist_button, music_card.song_list_button, music_card.close_song_list_button,
                     music_card.delete_song_button, music_card.add_playlist_button, music_card.close_playlist_button,
                     music_card.edit_playlist_button, music_card.delete_playlist_button, music_card.import_button]
    for button in base_top_btn_list:
        button.setStyleSheet(top_button_style)

def edit_current_playlist(music_card):
    if not music_card.current_playlist:
        dialog_module.box_information(music_card.main_object, "提示", "请先选择歌单")
        return
    edit_playlist(music_card, music_card.current_playlist)


def delete_current_playlist(music_card):
    # 未登录的判断
    music_card.main_object.show_login_tip()
    if music_card.main_object.current_user['username'] == "LocalUser":
        return
    # 获取选中的歌单项
    selected_items = music_card.playlists.selectedItems()
    if not selected_items:
        dialog_module.box_information(music_card.main_object, "提示", "请先选择要删除的歌单")
        return
    # 获取选中歌单名称
    playlist_name = selected_items[0].text()
    # 原有删除逻辑（替换最后一行参数为playlist_name）
    confirm = dialog_module.box_acknowledgement(
        music_card.main_object, "确认删除", f"确定要删除歌单 {playlist_name} 吗？")
    if confirm:
        # 删除数据结构
        del music_card.playlist_data[playlist_name]
        # 更新当前歌单
        if music_card.current_playlist == playlist_name:
            music_card.current_playlist = None
            music_card.title_label.setText("未选择歌单")
            music_card.songs_list.clear()
            music_card.song_list_title_label.setText("未命名歌单")
        # 更新列表
        items = music_card.playlists.findItems(playlist_name, Qt.MatchExactly)
        if items:
            row = music_card.playlists.row(items[0])
            music_card.playlists.takeItem(row)
        music_card.save_settings()
