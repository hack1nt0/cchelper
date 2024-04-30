from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from cchelper import *
from .terminal_ui import Ui_Terminal

class Terminal(QDialog, Ui_Terminal):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
