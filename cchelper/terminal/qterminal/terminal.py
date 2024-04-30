from PySide6.QtCore import Qt
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QWidget
from cchelper import *
from .terminal_ui import Ui_Terminal
import pyte
import paramiko


class Terminal(QWidget, Ui_Terminal):
    view_signal: Signal = Signal(File)

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        windows['terminal'] = self.widget

        self.widget.set_pty()
        self.resize(800, 600)

        self.widget.write(b"export LANG=zh_CN.UTF-8\n")
        self.widget.write(b"export TERM=xterm\n")

        self.viewButton.setShortcut("F3")
        self.viewButton.clicked.connect(self.view_file)
        self.clearButton.setShortcut("Ctrl+K")
        self.clearButton.clicked.connect(lambda: self.widget.write(b"clear\n"))

    def view_file(self):
        self.view_signal.emit(File(self.widget.view_file()))
