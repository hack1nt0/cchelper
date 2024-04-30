from PySide6.QtGui import QResizeEvent
from cchelper import *
from PySide6.QtCharts import *
from collections import Counter
from cchelper.verdictbrowser.model import VerdictModel
from .chartviewer_ui import Ui_ChartViewer


class ChartViewer(QWidget, Ui_ChartViewer):
    drillin_signal: Signal = Signal(VS)

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        # self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        # self.setWindowFlags(Qt.WindowType.Tool)

        self.series = QPieSeries()
        self.view.chart().addSeries(self.series)
        self.slices: Dict[str, QPieSlice] = {}
        self.colors: Dict[str, QColor] = {}
        self.markers: Dict[str, QLegendMarker] = {}

        for label in self.labels:
            slice = self.series.append(label, 0)
            color = VerdictModel.COLORS[VS.kind(VS(label))]
            if color == BLUE:
                color = WHITE
            slice.setPen(color)
            slice.setBrush(color)
            slice.setExploded(F)
            slice.setLabelVisible(F)
            # slice.setLabel(f"{slice.label()}: #{int(slice.value())}")
            # slice.setLabelPosition(QPieSlice.LabelPosition.LabelInsideNormal)
            # slice.setLabelColor(color)
            self.slices[label] = slice
            self.colors[label] = color
            slice.clicked.connect(self.popup_closure(label))
            # slice.hovered.connect(self.explode_closure(label))
        for marker in self.view.chart().legend().markers(self.series):
            label = marker.label()
            marker.clicked.connect(self.popup_closure(label))
            # marker.hovered.connect(self.explode_closure(label))
            self.markers[label] = marker
        # self.series.clicked.connect(lambda: self.filter)

        self.view.chart().setTitle("Click slice/marker to drill in verdicts of specific vs.")

    @property
    def labels(self):
        return [status.value for status in VS]

    def set_task(self, task: Task):
        self.task = task
        self.verdicts = task.verdicts
        counter = Counter((v.status.value for v in self.verdicts))
        for label in self.labels:
            self.slices[label].setValue(counter[label])
        for label in self.labels:
            c = counter[label]
            self.markers[label].setVisible(c > 0)
            self.markers[label].setLabel(f"{label}: {c}")

    def clear(self):
        for label in self.labels:
            self.slices[label].setValue(0)
        for label in self.labels:
            self.markers[label].setVisible(F)

    def refresh(self):
        counter = Counter((v.status.value for v in self.verdicts))
        for label in self.labels:
            self.slices[label].setValue(counter[label])
        for label in self.labels:
            c = counter[label]
            self.markers[label].setVisible(c > 0)
            self.markers[label].setLabel(f"{label}: {c}")

    # def popup_closure(self, label: str):
    #     def f():
    #         slice = self.slices[label]
    #         if abs(slice.percentage()) < 1e-6:
    #             return
    #         d = VerdictBrowser(self.task, VS(label), self)
    #         # d.setGeometry(self.geometry())
    #         d.resize(self.father.size())
    #         d.open()
    #     return f

    def popup_closure(self, label: str):
        def f():
            for lbl, slc in self.slices.items():
                slc.setBrush(self.colors[lbl])
            slice = self.slices[label]
            slice.setBrush(QBrush(self.colors[label], Qt.BrushStyle.DiagCrossPattern))
            if abs(slice.percentage()) < 1e-6:
                return
            self.drillin_signal.emit(VS(label))

        return f

    def explode_closure(self, label: str):
        def f():
            for lbl, slc in self.slices.items():
                slc.setBrush(self.colors[lbl])
            slice = self.slices[label]
            slice.setBrush(QBrush(self.colors[label], Qt.BrushStyle.DiagCrossPattern))

        return f
