from cchelper import *
from .taskarxivbrowser_ui import Ui_TaskArxivBrowser
from .model import TaskModel
from .delegate import TaskDelegate
from cchelper.taskfinder import TaskFinder
from cchelper.fileviewer import FileViewerD
import tempfile
from .testbrowser import TestBrowser


class TaskArxivBrowser(QDialog, Ui_TaskArxivBrowser):
    find_signal: Signal = Signal(object)
    stash_task_signal: Signal = Signal()

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        # self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowTitle("Arxiv - Tasks")
        # self.label.setStyleSheet("background-color : blue; color : white;")

        self.view.setSortingEnabled(True)
        self.model = TaskModel(self.view)
        self.view.setModel(self.model)
        self.deleg = TaskDelegate(self.view)
        self.deleg.drill_in_signal.connect(self.drill_in)
        self.view.setItemDelegate(self.deleg)
        self.view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        # self.view.horizontalHeader().setSectionResizeMode(
        #     self.model.cols.index("doc"),
        #     QHeaderView.ResizeMode.Stretch,
        # )
        self.view.verticalHeader().setVisible(False)

        self.form = None

        self.pageSzBox.setEnabled(F)
        self.pageNoBox.setEnabled(F)
        self.pageNoBox.setMinimum(1)
        self.pageSzBox.setMinimum(1)
        self.pageSzBox.valueChanged.connect(self.pagesz_changed)
        self.pageNoBox.valueChanged.connect(self.pageno_changed)

        self.view.selectionModel().selectionChanged.connect(self.select_changed)
        self.view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.view.setTabKeyNavigation(False)
        self.view.setAlternatingRowColors(True)
        self.view.horizontalHeader().setSortIndicatorShown(F)
        # self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.view.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.stashButton.setEnabled(F)
        self.stashButton.clicked.connect(self._stash_task)

        self.fileViewer = FileViewerD(self)
        self.fileViewer.hide()

        self.offset = 0
        self.limits = 20
        self.order_by = "ctime"
        self.order: Qt.SortOrder = None
        self.where_form = {}
        self.find_signal.connect(self.refresh)

    def find(self) -> int:
        tot = db.query(
            (
                f"""
            select count(*) AS tot
            from task
                join file on file.task_id=task.id and file.path=task.solver
            where 1=1
                AND url like ?
                AND name like ?
                AND tags & {self.where_form['tags']} = {self.where_form['tags']} 
                AND ctime BETWEEN {self.where_form['ctime_l']} AND {self.where_form['ctime_r']}
                AND file.content like ?
            """,
                (
                    f"%{self.where_form['url']}%",
                    f"%{self.where_form['name']}%",
                    f"%{self.where_form['solver_c']}%",
                ),
            )
        )[0]["tot"]
        dats = db.query(
            (
                f"""
            select task.*
            from task
                join file on file.task_id=task.id and file.path=task.solver
            where 1=1
                AND url like ?
                AND name like ?
                AND tags & {self.where_form['tags']} = {self.where_form['tags']} 
                AND ctime BETWEEN {self.where_form['ctime_l']} AND {self.where_form['ctime_r']}
                AND file.content like ?
            order by {self.order_by} {'ASC' if self.order == Qt.SortOrder.AscendingOrder else 'DESC'}
            limit {self.offset},{self.limits}
            """,
                (
                    f"%{self.where_form['url']}%",
                    f"%{self.where_form['name']}%",
                    f"%{self.where_form['solver_c']}%",
                ),
            )
        )
        self.model.beginResetModel()
        self.model.dats = dats
        self.model.endResetModel()
        return tot

    def find_task(self):
        logger.info(f"Searching begin...")
        psz, pno = 30, 1
        self.offset = 0
        self.limits = psz
        self.tot = self.find()  # TODO
        self.pageSzBox.setSuffix(f"/{self.tot} rows")
        self.pageSzBox.setValue(psz)
        self.pageSzBox.setRange(1, self.tot)
        ptot = max(1, (self.tot + psz - 1) // psz)
        self.pageNoBox.setRange(1, ptot)
        self.pageNoBox.setSuffix(f"/{ptot} pages")
        self.pageNoBox.setValue(pno)
        self.pageSzBox.setEnabled(T)
        self.pageNoBox.setEnabled(T)
        logger.info(f"Searching done.")

    def refresh(self, where_form):
        self.stashButton.setEnabled(F)
        self.pageSzBox.setEnabled(F)
        self.pageNoBox.setEnabled(F)
        # thread_pool.submit(self.find_task)
        self.where_form = where_form
        self.find_task()
        # # self.view.adjustSize()
        # w = 0
        # for idx in range(self.model.columnCount()):
        #     w += self.view.columnWidth(idx)
        # # self.view.setFixedSize(w, max(250, self.view.size().height()))
        # self.view.setBaseSize(w, self.view.height())

    def pagesz_changed(self, v):
        self.pageSzBox.setEnabled(F)
        self.pageNoBox.setEnabled(F)
        self.pageNoBox.blockSignals(T)
        psz, pno = self.pageSzBox.value(), self.pageNoBox.value()
        ptot = max(1, (self.tot + psz - 1) // psz)
        self.pageNoBox.setRange(1, ptot)
        self.pageNoBox.setSuffix(f"/{ptot} pages")
        psz, pno = self.pageSzBox.value(), self.pageNoBox.value()
        self.offset = psz * (pno - 1)
        self.limits = psz
        self.find()
        self.pageSzBox.setEnabled(T)
        self.pageNoBox.setEnabled(T)
        self.pageNoBox.blockSignals(F)

    def pageno_changed(self, v):
        self.pageSzBox.setEnabled(F)
        self.pageNoBox.setEnabled(F)
        psz, pno = self.pageSzBox.value(), self.pageNoBox.value()
        self.offset = psz * (pno - 1)
        self.limits = psz
        self.find()
        self.pageSzBox.setEnabled(T)
        self.pageNoBox.setEnabled(T)

    def drill_in(self, id, val):
        content = db.query(
            (f"select content from file where task_id=? and path=?", (id, val))
        )[0]["content"]
        _, fn = tempfile.mkstemp()
        with open(fn, "w") as w:
            w.write(content)
        self.fileViewer.set_file(fn)
        self.fileViewer.show()

    # db -> disk
    def _stash_task(self):
        rows = list({idx.row() for idx in self.view.selectedIndexes()})
        self.stash_task([self.model.dats[row] for row in rows])
        self.refresh()
        self.stash_task_signal.emit()

    @staticmethod
    def stash_task(task_dicts: List[Dict[str, Any]]):
        for task_dict in task_dicts:
            try:
                task = Task(**task_dict)
                task.solver = File(task.stash_dir(task.solver))
                task.generator = File(task.stash_dir(task.generator))
                task.jurger = File(task.stash_dir(task.jurger))
                task.comp_type = CT(task.comp_type)
                task.tests = []
                for file_dict in db.query(
                    f"select * from file where task_id={task.id}"
                ):
                    with open(File(task.stash_dir(file_dict["path"])).path, "w") as w:
                        w.write(file_dict["content"])
                for test_dict in db.query(
                    f"select * from test where task_id={task.id}"
                ):
                    test = Test()
                    test.id = test_dict["test_id"]
                    test.status = VS(test_dict["status"])
                    test.input_type = IT(test_dict["input_type"])
                    test.answer_type = AT(test_dict["answer_type"])
                    test.input = File(task.test_dir(test.id, "input.txt"))
                    test.answer = File(task.test_dir(test.id, "answer.txt"))
                    task.tests.append(test)
                with open(task.stash_dir("meta.pickle"), "wb") as w:
                    pickle.dump(task, w)
                db.execute(
                    [  # TODO tests/files deleted cascaded ?
                        f"delete from task where id={task.id}",
                        f"delete from test where task_id={task.id}",
                        f"delete from file where task_id={task.id}",
                    ]
                )
            except BaseException as e:
                logger.error(f"Failed to stashed task: {task}!")
                logger.exception(e)
                continue
            logger.info(f"Successfully stashed task: {task}.")

    def select_changed(self, selected, deselected):
        self.stashButton.setEnabled(T if selected else F)

    def show(self) -> None:
        super().show()
        self.raise_()
        self.activateWindow()

    def closeEvent(self, arg__1: QCloseEvent) -> None:
        self.fileViewer.close()
        return super().closeEvent(arg__1)