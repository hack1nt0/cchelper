from cchelper import *
from .taskterminal_ui import Ui_TaskStashW


class TaskStashW(QMainWindow, Ui_TaskStashW):
    add_task_signal: Signal = Signal(Task)
    arxiv_task_signal: Signal = Signal()

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)