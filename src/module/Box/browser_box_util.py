import os

from PySide6 import QtGui
from PySide6.QtCore import QUrl, QDir
from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile, QWebEnginePage
from PySide6.QtWidgets import QVBoxLayout, QApplication, QHBoxLayout

from src.component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
from src.component.AgileTilesFramelessWebEngineView.AgileTilesFramelessWebEngineView import AgileTilesFramelessWebEngineView

def get_custom_profile():
    data_dir = str(os.getcwd()) + "/cache/browser"
    QDir().mkpath(data_dir)
    profile = QWebEngineProfile("MyCustomProfile")  # 创建独立 profile
    profile.setCachePath(QDir(data_dir).filePath("cache"))
    profile.setPersistentStoragePath(QDir(data_dir).filePath("storage"))
    profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
    profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
    return profile


class BrowserPopup(AgileTilesAcrylicWindow):
    def __init__(self, parent=None, use_parent=None, title=None, content=None, link=None):
        super().__init__(parent=parent, is_dark=use_parent.is_dark, form_theme_mode=use_parent.form_theme_mode,
                                                 form_theme_transparency=use_parent.form_theme_transparency)
        self.setWindowTitle("页面查看" if title is None else title)
        if link:
            self.standard_title_bar.setLink(link)
        # 大小调整
        browser_width = 1000
        browser_height = 800
        if 'size' in content:
            browser_width = content["size"][0]
            browser_height = content["size"][1]
        self.setMinimumSize(browser_width + 20, browser_height + 32 + 20)
        if 'max' in content and content['max']:
            self.showFullScreen()
        else:
            self.center_on_screen()
        self.init_ui()
        url = content['url']
        self.load_html(url)

    def init_ui(self):
        # 内容布局
        self.browser_layout = QVBoxLayout()
        # self.remove_window_effect()
        # 初始化浏览器
        self.default_profile = get_custom_profile()
        self.web_page = QWebEnginePage(self.default_profile)
        self.my_browser = AgileTilesFramelessWebEngineView(self)
        self.my_browser.setPage(self.web_page)
        self.my_browser.settings().setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, False)
        self.my_browser.setStyleSheet("background-color:transparent;background:transparent;padding:0px;margin:0px;")
        # 确保页面完全加载
        self.my_browser.loadFinished.connect(lambda ok: print("加载完成，等待缓存写入..."))
        # 设置浏览器不打开链接
        # self.my_browser.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.browser_layout.addWidget(self.my_browser)
        # 主布局
        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.browser_layout)
        self.widget_base.setLayout(self.main_layout)
        self.update()

    def center_on_screen(self):
        qr = self.frameGeometry()
        cp = QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def load_html(self, url):
        if not url.startswith("http"):
            url = "file:///" + str(os.getcwd()).replace("\\", "/") + url
        self.my_browser.load(QUrl(url))
        self.my_browser.page().setBackgroundColor(QtGui.QColorConstants.Transparent)

    def closeEvent(self, e):
        print(f"关闭的是 BrowserPopup (对象ID:{id(self)})，不是主窗口")
        # 显式释放WebEngine资源
        self.my_browser.page().deleteLater()
        self.default_profile.deleteLater()
        super().closeEvent(e)


def show_browser_dialog(main_object, title, content, link):
    print(f"准备打开浏览器窗口:{title}...")
    dialog = BrowserPopup(None, main_object, title, content, link)
    dialog.refresh_geometry(main_object.toolkit.resolution_util.get_screen(main_object))
    dialog.show()
    print(f"加载浏览器窗口:{title}完成")
    return dialog
