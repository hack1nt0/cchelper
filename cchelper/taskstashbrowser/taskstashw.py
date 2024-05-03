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
# from cchelper.taskeditor import TaskEditor, TestParamsEditor
from cchelper.confform import ConfForm
from cchelper.taskfinder import TaskFinder

# import cchelper.taskstashbrowser.test as TestService
import cchelper.taskstashbrowser.testasync as TestService
# from cchelper.testbrowser import TestBrowser
from cchelper.langbrowser import LangBrowser
from cchelper.tagbrowser import TagBrowser
from cchelper.tasksubmitter import CodeSubmitter
import glob
from pathlib import Path
from .statemachines import statemachine_of_build, statemachine_of_run
from cchelper.verdictbrowser import VerdictBrowser

# from cchelper.terminal.ipython import IPythonConsole


class TaskStashW(QMainWindow, Ui_TaskStashW):
    add_task_signal: Signal = Signal(Task)
    arxiv_task_signal: Signal = Signal()

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
        self.setting_reset_act = self.settingMenu.addAction("RESET", self.reset)
        self.settingButton.setMenu(self.settingMenu)
        self.settingButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        self.logButton.setToolTip("Show Log")
        self.logButton.clicked.connect(lambda: LogViewer(None).show())
        self.logButton.setIcon(QIcon(paths.img("footprints.png")))
        self.F1Button.setToolTip("Help")
        self.F1Button.clicked.connect(
            lambda: QDesktopServices.openUrl(
                "https://time-oviraptor-66c.notion.site/cchelper-a8b256d6d2534c609f04d15a7f8e95f0"
            )
        )
        self.F1Button.setToolTip("Help")
        self.F1Button.setShortcut("F1")
        self.F1Button.setIcon(QIcon(paths.img("question.png")))

        #### FIND
        self.findButton.setToolTip("Find Task (Ctrl+F)")
        self.findButton.setIcon(QIcon(paths.img("search.png")))
        self.findButton.clicked.connect(self.find_task)
        self.findButton.setShortcut("Ctrl+F")
        self.arxivBrowser = TaskArxivBrowser(self)
        self.arxivBrowser.stash_task_signal.connect(self.refresh_tasks)
        self.arxiv_task_signal.connect(self.arxivBrowser.refresh)
        self.arxivBrowser.hide()

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

        self.tabs = [self.SButton, self.GButton, self.JButton]
        self.SButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.GButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.JButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.tab_shortcut = QShortcut("Alt+Tab", self)
        self.tab_shortcut.activated.connect(self.switch_tab)

        ##### TEST

        self.TCButton.clicked.connect(self.open_tcs)

        self.buildButton.setShortcut("F4")
        self.buildButton.setToolTip("Build/Compile (F4)")
        self.buildButton.setIcon(QIcon(paths.img("hammer.png")))
        self.buildButton.clicked.connect(self.build_task)
        self.runButton.setShortcut("F5")
        self.runButton.setToolTip("Start (F5)")
        self.runButton.setIcon(QIcon(paths.img("play-button.png")))
        self.runButton.clicked.connect(self.run_task)
        self.stopButton.setShortcut("Shift+F5")
        self.stopButton.setToolTip("Stop (Shift+F5)")
        self.stopButton.setIcon(QIcon(paths.img("stop-button.png")))
        self.stopButton.clicked.connect(self.terminate_task)

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

        self.VBrowser = VerdictBrowser(self)
        self.VBrowser.hide()
        self.VButton.clicked.connect(self.VBrowser.show)

        # self.pyButton.clicked.connect(self.open_console)
        # self.console = None

    def switch_tab(self):
        for idx, tab in enumerate(self.tabs):
            if tab.isChecked():
                self.tabs[(idx + 1) % 3].animateClick()
                break

    def setting(self):
        d = ConfForm(self)
        if self.task:
            self.task.arxiv()
        d.exec()
        if self.task:
            self.task.stash()

    def find_task(self):
        d = TaskFinder(self)
        if d.exec():
            # w = popup_window(TaskArxivBrowser, self)
            self.arxivBrowser.find_signal.emit(d.form)
            self.arxivBrowser.show()

    def refresh_tasks(self):
        self.model.beginResetModel()
        self.tasks = Task.load()
        self.tasks.sort(key=lambda task: task.name)
        self.model.dats = self.tasks
        self.model.endResetModel()
        if not self.tasks:
            for w in self.all_btns:
                w.setEnabled(F)
            self.stackedWidget.setEnabled(F)
            self.settingButton.setEnabled(T)
            self.findButton.setEnabled(T)
            self.newButton.setEnabled(T)
            logger.info("No tasks found.")
        # else:
        #     for w in self.all_widgets:
        #         w.setEnabled(T)

    @property
    def task(self) -> Task | None:
        try:
            return self.tasks[self.comboBox.currentIndex()]
        except:
            return

    @property
    def all_btns(self):
        return (
            self.settingButton,
            self.findButton,
            self.newButton,
            self.delButton,
            self.arxivButton,
            self.comboBox,
            self.buildButton,
            self.runButton,
            self.stopButton,
            self.submitButton,
            self.TCButton,
        )

    @property
    def all_editors(self):
        return (
            self.SEditor,
            self.GEditor,
            self.JEditor,
        )

    def change_task(self, name: str):
        if self.task is None:
            for w in self.all_btns:
                w.setEnabled(F)
            self.settingButton.setEnabled(T)
            self.findButton.setEnabled(T)
            self.newButton.setEnabled(T)
            self.stackedWidget.setEnabled(F)
            self.VBrowser.clear()
            logger.info("No tasks found.")
            return
        self.task.stash()
        self.SEditor.set_file(self.task.solver)
        self.GEditor.set_file(self.task.generator)
        self.JEditor.set_file(self.task.jurger)
        self.VBrowser.set_task(self.task)
        for w in self.all_btns:
            w.setEnabled(T)
        self.stopButton.setEnabled(F)
        self.stackedWidget.setEnabled(T)
        logger.info(f"Switched to task: {self.task}.")

    def arxiv_task(self):
        d = TaskEditor(self.model, self.comboBox.currentIndex(), self)
        if d.exec():
            task_name = self.task.name
            for w in self.all_btns:
                w.setEnabled(F)
            self.task.arxiv()
            self.task.arxiv()
            shutil.rmtree(self.task.stash_dir())
            self.refresh_tasks()
            self.arxiv_task_signal.emit()
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
                        with open(task.solver.path, "a") as w:
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
                    self.tasks.append(task)
                    logger.info(f"Successfully created task: {task}: new.")
            except BaseException as e:
                logger.exception(e)
                logger.error(f"Failed to creat task: {task}.")
                continue
        self.model.beginResetModel()
        self.tasks.sort(key=lambda task: task.name)
        self.model.endResetModel()

    def del_task(self):
        if (
            ConfirmBox(self, f"Are you sure to delete task: {self.task} ?").exec()
            == ConfirmBox.YES
        ):
            task_name = self.task.name
            for w in self.all_btns:
                w.setEnabled(F)
            self.task.arxiv()
            shutil.rmtree(self.task.stash_dir())
            self.refresh_tasks()
            logger.info(f"Successfully deleted task: {task_name}.")

    def open_tcs(self):
        d = TestBrowser(self.model, self.comboBox.currentIndex(), self)
        d.exec()

    def pre_task(self):
        for w in self.all_btns:
            w.setEnabled(F)
        self.stopButton.setEnabled(T)
        self.settingButton.setEnabled(T)
        global_stopflag.clear()
        try:
            idx = [
                idx
                for idx in range(self.tabWidget.count())
                if self.tabWidget.tabText(idx).startswith("Test")
            ][0]
            self.tabWidget.setCurrentIndex(idx)
        except:
            pass
        # self.VBrowser.show()

    def build_task(self):
        self.machine = statemachine_of_build(self.task, [self.VBrowser])
        self.machine.started.connect(self.pre_task)
        self.machine.finished.connect(self.post_task)
        self.machine.start()

    def run_task(self):
        self.machine = statemachine_of_run(self.task, [self.VBrowser])
        self.machine.started.connect(self.pre_task)
        self.machine.finished.connect(self.post_task)
        self.machine.start()

    def post_task(self):
        for verdict in self.task.verdicts:
            if verdict.test_id is not None:  # TODO generator type
                self.task.tests[verdict.test_id].status = verdict.status
        for w in self.all_btns:
            w.setEnabled(T)
        self.stopButton.setEnabled(F)

    def terminate_task(self):
        logger.info(f"Terminating...")
        global_stopflag.set()

    def submit_task(self):
        d = CodeSubmitter(self.task.solver, self)
        d.exec()

    def reset(self):
        d = ConfirmBox(self, f"RESET will delete **ALL** data, continue ?")
        d.NButton.setDefault(T)
        if d.exec() == ConfirmBox.YES:
            db.reset()
            conf.reset()
            shutil.rmtree(paths.stash_dir())
            self.refresh_tasks()

    # def open_console(self):
    #     if self.console is None:
    #         self.console = IPythonConsole(self)
    #     self.console.show()

    def closeEvent(self, event: QCloseEvent) -> None:
        # self.terminate_task()
        # self.post_task()
        # if self.machine is not None:
        #     self.machine.stop()
        # if self.task:
        #     self.task.remove_symlinks()
        try:
            shutil.rmtree(conf.working_dir())
        except:
            pass
        self.ccListener.shutdown()
        for task in self.tasks:
            task.dump()
        # if self.console is not None:
        #     self.console.shutdown_kernel()
        return super().closeEvent(event)
