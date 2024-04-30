from PySide6.QtWidgets import QWidget
from cchelper import *
from .model import TaskModel
from .testbrowser_ui import Ui_TestArxivBrowser


class TestBrowser(QDialog, Ui_TestArxivBrowser):
    def __init__(self, dats, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.label.setStyleSheet("background-color : blue; color : white;")
        self.model = TaskModel(self)
        self.model.dats = dats
        self.view.setModel(self.model)
        self.view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        # self.view.horizontalHeader().setSectionResizeMode(
        #     0, QHeaderView.ResizeMode.Stretch
        # )
        self.view.verticalHeader().setVisible(F)
        # self.setFixedWidth(400)
