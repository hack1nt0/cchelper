from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from cchelper import *
from .filesubmit_ui import Ui_FileSubmitter

class FileSubmitter(QDialog, Ui_FileSubmitter):
    def __init__(self, parent: QWidget =None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        