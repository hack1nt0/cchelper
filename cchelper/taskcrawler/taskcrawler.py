from cchelper import *
from .taskcrawler_ui import Ui_TaskCrawler
from .taskmodel import TaskModel
from .testmodel import TestModel
from .testdelegate import TestDelegate
from .parse import parse


class TaskCrawler(QDialog, Ui_TaskCrawler):
    add_task_signal: Signal = Signal(list)

    def __init__(
        self,
        parent: QWidget,
    ) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.crawlButton.setToolTip("Return to parse")
        # self.parseButton.setIcon(QIcon(path.img("sync.png")))
        self.crawlButton.clicked.connect(self.crawl)
        self.urlLineEdit.returnPressed.connect(self.crawl)
        self.urlLineEdit.setFocus()

        view = self.taskTable
        # view.setSortingEnabled(True)
        model = TaskModel(view)
        view.setModel(model)
        for idx, col in enumerate(model.cols):
            match col:
                case "name":
                    view.horizontalHeader().setSectionResizeMode(
                        idx, QHeaderView.ResizeMode.Stretch
                    )
                case _:
                    view.hideColumn(idx)
        view.verticalHeader().setVisible(F)
        # TODO task view selection...
        view.selectionModel().currentRowChanged.connect(self.change_task)
        self.task_model = model
        self.task_view = view

        view = self.testTable
        model = TestModel(parent=view)
        view.setModel(model)
        delegate = TestDelegate(self)
        view.setItemDelegate(delegate)
        for idx, col in enumerate(model.cols):
            match col:
                case "input":
                    view.horizontalHeader().setSectionResizeMode(
                        idx, QHeaderView.ResizeMode.Stretch
                    )
                case "answer":
                    view.horizontalHeader().setSectionResizeMode(
                        idx, QHeaderView.ResizeMode.Stretch
                    )
                case _:
                    view.hideColumn(idx)
        view.verticalHeader().setVisible(T)
        view.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.test_model = model
        self.test_view = view
        self.test_delegate = delegate

        self.okButton.clicked.connect(lambda: self.done(1))
        # self.nkButton.clicked.connect(lambda: self.done(0))
        self.convertButton.clicked.connect(self.convert)

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if (
            e.key() == Qt.Key.Key_L
            and e.modifiers() == Qt.KeyboardModifier.ControlModifier
        ):
            self.urlLineEdit.setFocus()
            self.urlLineEdit.selectAll()
            return T
        return super().keyPressEvent(e)

    def all_widgets(self) -> List[QWidget]:
        return [
            self.urlLineEdit,
            self.task_view,
            self.test_view,
            self.okButton,
            self.crawlButton,
        ]

    def crawl(self):
        # self._crawl()
        global_threadpool.submit(self._crawl)
        for w in self.all_widgets():
            w.setEnabled(F)

    def _crawl(self):
        try:
            tasks = None
            self.test_model.beginResetModel()
            self.test_model.dats.clear()
            self.test_model.endResetModel()
            url = self.urlLineEdit.text().strip()
            tasks = parse(url) if url else None
        except BaseException as e:
            logger.error("Failed to Crawl, see log for detail")
            logger.exception(e)
        finally:
            if tasks:
                self.task_model.beginResetModel()
                self.task_model.dats = tasks
                self.task_model.endResetModel()
            for w in self.all_widgets():
                w.setEnabled(T)

    def add_task(self, task):
        idx = self.task_model.rowCount()
        self.task_model.beginInsertRows(QModelIndex(), idx, idx)
        self.task_model.dats.append(task)
        self.task_model.endInsertRows()

    def change_task(self, current, previous):
        if current.row() >= 0:
            task = self.task_model.dats[current.row()]
            self.test_model.beginResetModel()
            self.test_model.dats = task.tests
            self.test_model.endResetModel()
        else:
            self.test_model.beginResetModel()
            self.test_model.dats.clear()
            self.test_model.endResetModel()

    def convert(self):
        def test_to_str(obj: str) -> str:  # TODO
            w = io.StringIO()
            idx = 0
            while idx < len(obj):
                c = obj[idx]
                if c == '[':
                    arr = io.StringIO()
                    arr.write(c)
                    bs = 1
                    while bs:
                        idx += 1
                        c = obj[idx]
                        arr.write(c)
                        if c == ']': bs -= 1
                        if c == '[': bs += 1
                    arr = eval(arr.getvalue())
                    w.write(str(len(arr)))
                    if isinstance(arr[0], list):
                        w.write(' ')
                        w.write(str(len(arr[0])))
                        if isinstance(arr[0][0], list):
                            w.write(' ')
                            w.write(str(len(arr[0][0])))
                            for i in range(len(arr)):
                                for j in range(len(arr[0])):
                                    w.write('\n')
                                    w.write(' '.join(map(str, arr[i][j])))
                        else:
                            for row in arr:
                                w.write('\n')
                                w.write(' '.join(map(str, row)))
                    else:
                        w.write('\n')
                        w.write(' '.join(map(str, arr)))
                else:
                    w.write(c)
                idx += 1
            return w.getvalue()
        for task in self.task_model.dats:
            for test in task.tests:
                test.input = test_to_str(test.input)
                test.answer = test_to_str(test.answer)
        self.test_model.modelReset.emit()

    def done(self, arg__1: int) -> None:
        if arg__1:
            self.add_task_signal.emit(self.task_model.dats)
        del windows[self.__class__.__name__]
        super().done(arg__1)
