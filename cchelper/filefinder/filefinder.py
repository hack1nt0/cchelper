from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from cchelper import *
from .filefinder_ui import Ui_FileFinder

class FileFinder(QDialog, Ui_FileFinder):
    def __init__(self, parent: QWidget=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.path = None
        self.contains = None
    
    def done(self, arg__1: int) -> None:
        if arg__1:
            self.path = self.pathLineEdit.text()
            self.contains = self.containsLineEdit.text()
        return super().done(arg__1)