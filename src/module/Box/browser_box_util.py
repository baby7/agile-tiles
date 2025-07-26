import os

from PySide6 import QtCore
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


# 自定义WebEnginePage以捕获控制台日志
class ConsoleLogWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        """重写控制台消息处理，将日志输出到Python控制台"""
        log_levels = {
            QWebEnginePage.JavaScriptConsoleMessageLevel.InfoMessageLevel: "INFO",
            QWebEnginePage.JavaScriptConsoleMessageLevel.WarningMessageLevel: "WARNING",
            QWebEnginePage.JavaScriptConsoleMessageLevel.ErrorMessageLevel: "ERROR"
        }
        level_str = log_levels.get(level, "UNKNOWN")
        print(f"[Browser Console] [{level_str}] Line {lineNumber}: {message}")
        super().javaScriptConsoleMessage(level, message, lineNumber, sourceID)


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
        self.url = content['url']
        self.load_html(self.url)

    def init_ui(self):
        # 内容布局
        self.browser_layout = QVBoxLayout()
        # self.remove_window_effect()
        # 初始化浏览器
        self.default_profile = get_custom_profile()
        # 使用自定义的ConsoleLogWebEnginePage
        self.web_page = ConsoleLogWebEnginePage(self.default_profile)
        self.my_browser = AgileTilesFramelessWebEngineView(self)
        self.my_browser.setPage(self.web_page)
        self.my_browser.settings().setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, False)
        self.my_browser.setStyleSheet("background:transparent;padding:0px;margin:0px;")
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
        # self.my_browser.page().setBackgroundColor(QtGui.QColorConstants.Transparent)

        # 在页面加载完成后强制设置深色主题
        def on_load_finished(ok):
            if not ok:
                return
            if self.url == "/static/html/Game/XiuXianGame/index.html":
                QtCore.QTimer.singleShot(1000, self.apply_theme)
                return
            # 使用定时器延迟执行
            QtCore.QTimer.singleShot(100, self.apply_theme)
            QtCore.QTimer.singleShot(200, self.apply_theme)
            QtCore.QTimer.singleShot(400, self.apply_theme)
            QtCore.QTimer.singleShot(600, self.apply_theme)
            QtCore.QTimer.singleShot(800, self.apply_theme)
            QtCore.QTimer.singleShot(1000, self.apply_theme)
            QtCore.QTimer.singleShot(1200, self.apply_theme)
            QtCore.QTimer.singleShot(1400, self.apply_theme)
            QtCore.QTimer.singleShot(1600, self.apply_theme)

        # 单次连接确保只执行一次
        self.my_browser.loadFinished.connect(
            on_load_finished,
            QtCore.Qt.ConnectionType.SingleShotConnection
        )

    def apply_theme(self):
        """应用主题的JS代码"""
        theme = 'dark' if self.is_dark else 'light'
        js_code = None
        # *********************************** 工具箱模块 ***********************************
        # 程序员工具箱
        if self.url == "/static/html/Tool/ctool_web/index.html":
            js_code = f'document.documentElement.dataset.theme="{theme}";'
        # 程序员速查表
        elif self.url == "/static/html/Tool/reference/index.html":
            js_code = f'document.documentElement.dataset.colorMode = "{theme}";'
        # API调试工具
        elif self.url == "https://hoppscotch.io/":
            js_code = f'document.documentElement.className="{theme}";'
        # 手绘风格的绘图工具
        elif self.url == "https://excalidraw.com/":
            theme = 'excalidraw excalidraw-container theme--dark' if self.is_dark else 'excalidraw excalidraw-container'
            js_code = f'document.querySelector("#root > div > div").className="{theme}";'
        # 经典作图工具
        elif self.url == "https://app.diagrams.net/index.html":
            js_code = f'document.querySelector("body").style.setProperty("color-scheme", "{theme}");'
        # 像素绘图工具
        elif self.url == "https://www.piskelapp.com/p/create/sprite":
            # 暂无切换主题功能
            pass
        # Svg编辑工具
        elif self.url == "https://yqnn.github.io/svg-path-editor/":
            # 暂无切换主题功能
            pass
        # Ascii作图工具
        elif self.url == "/static/html/Tool/asciiflow/index.html":
            if self.is_dark:
                js_code = f"""
                    document.querySelector("#root > div > div > div > img").src = "public/logo_full.svg";
                    if (!document.querySelector("#root > div").className.includes(" dark")) {{
                        document.querySelector("#root > div > div > ul > li:nth-child(10) > div.MuiListItemSecondaryAction-root > button:nth-child(2)").click()
                    }};"""
            else:
                js_code = f"""
                    document.querySelector("#root > div > div > div > img").src = "public/logo_full.svg";
                    if (document.querySelector("#root > div").className.includes(" dark")) {{
                        document.querySelector("#root > div > div > ul > li:nth-child(10) > div.MuiListItemSecondaryAction-root > button:nth-child(2)").click()
                    }};"""
        # 中国家庭称谓计算器
        elif self.url == "https://passer-by.com/relationship/vue/#/":
            # 暂无切换主题功能
            pass
        # 制霸生成器
        elif self.url == "https://lab.magiconch.com/china-ex/" or self.url == "https://lab.magiconch.com/world-ex/":
            # 暂无切换主题功能
            pass
        # 科学计算器
        elif self.url == "https://calcium.js.org/":
            js_code = f'document.querySelector("body").setAttribute("theme", "{theme}");'
        # 命令行计算器
        elif self.url == "https://clcalc.net/":
            js_code = f'document.querySelector("body").className="{theme}";'
        # *********************************** 游戏模块 ***********************************
        # 小黑屋
        elif self.url == "/static/html/Game/adarkroom/index.html":
            if self.is_dark:
                js_code = f"""
                    if (document.querySelector("body > div.menu > span.lightsOff.menuBtn").textContent == "夜间模式"
                    || document.querySelector("body > div.menu > span.lightsOff.menuBtn").includes("off")) {{
                        document.querySelector("body > div.menu > span.lightsOff.menuBtn").click()
                    }};"""
            else:
                js_code = f"""
                    if (document.querySelector("body > div.menu > span.lightsOff.menuBtn").textContent == "开灯"
                    || document.querySelector("body > div.menu > span.lightsOff.menuBtn").includes("on")) {{
                        document.querySelector("body > div.menu > span.lightsOff.menuBtn").click()
                    }};"""
        # 我的文字修仙全靠刷
        elif self.url == "/static/html/Game/XiuXianGame/index.html":
            if self.is_dark:
                js_code = f"""
                    if (document.documentElement.className!="dark") {{
                        document.querySelector("#app > div > div.game-container > div.footer > div > span").click()
                    }};"""
            else:
                js_code = f"""
                    if (document.documentElement.className="dark") {{
                        document.querySelector("#app > div > div.game-container > div.footer > div > span").click()
                    }};"""
        # 人生重开模拟器
        elif self.url == "https://passer-by.com/relationship/vue/#/":
            # Canvas绘制，暂时没找到切换主题的JS代码
            pass
        # 太空公司
        elif self.url == "/static/html/Game/SpaceCompany/index.html":
            theme = 'styles/darkly-bootstrap.min.css' if self.is_dark else 'lib/bootstrap.min.css'
            js_code = f'document.querySelector("#theme_css").href"{theme}";'
        # 信任的进化
        elif self.url == "/static/html/Game/trust/index.html":
            # 暂无切换主题功能
            pass
        # 超苦逼冒险者
        elif self.url == "/static/html/Game/KuBiTionAdvanture/index.html":
            # 暂无切换主题功能
            pass
        # 挂机放置类小游戏
        elif self.url == "http://couy.xyz/#/":
            # 暂无切换主题功能
            pass
        # 2048
        elif self.url == "/static/html/Game/2048/index.html":
            # 暂无切换主题功能
            pass
        # 圈小猫
        elif self.url == "/static/html/Game/CorralCat/index.html":
            # 暂无切换主题功能
            pass
        # 数独
        elif self.url == "/static/html/Game/Sudoku/index.html":
            # 暂无切换主题功能
            pass
        # 俄罗斯方块
        elif self.url == "/static/html/Game/Tetris/index.html":
            # 暂无切换主题功能
            pass
        else:
            return
        if js_code is None:
            return
        self.my_browser.page().runJavaScript(js_code)

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
