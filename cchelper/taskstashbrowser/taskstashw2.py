from PySide6.QtGui import QShowEvent
from cchelper import *
from cchelper.taskcrawler import TaskCrawler
from .taskstashw_ui import Ui_TaskStashW
from .model import TaskModel
from .delegate import TaskDelegate
from cchelper.taskarxivbrowser import TaskArxivBrowser
from cchelper.logviewer import LogViewer
from .listener import CcListener
from cchelper.taskcreator import TaskCreator
from cchelper.taskeditor import TaskEditor, TestParamsEditor
from cchelper.confform import ConfForm
from cchelper.taskfinder import TaskFinder
from cchelper.fileeditor import CodeEditor
# import cchelper.taskstashbrowser.test as TestService
import cchelper.taskstashbrowser.testasync as TestService
from cchelper.testbrowser import TestBrowser
from cchelper.filebrowser import FileBrowser
from cchelper.langbrowser import LangBrowser
from cchelper.tagbrowser import TagBrowser
from cchelper.tasksubmitter import FileSubmitter, CodeSubmitter
import glob
from pathlib import Path

class TaskStashW(QMainWindow, Ui_TaskStashW):
    add_task_signal: Signal = Signal(Task)
    resize_signal: Signal = Signal()

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        # self.comboBox.setStyleSheet("background: blue; color : white; font: bold;")
        self.comboBox.addItems(["a"] * 10)

        # self.setWindowFlags(Qt.WindowStaysOnTopHint)

        logger.status_bar = self.statusbar

        windows[self.__class__.__name__] = self  # TODO

        #### SETTING
        self.settingButton.setToolTip("Settings/Tools (Ctrl+,)")
        self.settingButton.setShortcut("Ctrl+,")
        self.settingButton.setIcon(QIcon(paths.img("setting.png")))
        # self.settingButton.clicked.connect(self.setting)
        self.settingMenu = QMenu(self)
        self.setting_general_act = self.settingMenu.addAction("General")
        self.setting_general_act.triggered.connect(self.setting)
        self.setting_language_act = self.settingMenu.addAction("Languages")
        self.setting_language_act.triggered.connect(lambda: LangBrowser(self).exec())
        self.setting_tag_act = self.settingMenu.addAction("Tags")
        self.setting_tag_act.triggered.connect(lambda: TagBrowser(self).exec())
        self.setting_log_act = self.settingMenu.addAction(
            QIcon(paths.img("footprints.png")), "Show Log"
        )
        self.setting_log_act.triggered.connect(lambda: LogViewer(self).show())
        self.setting_about_act = self.settingMenu.addAction(
            "About", lambda: QDesktopServices.openUrl("https://www.baidu.com")
        )  # TODO
        self.settingButton.setMenu(self.settingMenu)
        self.settingButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        #### FIND
        self.findButton.setToolTip("Find Task (Ctrl+F)")
        self.findButton.setIcon(QIcon(paths.img("search.png")))
        # self.findButton.clicked.connect(self.find_task)
        self.findButton.setShortcut("Ctrl+F")
        self.findMenu = QMenu(self)
        self.find_table_act = self.findMenu.addAction("Table", self.find_task)
        self.find_chart_act = self.findMenu.addAction("Chart")
        self.findButton.setMenu(self.findMenu)
        self.findButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        # self.findButton.clicked.connect(self.find_task)

        #### NEW
        self.newButton.setToolTip("New Task (Ctrl+N)")
        self.newButton.setIcon(QIcon(paths.img("add.png")))
        self.newButton.setShortcut("Ctrl+N")
        self.newMenu = QMenu(self)
        self.newOpts = QActionGroup(self)
        self.new_taskform_act = self.newMenu.addAction("Manual")
        self.new_taskform_act.triggered.connect(self.new_task_from_input)
        self.new_taskcrawl_act = self.newMenu.addAction("Crawl")
        self.new_taskcrawl_act.triggered.connect(self.new_task_from_crawl)
        self.newMenu.addSeparator()
        self.new_taskcc_act = self.newMenu.addAction("Competitive Companion")
        self.new_taskcc_act.setCheckable(T)
        self.new_taskcc_act.setChecked(T)
        self.new_taskcc_act.triggered.connect(self.start_listener)
        # act.triggered.emit()
        self.add_task_signal.connect(self.add_task_from_listener)
        self.newButton.setMenu(self.newMenu)
        self.newButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        #### DELETE
        self.delButton.setToolTip("Delete Task (Ctrl+D)")
        self.delButton.setIcon(QIcon(paths.img("delete.png")))
        self.delButton.setShortcut("Ctrl+D")
        self.delButton.clicked.connect(self.del_task)

        ##### TASKS
        self.tasks: List[Task] = None
        self.model = TaskModel(self)
        self.comboBox.setModel(self.model)
        self.comboBox.currentTextChanged.connect(self.change_task)
        self.data_mapper = QDataWidgetMapper(self)
        self.data_mapper.setModel(self.model)
        self.deleg = TaskDelegate(self)
        self.data_mapper.setItemDelegate(self.deleg)

        self.task_menu_key = QShortcut(QKeySequence("Ctrl+L"), self)
        self.task_menu_key.activated.connect(self.comboBox.showPopup)

        self.PButton.clicked.connect(
            lambda: TestParamsEditor(
                self.model, self.comboBox.currentIndex(), self
            ).open()
        )
        self.PButton.setShortcut("F8")
        self.PButton.setToolTip("Test related parameters (F8)")
        # self.FBrowser = FileBrowser(self)
        # self.FButton.clicked.connect()
        self.SButton.setShortcut("F9")
        self.SButton.clicked.connect(
            lambda: CodeEditor(
                os.path.relpath(self.task.solver.path, self.task.file_dir()), self
            ).open()
        )
        self.SButton.setToolTip("Solver (F9)")
        self.GButton.setShortcut("F10")
        self.GButton.clicked.connect(
            lambda: CodeEditor(
                os.path.relpath(self.task.generator.path, self.task.file_dir()), self
            ).open()
        )
        self.GButton.setToolTip("Generator (F10)")
        self.JButton.setShortcut("F11")
        self.JButton.clicked.connect(
            lambda: CodeEditor(
                os.path.relpath(self.task.jurger.path, self.task.file_dir()), self
            ).open()
        )
        self.JButton.setToolTip("Jurger (F11)")
        # self.TBrowser = TestBrowser(self)
        # self.TButton.clicked.connect(lambda: TestBrowser(self.task, self).open())
        # self.TButton.setShortcut("F10")
        # self.CBrowser = ChartWidget(self)
        # self.CButton.clicked.connect(lambda: ChartWidget(self.task, self).open())
        # self.CButton.setShortcut('F11')

        ##### I/O
        # self.inputButton.setToolTip("Input")
        # self.inputButton.setIcon(QIcon(path.img("documents.png")))
        # self.inputButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        # self.outputButton.setToolTip("Output")
        # self.outputButton.setIcon(QIcon(path.img("verdict.png")))
        # self.outputButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        # self.chartButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        # self.chartButton.setIcon(QIcon(path.img("pie-chart.png")))
        # self.switch_FT_sc = QShortcut("Alt+Tab", self)
        # self.switch_FT_sc.activated.connect(self.switch_panels)
        # self.switch_buttons = [self.inputButton, self.outputButton, self.chartButton]
        # # self.splitter.setSizes([1, 0])
        # self.inputButton.clicked.emit()
        # self.FButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        # self.VButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        # self.CButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        # self.FButton.setChecked(T)
        # self.tab_acts = QActionGroup(self)
        # self.i_tab_act = self.tab_acts.addAction(self.toolBar2.addAction(QIcon(path.img("documents.png")), 'Input', lambda: self.stackedWidget.setCurrentIndex(0)))
        # self.i_tab_act.setCheckable(T)
        # self.i_tab_act.setChecked(T)
        # self.o_tab_act = self.tab_acts.addAction(self.toolBar2.addAction(QIcon(path.img("verdict.png")), 'Output', lambda: self.stackedWidget.setCurrentIndex(1)))
        # self.o_tab_act.setCheckable(T)
        # self.c_tab_act = self.tab_acts.addAction(self.toolBar2.addAction(QIcon(path.img("pie-chart.png")), 'Chart', lambda: self.stackedWidget.setCurrentIndex(2)))
        # self.c_tab_act.setCheckable(T)
        # self.toolBar.addSeparator()

        ##### TEST

        self.buildButton.setShortcut("F4")
        self.buildButton.setToolTip("Build/Compile (F4)")
        self.buildButton.setIcon(QIcon(paths.img("hammer.png")))
        self.buildButton.clicked.connect(self.run_compile)
        self.runButton.setShortcut("F5")
        self.runButton.setToolTip("Start (F5)")
        self.runButton.setIcon(QIcon(paths.img("play-button.png")))
        self.runButton.clicked.connect(self.run_execute)
        self.stopButton.setShortcut("Shift+F5")
        self.stopButton.setToolTip("Stop (Shift+F5)")
        self.stopButton.setIcon(QIcon(paths.img("stop-button.png")))
        self.stopButton.clicked.connect(self.run_terminate)
        self.compiling = F
        self.executing = F
        self.compile_tasks = []
        self.execute_tasks = []
        self.stop_flag = None

        #### SUBMIT
        self.submitButton.setShortcut("F6")
        self.submitButton.setToolTip("Submit (F6)")
        self.submitButton.setIcon(QIcon(paths.img("send.png")))
        self.submitButton.clicked.connect(self.submit_task)

        #### ARXIV
        self.arxivButton.setToolTip("Arxiv task (F7)")
        self.arxivButton.setIcon(QIcon(paths.img("check-mark.png")))
        self.arxivButton.setShortcut("F7")
        self.arxivButton.clicked.connect(self.arxiv_task)

        #### STAT
        # self.SViewer.setMaximumHeight(300)

        #### Interactive
        # self.VBrowser.view.selectionModel().currentRowChanged.connect(
        #     self.select_test_from_verdict
        # )

    def setting(self):
        d = ConfForm(self)
        d.exec()

    def find_task(self):
        d = TaskFinder(self)
        if d.exec():
            # w = popup_window(TaskArxivBrowser, self)
            w = TaskArxivBrowser(d.form, self)
            w.stash_task_signal.connect(self.refresh_tasks)
            w.open()

    def refresh_tasks(self):
        self.model.beginResetModel()
        self.tasks = Task.load()
        self.model.dats = self.tasks
        self.model.endResetModel()
        if not self.tasks:
            for w in self.all_widgets:
                w.setEnabled(F)
            self.settingButton.setEnabled(T)
            self.findButton.setEnabled(T)
            self.newButton.setEnabled(T)
            logger.info("No tasks found.")
        else:
            for w in self.all_widgets:
                w.setEnabled(T)

    @property
    def task(self) -> Task | None:
        try:
            return self.tasks[self.comboBox.currentIndex()]
        except:
            return

    @property
    def all_widgets(self):
        return (
            self.settingButton,
            self.findButton,
            self.newButton,
            self.delButton,
            self.arxivButton,
            self.comboBox,
            self.PButton,
            self.SButton,
            self.GButton,
            self.JButton,
            self.view,
            self.buildButton,
            self.runButton,
            self.stopButton,
            self.submitButton,
        )

    def change_task(self, name: str):
        if self.task is None:
            for w in self.all_widgets:
                w.setEnabled(F)
            self.settingButton.setEnabled(T)
            self.findButton.setEnabled(T)
            self.newButton.setEnabled(T)
            logger.info("No tasks found.")
            return
        paths.remove_symlink(conf.working_dir())
        os.symlink(
            paths.data("stash", str(self.task), "F"),
            conf.working_dir(),
            target_is_directory=T,
        )
        os.chdir(conf.working_dir())
        self.view.setData(self.task)
        for w in self.all_widgets:
            w.setEnabled(T)
        logger.info(f"Switched to task: {self.task}.")

    def arxiv_task(self):
        d = TaskEditor(self.model, self.comboBox.currentIndex(), self)
        if d.exec():
            task_name = self.task.name
            for w in self.all_widgets:
                w.setEnabled(F)
            self.task.arxiv()
            shutil.rmtree(self.task.stash_dir())
            self.refresh_tasks()
            logger.info(f"Successfully archived task: {task_name}.")

    def start_listener(self, v=T):
        # TODO start/stop cclistener
        if v:
            self.ccListener = HTTPServer(("localhost", 27121), CcListener)
            global_threadpool.submit(self.ccListener.serve_forever)
            logger.info("Listener started")
        else:
            self.ccListener.shutdown()
            self.ccListener = None
            logger.info("Listener stopped")

    def new_task_from_input(self):
        d = TaskCreator(self)
        if d.exec():
            self.add_task([d.task])

    def new_task_from_crawl(self):
        if TaskCrawler.__name__ not in windows:
            d = TaskCrawler(self)
            d.add_task_signal.connect(self.add_task)
            windows[TaskCrawler.__name__] = d
            d.exec()

    def add_task_from_listener(self, task: Task):
        if TaskCrawler.__name__ not in windows:
            d = TaskCrawler(self)
            d.add_task_signal.connect(self.add_task)
            windows[TaskCrawler.__name__] = d
            d.add_task(task)
            d.exec()
        else:
            windows[TaskCrawler.__name__].add_task(task)

    def add_task(self, tasks: List[Task]):
        for task in tasks:
            try:
                # check dup in db
                old = db.query(
                    (
                        f"select * from task where name=?",
                        (task.name,),
                    )
                )
                if old:
                    TaskArxivBrowser.stash_task(old)
                    self.refresh_tasks()
                    logger.info(f"Successfully created task: {task}: arxiv -> stash")
                    continue
                # check dup in disk
                if os.path.isdir(task.stash_dir()):
                    logger.info(f"Successfully created task: {task}: stash -> stash")
                    continue
                else:
                    solver_content = task.solver
                    task.solver = File(task.file_dir(conf.solver))
                    task.generator = File(task.file_dir(conf.generator))
                    task.jurger = File(task.file_dir(conf.jurger))
                    for fn in map(
                        lambda file: file.path,
                        [task.solver, task.generator, task.jurger],
                    ):
                        lang = next(
                            filter(
                                lambda lang: lang.suffix == os.path.splitext(fn)[1],
                                conf.languages,
                            )
                        )
                        with open(fn, "w") as w:
                            w.write(lang.template)
                    if solver_content is not None:
                        with open(task.solver.path, 'a') as w:
                            w.write(solver_content)
                    # from crawler
                    for test in task.tests:
                        input_content = test.input
                        answer_content = test.answer
                        test.input = File(task.test_dir(test.id, "input.txt"))
                        test.answer = File(task.test_dir(test.id, "answer.txt"))
                        with open(test.input.path, "w") as w:
                            w.write(input_content)
                        with open(test.answer.path, "w") as w:
                            w.write(answer_content)
                    task.dump()
                    self.model.beginResetModel()
                    self.tasks.append(task)
                    self.model.endResetModel()
                    logger.info(f"Successfully created task: {task}: new.")
            except BaseException as e:
                logger.exception(e)
                logger.error(f"Failed to creat task: {task}.")
                continue

    def del_task(self):
        if (
            ConfirmBox(self, f"Are you sure to delete task: {self.task} ?").exec()
            == ConfirmBox.YES
        ):
            task_name = self.task.name
            for w in self.all_widgets:
                w.setEnabled(F)
            paths.remove_symlink(conf.working_dir())
            shutil.rmtree(self.task.stash_dir())
            self.refresh_tasks()
            logger.info(f"Successfully deleted task: {task_name}.")

    def run_pre(self):
        for w in self.all_widgets:
            w.setEnabled(F)
        self.view.setEnabled(T)
        self.stopButton.setEnabled(T)
        self.PButton.setEnabled(T)
        self.SButton.setEnabled(T)
        self.GButton.setEnabled(T)
        self.JButton.setEnabled(T)
        self.settingButton.setEnabled(T)
        if os.path.exists(self.task.verdict_dir()):
            shutil.rmtree(self.task.verdict_dir())
        self.task.verdicts.clear()
        # self.stop_flag = threading.Event()
        global_stopflag.clear()
        self.thread_pool = ThreadPoolExecutor(max_workers=conf.parallel)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run_refresh)
        self.timer.setInterval(1000 // conf.refresh_rate)
        self.refresh_busy = F
        self.timer.start()
        logger.info(f"Timer started.")

    def run_compile(self):
        self.run_pre()
        if self.executing:
            logger.info(f"Execution started.")
        else:
            self.compiling = T
            logger.info(f"Compilation started.")

        for file in [self.task.solver, self.task.generator, self.task.jurger]:
            vid = len(self.task.verdicts)
            verdict = Verdict(
                id=vid,
                test_id=None,
                status=VS.COMPILATION_QUE,
                stderr=File(self.task.verdict_dir(vid, "stderr.txt")),
            )
            self.task.verdicts.append(verdict)
            if len(file) == 0:  # TODO file empty
                verdict.status = VS.COMPILATION_SKP
                continue
            task = self.thread_pool.submit(
                TestService.compile_one,
                verdict=verdict,
                file=file,
                build_asneed=conf.build_asneed,
            )
            self.compile_tasks.append(task)

    def run_execute(self):
        self.executing = T
        self.run_compile()

    def run_refresh(self):
        if self.refresh_busy:
            return
        self.refresh_busy = True
        #
        # Compile
        #
        if self.compiling:
            finished = all((task.done() for task in self.compile_tasks))
            self.view.refresh()
            if finished:
                self.run_post()
                logger.info(f"Compilation Stopped.")
                return
        #
        # Run Tests
        #
        elif self.executing:
            if self.compile_tasks:
                finished = all((task.done() for task in self.compile_tasks))
                self.view.refresh()
                if finished:
                    self.compile_tasks.clear()
                    if not all(self.task.verdicts):
                        self.run_post()
                        logger.info(
                            f"Compilation Stopped with failures, execution skipped."
                        )
                        return
                    if os.path.exists(self.task.verdict_dir()):
                        shutil.rmtree(self.task.verdict_dir())
                    self.task.verdicts.clear()
                    self.tests: List[Test] = []
                    for old in filter(lambda test: test.checked, self.task.tests):
                        new = Test()
                        new.status = VS.QUE
                        new.input_type = old.input_type
                        new.input = old.input
                        new.answer_type = old.answer_type
                        new.answer = old.answer
                        new.id = old.id
                        if old.input_type == IT.GENERATOR:
                            new.input = self.task.generator
                        if old.answer_type in (AT.JURGER, AT.INTERACTIVE_JURGER):
                            new.answer = self.task.jurger
                        if old.input_type == IT.GENERATOR:
                            self.tests += [new] * self.task.gcount
                        else:
                            self.tests.append(new)
                    for test in self.tests:
                        tid = test.id
                        vid = len(self.task.verdicts)
                        verdict = None #TODO
                        if test.answer_type == AT.INTERACTIVE_JURGER:
                            verdict = Verdict(
                                id=vid,
                                test_id=tid,
                                status=VS.QUE,
                                input=File(self.task.verdict_dir(vid, "input.txt")),
                                chat=File(self.task.verdict_dir(vid, "chat.txt")),
                                stderr=File(self.task.verdict_dir(vid, "stderr.txt")),
                            )
                        else:
                            verdict = Verdict(
                                id=vid,
                                test_id=tid,
                                status=VS.QUE,
                                input=File(self.task.verdict_dir(vid, "input.txt")),
                                answer=File(self.task.verdict_dir(vid, "answer.txt")),
                                actual=File(self.task.verdict_dir(vid, "actual.txt")),
                                stderr=File(self.task.verdict_dir(vid, "stderr.txt")),
                            )
                        self.task.verdicts.append(verdict)
                        task = self.thread_pool.submit(
                            TestService.test_one,
                            verdict=verdict,
                            solver=self.task.solver,
                            test=test,
                            cpu_upbound=self.task.cpu,
                            mem_upbound=self.task.mem,
                            qry_upbound=self.task.qry,
                            comp_type=self.task.comp_type,
                        )
                        self.execute_tasks.append(task)
            else:
                finished = all((task.done() for task in self.execute_tasks))
                self.view.refresh()
                if finished:
                    self.run_post()
                    logger.info(f"Execution Stopped.")
                    return

        self.refresh_busy = False

    def run_post(self):
        if self.compiling or self.executing:
            self.thread_pool.shutdown(wait=T, cancel_futures=T)
            self.timer.stop()
            self.thread_pool = None
            # self.stop_flag = None
            global_stopflag.clear()
            self.timer = None
            self.compiling = F
            self.executing = F
            self.compile_tasks.clear()
            self.execute_tasks.clear()
            for verdict in self.task.verdicts:
                if verdict.test_id is not None: #TODO generator type
                    self.task.tests[verdict.test_id].status = verdict.status
            for w in self.all_widgets:
                w.setEnabled(T)

    def run_terminate(self):
        if self.compiling or self.executing:
            logger.info(f"Terminating...")
            global_stopflag.set()

    def submit_task(self):
        if conf.submit_code:
            d = CodeSubmitter(self.task.solver, self)
        else:
            d = FileSubmitter(self)
        d.exec()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.run_terminate()
        self.run_post()
        self.ccListener.shutdown()
        for task in self.tasks:
            task.dump()
        return super().closeEvent(event)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.resize_signal.emit()
        super().resizeEvent(event)
