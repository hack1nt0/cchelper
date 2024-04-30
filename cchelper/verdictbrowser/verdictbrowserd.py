from PySide6.QtGui import QCloseEvent
from cchelper import *
from .verdictbrowser_ui import Ui_VerdictBrowser
from .model import VerdictModel
from cchelper.fileviewer import FileViewerD
from .delegate import VerdictDelegate
from cchelper.gviewer import GViewer
from cchelper.chartviewer import ChartViewer


class VerdictBrowser(QDialog, Ui_VerdictBrowser):
    add_test_signal: Signal = Signal()

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        # self.setWindowFlags(Qt.WindowType.Tool)
        # self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        # self.label.setStyleSheet("background-color : blue; color : white;")
        # self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.view.setTabKeyNavigation(False)
        self.view.setAlternatingRowColors(True)

        self.model = VerdictModel(self.view)
        self.view.setModel(self.model)
        self.view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        for col in ["status", "cmd", "input", "actual", "answer", "chat", "stderr"]:
            idx = self.model.cols.index(col)
            self.view.horizontalHeader().setSectionResizeMode(
                idx, QHeaderView.ResizeMode.Stretch
            )
        self.view.verticalHeader().setVisible(F)
        self.view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)

        self.deleg = VerdictDelegate(self)
        self.view.setItemDelegate(self.deleg)

        self.pageNoBox.valueChanged.connect(self.pageno_changed)
        self.prevButton.setShortcut(Qt.Key.Key_PageUp)
        self.prevButton.clicked.connect(
            lambda: self.pageNoBox.setValue(self.pageNoBox.value() - 1)
        )
        self.nextButton.setShortcut(Qt.Key.Key_PageDown)
        self.nextButton.clicked.connect(
            lambda: self.pageNoBox.setValue(self.pageNoBox.value() + 1)
        )
        self.tailsSpinBox.setRange(1, int(1e9))
        self.tailsSpinBox.setValue(conf.bytes_per_cell)
        self.tailsSpinBox.valueChanged.connect(self.tails_changed)

        self.view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.popup_context_menu)
        self.context_menu = QMenu(self)
        self.add_act = self.context_menu.addAction("Add as Test")
        self.add_act.setIcon(QIcon(paths.img("add.png")))
        self.add_act.triggered.connect(self.add_as_test)
        # self.view_act = self.context_menu.addAction("View File")
        # self.view_act.setIcon(QIcon(paths.img("eye.png")))
        # self.view_act.triggered.connect(self.view_file)

        self.AButton.clicked.connect(self.add_as_test)
        self.EButton.clicked.connect(self.extract_gvdots)

        # self.timer = QTimer(self)
        # self.timer.setInterval(1000 // conf.refresh_rate)
        # self.timer.timeout.connect(self.refresh)
        # self.timer.start()
        self.is_refresh = F

        self.chartViewer = ChartViewer(self)
        self.chartViewer.hide()
        self.chartViewer.drillin_signal.connect(self.drillin)
        self.chartButton.clicked.connect(self.chartViewer.show)
        self.fileViewer = FileViewerD(self)
        self.fileViewer.hide()
        self.deleg.view_signal.connect(self.view_file)
        self.graphViewer = GViewer(self)
        self.graphViewer.hide()

    def setData(self, task: Task):
        self.status = None
        self.task = task
        self.model.beginResetModel()
        self.model.dats = task.verdicts
        self.pageNoBox.blockSignals(T)
        self.model.offset = 0
        self.model.limit = 1
        self.model.tail_bytes = self.tailsSpinBox.value()
        psz, pno = 1, 1
        self.tot = len(task.verdicts)
        ptot = max(1, (self.tot + psz - 1) // psz)
        self.pageNoBox.setSuffix(f"/{ptot} pages")
        self.pageNoBox.setRange(1, ptot)
        self.pageNoBox.setValue(pno)
        self.model.endResetModel()
        self.pageNoBox.blockSignals(F)
        self.chartViewer.set_task(task)

    def clear(self):
        self.fileViewer.hide()
        self.chartViewer.clear()
        self.graphViewer.hide()
        self.model.beginResetModel()
        self.model.dats.clear()
        self.model.endResetModel()

    def drillin(self, status: VS = None):
        self.status = status
        self.refresh()

    def start(self, step: str):
        cols = None
        match step:
            case "Build":
                cols = {"status", "cmd", "stderr"}
                self.show()
                self.chartViewer.show()
                self.fileViewer.hide()
                self.graphViewer.hide()
            case "Run":
                if not self.task.interactive:
                    cols = {
                        "id",
                        "status",
                        "input",
                        "actual",
                        "answer",
                        "stderr",
                    }
                else:
                    cols = {
                        "id",
                        "status",
                        "stderr",
                        "input",
                        "chat",
                    }
        if cols:
            for col in cols:
                self.view.showColumn(self.model.cols.index(col))
            for col in set(self.model.cols) - cols:
                self.view.hideColumn(self.model.cols.index(col))
        self.chartViewer.start(step)

    def refresh(self):
        if self.is_refresh:
            return
        self.chartViewer.refresh()
        self.is_refresh = T
        self.pageNoBox.blockSignals(T)
        self.model.dats = (
            self.task.verdicts
            if self.status is None
            else list(filter(lambda v: v.status == self.status, self.task.verdicts))
        )
        ptot = max(1, len(self.model.dats))
        pno = min(ptot, self.pageNoBox.value())
        self.model.offset = pno - 1
        self.pageNoBox.setValue(pno)
        self.pageNoBox.setRange(1, ptot)
        self.pageNoBox.setSuffix(f"/{ptot} pages")
        self.model.refresh()
        self.pageNoBox.blockSignals(F)
        self.is_refresh = F

    def stop(self):
        self.chartViewer.stop()

    def pageno_changed(self, v):
        self.model.offset = v - 1
        self.model.refresh()

    def tails_changed(self, v):
        self.model.tail_bytes = v
        self.model.refresh()

    def add_as_test(self):
        if self.model.rowCount() == 0:
            return
        verdict = self.model.dats[self.model.offset]
        if verdict.test_id is None:
            logger.info(f"Failed to add verdict #{verdict.id} as test: compilation.")
            return
        if VS.kind(verdict.status) == 3:
            logger.info(f"Failed to add verdict #{verdict.id} as test: unfinished.")
            return
        test_id = None
        for test in self.task.tests:
            if test.input_type == IT.MANUAL and test.input == verdict.input:
                test_id = test.id
                break
        if test_id is None:
            test_id = len(self.task.tests)
            test = Test(
                id=test_id,
                status=verdict.status,
                checked=T,
                input_type=IT.MANUAL,
                answer_type=self.task.tests[verdict.test_id].answer_type,
                input=File(self.task.test_dir(test_id, "input.txt")),
                answer=File(self.task.test_dir(test_id, "answer.txt")),
            )
            with (
                open(verdict.input.path, "r") as r,
                open(test.input.path, "w") as w,
            ):
                # w.write(r.read())  # TODO
                for line in r:
                    w.write(line)
            with (
                open(verdict.answer.path, "r") as r,
                open(test.answer.path, "w") as w,
            ):
                for line in r:
                    w.write(line)
            self.task.tests.append(test)
        verdict.added_as_test = T
        logger.info(f"Successfully added verdict #{verdict.id} as test #{test_id}.")

    def extract_gvdots(self):
        if self.model.rowCount() == 0:
            return
        stderr: File = self.model.data(
            self.model.index(0, self.model.cols.index("stderr")),
            role=Qt.ItemDataRole.EditRole,
        )
        self.show_gviewer(stderr)

    def show_gviewer(self, file: File):
        self.graphViewer.set_file(file)
        self.graphViewer.show()

    def view_file(self, file: File):
        self.fileViewer.set_file(file)
        self.fileViewer.show()

    def popup_context_menu(self, point):
        idx = self.view.indexAt(point)
        self.add_act.setEnabled(idx.isValid())
        # self.view_act.setEnabled(
        #     idx.isValid()
        #     and isinstance(
        #         getattr(self.model.dats[idx.row()], self.model.cols[idx.column()]), File
        #     )
        # )
        # self.context_menu.popup(QCursor().pos())
        self.context_menu.popup(self.view.viewport().mapToGlobal(point))


    def show(self) -> None:
        super().show()
        self.raise_()
        self.activateWindow()

    def closeEvent(self, arg__1: QCloseEvent) -> None:
        self.fileViewer.close()
        self.chartViewer.close()
        self.graphViewer.close()
        return super().closeEvent(arg__1)