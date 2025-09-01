from PySide6.QtCore import QSettings

settings = QSettings("AgileTiles", "TutorialProgram")
settings.setValue("FirstRun", True)