from cchelper import *
from PySide6.QtCharts import *
from .chartviewerd_ui import Ui_ChartViewerD


class ChartViewerD(QDialog, Ui_ChartViewerD):
    drillin_signal: Signal = Signal(VS)

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        # self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowFlags(Qt.WindowType.Tool)

        self.widget.drillin_signal.connect(self.drillin_signal.emit)
        self.buttonBox.button(QDialogButtonBox.StandardButton.Reset).clicked.connect(
            lambda: self.drillin_signal.emit(None)
        )

    def set_task(self, task: Task):
        self.widget.set_task(task)

    def clear(self):
        self.widget.clear()

    def refresh(self):
        self.widget.refresh()
