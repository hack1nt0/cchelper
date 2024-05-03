from PySide6.QtGui import QCloseEvent
from cchelper import *
from cchelper.taskcrawler import TaskCrawler
from .model import TaskModel
from .delegate import TaskDelegate
from .listener import CcListener
from cchelper.taskcreator import TaskCreator
from cchelper.taskfinder import TaskFinder
from .taskbrowser_ui import Ui_TaskBrowser
from .tasktagseditor import TaskTagsEditor
from .tasktestparamseditor import TaskTestParamsEditor
from cchelper.fileeditor import CodeEditorD
import glob


@dataclasses.dataclass
class TaskCondition:
    url: str = None
    name: str = None
    tags: int = 0
    solver: re.Pattern = None
    ctimeL: int = None
    ctimeR: int = None
    status: TS = TS.UNSOLVED


class TaskBrowser(QWidget, Ui_TaskBrowser):
    new_task_signal: Signal = Signal(Task)
    found_task_signal: Signal = Signal(Task)
    found_done_signal: Signal = Signal()
    solve_task_signal: Signal = Signal(Task)
    rename_task_signal: Signal = Signal()

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        windows["taskbrowser"] = self

        #### NEW
        self.newButton.setToolTip("New Task (Ctrl+N)")
        self.newButton.setIcon(QIcon(paths.img("add.png")))
        self.newButton.setShortcut("Ctrl+N")
        self.newButton.clicked.connect(self.new_task_from_input)
        self.crawlButton.setToolTip("Crawl Task")
        self.crawlButton.setIcon(QIcon(paths.img("web-crawler.png")))
        self.crawlButton.clicked.connect(self.new_task_from_crawl)
        self.ccListener: HTTPServer = None
        self.checkBox.setChecked(T)
        self.checkBox.stateChanged.connect(self.start_listener)

        ##### TASKS
        self.model = TaskModel(self)
        self.view.setModel(self.model)
        self.deleg = TaskDelegate(self)
        ### Edit
        self.deleg.edit_tags_signal.connect(self.edit_tags)
        self.deleg.edit_tp_signal.connect(self.edit_tps)
        self.view.setItemDelegate(self.deleg)
        self.view.verticalHeader().setVisible(F)
        self.view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.view.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        self.view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.popup_context_menu)
        self.context_menu = QMenu(self)
        ### Edit SOLVER
        self.edit_solver_act = self.context_menu.addAction(
            "Edit Solver", self.edit_solver
        )
        #### DELETE task
        self.del_task_act = self.context_menu.addAction("Delete Task", self.del_task)

        #### FIND
        self.findButton.setToolTip("Find Task (Ctrl+F)")
        self.findButton.setIcon(QIcon(paths.img("search.png")))
        self.findButton.clicked.connect(self.find_task)
        self.findButton.setShortcut("Ctrl+F")

        self.condition = TaskCondition()
        self.load_killed = threading.Event()
        self.found_task_signal.connect(self.add_task_from_loader)

        self.stopButton.setVisible(F)
        self.stopButton.setShortcut("Shift+Ctrl+F")
        self.stopButton.setToolTip("Stop Search (Shift+Ctrl+F)")
        self.stopButton.setIcon(QIcon(paths.img("stop-button.png")))
        self.stopButton.clicked.connect(lambda: self.load_killed.set())

        def stopped():
            self.stopButton.setVisible(F)
            self.findButton.setVisible(T)

        self.found_done_signal.connect(stopped)

        self.spinBox.setRange(0, 0)

        def jump2page(idx: int):
            self.model.offset = idx - 1
            self.model.refresh()
            self.solve_task_signal.emit(self.task)

        self.spinBox.valueChanged.connect(jump2page)

        # self.nxtpage_key = QShortcut(Qt.Key.Key_PageDown, self)
        # self.nxtpage_key.activated.connect(
        #     lambda: self.spinBox.setValue(self.spinBox.value() + 1)
        # )
        # self.prepage_key = QShortcut(Qt.Key.Key_PageUp, self)
        # self.prepage_key.activated.connect(
        #     lambda: self.spinBox.setValue(self.spinBox.value() - 1)
        # )


    @property
    def task(self) -> Task:
        return self.model.row()

    def start_listener(self, v=T):
        # TODO start/stop cclistener
        if v:
            self.ccListener = HTTPServer(("localhost", 27121), CcListener)
            self.new_task_signal.connect(self.new_task_from_listener)
            global_threadpool.submit(self.ccListener.serve_forever)
            logger.info("Listener started")
        else:
            self.ccListener.shutdown()
            self.ccListener = None
            logger.info("Listener stopped")

    def new_task_from_input(self):
        d = TaskCreator(self)
        if d.exec():
            self.new_task([d.task])

    def new_task_from_crawl(self):
        if TaskCrawler.__name__ not in windows:
            d = TaskCrawler(self)
            d.add_task_signal.connect(self.new_task)
            windows[TaskCrawler.__name__] = d
            d.exec()

    def new_task_from_listener(self, task: Task):
        if TaskCrawler.__name__ not in windows:
            d = TaskCrawler(self)
            d.add_task_signal.connect(self.new_task)
            windows[TaskCrawler.__name__] = d
            d.add_task(task)
            d.exec()
        else:
            windows[TaskCrawler.__name__].add_task(task)

    def new_task(self, tasks: List[Task]):
        news = 0
        for task in tasks:
            try:
                # check dup in db
                if os.path.exists(conf.tasks_dir(task.name)):
                    pass
                else:
                    solver_content = task.solver
                    task.solver = File(task.dir(conf.solver)).create()
                    lang = next(
                        filter(
                            lambda lang: lang.suffix
                            == os.path.splitext(task.solver.path)[1],
                            conf.languages,
                        )
                    )
                    with open(task.solver.path, "w") as w:
                        w.write(lang.template)
                    if solver_content is not None:
                        with open(task.solver.path, "a") as w:
                            w.write(solver_content)
                    # from crawler
                    for test in task.tests:
                        input_content = test.input
                        answer_content = test.answer
                        test.input = File(task.test_dir(test.id, "Input.txt")).create()
                        test.answer = File(
                            task.test_dir(test.id, "Answer.txt")
                        ).create()
                        with open(test.input.path, "w") as w:
                            w.write(input_content)
                        with open(test.answer.path, "w") as w:
                            w.write(answer_content)
                        test.input = File(os.path.relpath(test.input.path, task.dir()))
                        test.answer = File(
                            os.path.relpath(test.answer.path, task.dir())
                        )
                    task.solver = File(os.path.relpath(task.solver.path, task.dir()))
                    task.save()
                    news += 1
            except BaseException as e:
                logger.exception(e)
                continue
        logger.info(f"Successfully created {news} tasks.")

    def find_task(self):
        d = TaskFinder(self, self.condition)
        if d.exec():
            self.stopButton.setVisible(T)
            self.findButton.setVisible(F)
            self.load_killed.clear()
            self.spinBox.blockSignals(T)
            self.spinBox.setRange(0, 0)
            self.spinBox.setSuffix(f" tasks")
            self.model.dats.clear()
            self.model.modelReset.emit()
            self.solve_task_signal.emit(None)
            self.spinBox.blockSignals(F)
            global_threadpool.submit(self.load_tasks)

    def load_tasks(self) -> None:
        try:
            condition = self.condition

            def meet_req(task: Task) -> bool:
                ret = T
                if condition.ctimeL and condition.ctimeR:
                    ret &= condition.ctimeL <= task.ctime <= condition.ctimeR
                ret &= (condition.tags & task.tags) == condition.tags
                if condition.status:
                    ret &= condition.status == task.status
                if condition.url:
                    ret &= condition.url in task.url.lower()
                if condition.name:
                    ret &= condition.name in task.name.lower()
                if condition.solver:
                    ret &= condition.solver in open(task.solver.path).read().lower()
                return ret

            def relative(x: str, task: Task):
                # for name in (task.name, '-'.join(task.name.split('/'))):
                #     start = x.find(name)
                #     if start >= 0:
                #         return x[start+len(task.name):]
                for prefix in ('F/', 'T/', 'V/'):
                    start = x.find(prefix)
                    if start > 0:
                        return x[start:]
                if x.startswith('../'):
                    return os.path.split(x)[-1]
                return x

            solver_pattern = re.compile("^(sol|solver|solution|[a-z])$")
            for root, dns, fns in os.walk(conf.tasks_dir()):
                if self.load_killed.is_set():
                    break
                if os.path.split(root)[-1] == "dist":
                    continue
                root_istask = F
                if "meta.pickle" in fns:
                    with open(os.path.join(root, "meta.pickle"), "rb") as r:
                        task: Task = pickle.load(r)
                        task.name = os.path.relpath(root, conf.tasks_dir())
                        for test in task.tests:
                            match test.input_type:
                                case IT.MANUAL:
                                    test.input = File(relative(test.input.path, task))
                                case IT.GENERATOR:
                                    test.input = File(
                                        relative(
                                            glob.glob(task.dir("F", "Generator.*"))[0], task
                                        )
                                    )
                            match test.answer_type:
                                case AT.MANUAL:
                                    test.answer = File(relative(test.answer.path, task))
                                case AT.JURGER:
                                    test.answer = File(
                                        relative(
                                            glob.glob(task.dir("F", "Jurger.*"))[0], task
                                        )
                                    )
                        task.solver = File(relative(task.solver.path, task))
                        task.save()
                        if meet_req(task):
                            logger.debug(task)
                            self.found_task_signal.emit(task)
                    root_istask = T
                else:
                    for fn in fns:
                        if self.load_killed.is_set():
                            break
                        prefix, suffix = map(lambda s: s.lower(), os.path.splitext(fn))
                        if suffix and solver_pattern.match(prefix):
                            task = Task()
                            task.name = os.path.relpath(root, conf.tasks_dir())
                            task.solver = File(fn)
                            if meet_req(task):
                                self.found_task_signal.emit(task)
                            root_istask = T
                            break
                if root_istask:
                    dns.clear()
            self.found_done_signal.emit()
        except Exception as e:
            logger.exception(e)

    def add_task_from_loader(self, task: Task):
        self.model.dats.append(task)
        tot = len(self.model.dats)
        self.spinBox.setRange(1, tot)
        self.spinBox.setSuffix(f" /{tot} tasks")
        if tot == 1:
            self.model.modelReset.emit()
            self.solve_task_signal.emit(self.task)

    def popup_context_menu(self, point):
        idx = self.view.indexAt(point)
        self.edit_solver_act.setEnabled(idx.isValid())
        self.del_task_act.setEnabled(idx.isValid())
        self.context_menu.popup(QCursor().pos())

    def edit_solver(self):
        w = CodeEditorD(self)
        w.set_file(self.task.solver)
        w.exec()

    def edit_tps(self):
        if TaskTestParamsEditor(self, self.model).exec():
            self.solve_task_signal.emit(self.task)

    def edit_tags(self):
        oldname = self.task.name
        if TaskTagsEditor(self, self.model).exec():
            self.solve_task_signal.emit(self.task)
            if self.task.name != oldname:
                self.rename_task_signal.emit()

    def del_task(self):
        task = self.task
        if (
            ConfirmBox(self, f"Are you sure to delete those {str(task)}").exec()
            == ConfirmBox.YES
        ):
            task.remove()
            self.model.del_dat()
            self.view.setFocus()
            logger.info(f"Successfully deleted task: {str(task)}.")
        
    def closeEvent(self, event: QCloseEvent) -> None:
        if self.ccListener:
            self.ccListener.shutdown()
        return super().closeEvent(event)
