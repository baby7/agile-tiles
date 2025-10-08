# # coding: utf-8
# import sys
#
# from PySide6.QtCore import Qt
# from PySide6.QtWebEngineWidgets import QWebEngineView
#
# from src.my_component.AgileTilesFramelessDialog.AgileTilesFramelessDialog import AgileTilesFramelessDialog
# from src.my_component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
# from src.my_component.MainAcrylicWindow.MainAcrylicWindow import MainAcrylicWindow
#
# from qframelesswindow import FramelessDialog, AcrylicWindow
#
#
# class AgileTilesFramelessWebEngineView(QWebEngineView):
#     """ Frameless web engine view """
#
#     def __init__(self, parent):
#         if sys.platform == "win32" and isinstance(parent.window(), (AgileTilesAcrylicWindow, MainAcrylicWindow, FramelessDialog, AcrylicWindow)):
#             parent.window().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
#
#         super().__init__(parent=parent)
#         self.setHtml("")
#
#         if isinstance(self.window(), (AgileTilesAcrylicWindow, FramelessDialog)):
#             self.window().updateFrameless()
