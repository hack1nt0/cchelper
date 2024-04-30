from PySide6.QtGui import QResizeEvent
from cchelper import *
from PySide6.QtCharts import *


class ChartView(QChartView):
    drillin_signal: Signal = Signal(VS)

    def __init__(self, parent: QWidget = None) -> None:
        self.father = parent
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.setContentsMargins(0, 0, 0, 0)

        self.setRenderHint(QPainter.Antialiasing)
        # self.chart().legend().hide()
        self.chart().legend().setAlignment(Qt.AlignmentFlag.AlignRight)
        self.chart().legend().setInteractive(F)
        self.chart().setTitleBrush(WHITE)
        self.chart().layout().setContentsMargins(0, 0, 0, 0)
        # self.chart().setBackgroundVisible(F)
        self.chart().setBackgroundBrush(BLUE)
        self.chart().setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self.chart().setBackgroundRoundness(0)
