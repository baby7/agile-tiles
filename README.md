灵卡面板
 
"""
生成exe的命令：
pyinstaller -F -w -i img/icon/icon.ico -n 灵卡面板V4.0.0 main.py
pyinstaller -F -i img/icon/icon.ico -n 灵卡面板V4.0.0 main.py
nuitka --mingw64 --standalone --enable-plugin=pyside6 --disable-plugin=pyqt5,pyqt6 --include-qt-plugins=mediaservice,multimedia --windows-console-mode=disable --windows-icon-from-ico=static/img/icon/light/icon.ico --onefile --output-dir=out --lto=yes --jobs=14 AgileTiles.py
"""

安装:
```shell
pip install lxml==4.6.3
pip install winotify==1.1.0
pip install cnlunar==0.1.0
pip install zhdate==0.1
pip install requests==2.32.3
pip install pynput==1.7.6
pip install browser_cookie3==0.17.0
pip install pywin32==302
pip install Nuitka==2.3.10              # 打包工具,可选
pip install pillow==8.4.0               # 安装不成看下面的
```

# 关于pillow的安装:

先下载Microsoft C++ Build Tools:
[https://visualstudio.microsoft.com/visual-cpp-build-tools/](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
然后选择第一个安装
![](https://user-images.githubusercontent.com/30068301/171110492-0fd05d9d-5158-4ce6-86d4-c6a39393c60f.png)

# 关于Nuitka的安装:

详见：https://static.kancloud.cn/ay66544/py-0-1/2659009

（其中的x86_64-win32有做nas保存，位置：个人文件\收藏\代码工具备份\x86_64-8.1.0-release-win32-seh-rt_v6-rev0.7z）

其他
```shell

pip install pyside2
pip install PySide2-Frameless-Window

pip uninstall pyside2
pip uninstall PySide2-Frameless-Window

pip install pyqt5
pip install PyQt5-Frameless-Window
pip install pyqt5-tools

pip uninstall pyqt5
pip uninstall PyQt5-Frameless-Window
pip uninstall pyqt5-tools


pip install pyside6
pip install PySideSix-Frameless-Window


pip uninstall pyside6
pip uninstall PySideSix-Frameless-Window




# 内存分析工具
```python
import tracemalloc
tracemalloc.start(100)
def analysis_memory(self):
    self.info_logger.card_warning("内存分析",
                                  "↓==============================内存分析开始==================================↓")
    time_2 = tracemalloc.take_snapshot()
    stats = time_2.compare_to(self.tracemalloc_start, 'traceback')
    for stat in stats[:10]:
        line_str = "%s memory blocks: %.1f KiB" % (stat.count, stat.size / 1024) + "\n"
        is_show = True
        for line in stat.traceback.format():
            if "self.analysis_memory()" in line:
                is_show = False
                break
            line_str += line + "\n"
        if not is_show:
            continue
        self.info_logger.card_warning("内存分析", line_str)
    self.info_logger.card_warning("内存分析",
                                  "↑==============================内存分析结束==================================↑")
```
