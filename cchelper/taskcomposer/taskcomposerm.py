from PySide6.QtGui import QCloseEvent
from cchelper import *
from cchelper.taskbrowser.model import TaskModel
from cchelper.tasksubmitter import CodeSubmitter
from .statemachines import statemachine_of_build, statemachine_of_run
from cchelper.fileeditor.codeeditor import CodeEditor
from cchelper.fileviewer import FileViewerD
from cchelper.fileeditor import CodeEditorD
from cchelper.settings import Settings
from cchelper.gviewer import GViewer
from .taskcomposerm_ui import Ui_TaskComposerM


class TaskComposerM(QMainWindow, Ui_TaskComposerM):

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        logger.status_bar = self.statusbar

        def switch_tab():
            cur = self.tabWidget.currentIndex()
            nxt = (cur + 1) % self.tabWidget.count()
            self.tabWidget.setCurrentIndex(nxt)

        self.tab_shortcut = QShortcut("Alt+Tab", self)
        self.tab_shortcut.activated.connect(switch_tab)

        def switch_stack():
            cur = self.stackedWidget.currentIndex()
            nxt = (cur + 1) % self.stackedWidget.count()
            self.stackedWidget.setCurrentIndex(nxt)
            self.terminalButton.setVisible(nxt == 0)
            self.dbButton.setVisible(nxt == 1)

        # self.stack_shortcut = QShortcut("Alt+O", self)
        # self.stack_shortcut.activated.connect(switch_stack)
        self.terminalButton.setIcon(QIcon(paths.img("terminal.png")))
        self.terminalButton.setShortcut("Alt+O")
        self.terminalButton.clicked.connect(switch_stack)
        self.dbButton.setIcon(QIcon(paths.img("database.png")))
        self.dbButton.setShortcut("Alt+O")
        self.dbButton.clicked.connect(switch_stack)
        self.dbButton.setVisible(F)

        ### HELP
        self.helpButton.setToolTip("Help (F1)")
        self.helpButton.setShortcut("F1")
        self.helpButton.setIcon(QIcon(paths.img("question.png")))

        ### SETTING
        self.settingButton.setToolTip("Settings/Tools (Ctrl+,)")
        self.settingButton.setShortcut("Ctrl+,")
        self.settingButton.setIcon(QIcon(paths.img("setting.png")))
        self.settingButton.clicked.connect(lambda: Settings(self).exec())
        self.helpButton.clicked.connect(
            lambda: QDesktopServices.openUrl(
                "https://time-oviraptor-66c.notion.site/cchelper-a8b256d6d2534c609f04d15a7f8e95f0"
            )
        )

        def solve_task(task: Task):
            if task is None:
                self.setWindowTitle("Cchelper")
                for w in self.all_btns:
                    w.setEnabled(F)
                for w in self.all_tabs:
                    w.setEnabled(F)
                self.helpButton.setEnabled(T)
                self.settingButton.setEnabled(T)
                self.taskBrowser.setEnabled(T)
                self.terminal.new_shell(conf.tasks_dir())
                os.chdir(conf.tasks_dir())
                if self.task is not None:
                    self.task.save()
                self.solveButton.setStyleSheet('')
            else:
                if self.task is None or self.task.name != task.name:
                    self.setWindowTitle(os.path.basename(task.name))
                    for w in self.all_btns:
                        w.setEnabled(T)
                    for w in self.all_tabs:
                        w.setEnabled(T)
                    self.testBrowser.set_task(task)
                    self.verdictBrowser.set_task(task)
                    self.terminal.new_shell(task.dir())
                    os.chdir(task.dir())
                match task.status:
                    case TS.SOLVED:
                        self.solveButton.setStyleSheet('background-color: green')
                    case TS.UNSOLVED:
                        self.solveButton.setStyleSheet('background-color: red')
                    case TS.UNSURE:
                        self.solveButton.setStyleSheet('')
            if self.task is not None:
                self.task.save()
            self.task = task
        
        def task_renamed():
            self.setWindowTitle(os.path.basename(self.task.name))
            self.terminal.new_shell(self.task.dir())

        self.taskBrowser.solve_task_signal.connect(solve_task)
        self.taskBrowser.rename_task_signal.connect(task_renamed)

        self.verdictBrowser.view_file_signal.connect(self.view_file)

        ##### TASKS
        self.task: Task = None
        self.taskBrowser.start_listener()
        self.solveButton.setIcon(QIcon(paths.img("check-mark.png")))
        self.solveButton.clicked.connect(lambda: self.edit_file(self.task.solver))

        ### FILES
        self.fileBrowser.set_root(File(conf.project_dir))
        self.fileBrowser.edit_file_signal.connect(self.edit_file)

        ##### TEST

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
        self.stopButton.setVisible(F)

        #### SUBMIT
        self.submitButton.setShortcut("F6")
        self.submitButton.setToolTip("Submit (F6)")
        self.submitButton.setIcon(QIcon(paths.img("send.png")))
        self.submitButton.clicked.connect(self.submit_task)

        ### GRAPH
        self.graphViewer = GViewer(self)
        self.graphViewer.hide()
        self.graphButton.clicked.connect(self.graphViewer.show)
        self.graphButton.setIcon(QIcon(paths.img("data-analytics.png")))
        self.verdictBrowser.view_graph_signal.connect(self.graphViewer.set_file)

        ### Terminal
        windows["terminal"] = self.terminal

        solve_task(None)

    def set_model(self, model, idx):
        self.model = model
        self.idx = idx
        self.task = model.row(idx)
        self.setWindowTitle(str(self.task))
        # self.task.create_symlinks() #TODO
        # self.SEditor.set_file(self.task.solver)
        # self.SEditor.set_file(self.task.solver)
        self.VBrowser.set_data(self.task)
        self.CViewer.set_data(self.task)
        self.TEditor.set_model(self.model, self.idx)

    def edit_file(self, file: File) -> None:
        if len(file) < 5 * 1024**2:  # TODO
            w = CodeEditorD(self)
            w.set_file(file)
            w.exec()
        else:
            self.view_file(file)

    def view_file(self, file: File) -> None:
        w = FileViewerD(self)
        w.set_file(file)
        w.exec()

    @property
    def all_btns(self):
        return (
            self.helpButton,
            self.settingButton,
            self.solveButton,
            self.buildButton,
            self.runButton,
            self.stopButton,
            self.submitButton,
        )

    @property
    def all_tabs(self):
        return (
            w
            for w in (
                self.tabWidget.widget(idx) for idx in range(self.tabWidget.count())
            )
            if w is not self.fileBrowser
        )

    def pre_task(self):
        for w in self.all_btns:
            w.setEnabled(F)
        self.buildButton.setVisible(F)
        self.runButton.setVisible(F)
        self.stopButton.setEnabled(T)
        self.stopButton.setVisible(T)
        global_stopflag.clear()
        self.stackedWidget.setCurrentIndex(0)
        if self.tabWidget.currentWidget() is not self.verdictBrowser:
            self.tabWidget.setCurrentWidget(self.verdictBrowser)

    def build_task(self):
        self.machine = statemachine_of_build(self.task, [self.verdictBrowser])
        self.machine.started.connect(self.pre_task)
        self.machine.finished.connect(self.post_task)
        self.machine.start()

    def run_task(self):
        self.machine = statemachine_of_run(self.task, [self.verdictBrowser])
        self.machine.started.connect(self.pre_task)
        self.machine.finished.connect(self.post_task)
        self.machine.start()

    def post_task(self):
        for verdict in self.task.verdicts:
            if verdict.test_id is not None:  # TODO generator type
                self.task.tests[verdict.test_id].status = verdict.status
        for w in self.all_btns:
            w.setEnabled(T)
        self.buildButton.setVisible(T)
        self.runButton.setVisible(T)
        self.stopButton.setEnabled(F)
        self.stopButton.setVisible(F)

    def terminate_task(self):
        logger.info(f"Terminating...")
        global_stopflag.set()

    def submit_task(self):
        d = CodeSubmitter(self.task.solver, self)
        d.exec()

    def set_color(self, v: QPalette):
        self.terminal.set_color(v)

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.task:
            self.task.save()
        self.taskBrowser.close() #TODO
        return super().closeEvent(event)

    # def open_console(self):
    #     if self.console is None:
    #         self.console = IPythonConsole(self)
    #     self.console.show()
