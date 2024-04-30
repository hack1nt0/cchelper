
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtSql import *
from PySide6.QtCharts import *
from PySide6.QtStateMachine import *
import sys
import traceback
from .terminal import Terminal
from .widget2 import QTerminal


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Terminal()
    win.show()
    sys.exit(app.exec())