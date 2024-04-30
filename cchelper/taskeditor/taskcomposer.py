from PySide6.QtGui import QShowEvent
from cchelper import *
from cchelper.taskcrawler import TaskCrawler
from .model import TaskModel
from .delegate import TaskDelegate
from cchelper.taskarxivbrowser import TaskArxivBrowser
from cchelper.logviewer import LogViewer
from .listener import CcListener
from cchelper.taskcreator import TaskCreator
from cchelper.taskeditor import TaskEditor, TestParamsEditor
from cchelper.confform import ConfForm
from cchelper.taskfinder import TaskFinder

# import cchelper.taskstashbrowser.test as TestService
import cchelper.taskstashbrowser.testasync as TestService
from cchelper.testbrowser import TestBrowser
from cchelper.filebrowser import FileBrowser
from cchelper.langbrowser import LangBrowser
from cchelper.tagbrowser import TagBrowser
from cchelper.tasksubmitter import CodeSubmitter
import glob
from pathlib import Path
from .statemachines import statemachine_of_build, statemachine_of_run
from cchelper.verdictbrowser import VerdictBrowser

# from cchelper.terminal.ipython import IPythonConsole

from cchelper.fileeditor.codeeditor import CodeEditor
from cchelper.fileviewer.fileviewer import FileViewer
from .taskcomposerd_ui import Ui_TaskComposerD


class TaskComposer(QDialog, Ui_TaskComposerD):
    add_task_signal: Signal = Signal(Task)
    arxiv_task_signal: Signal = Signal()

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.fa = parent

        def switch_tab():
            cur = self.tabWidget.currentIndex()
            nxt = (cur + 1) % self.tabWidget.count()
            self.tabWidget.setCurrentIndex(nxt)

        self.tab_shortcut = QShortcut("Alt+Tab", self)
        self.tab_shortcut.activated.connect(switch_tab)

        def close_tab(idx: int = -1):
            if idx < 0:
                idx = self.tabWidget.currentIndex()
            w = self.tabWidget.widget(idx)
            if w not in (self.SEditor, self.TEditor):
                w.close()

        self.tabWidget.tabCloseRequested.connect(close_tab)
        self.tab_shortcut2 = QShortcut("Ctrl+W", self)
        self.tab_shortcut2.activated.connect(close_tab)

        def view_verdicts(v: VS):
            self.VBrowser.drillin(v)
            self.tabWidget_2.setCurrentWidget(self.VBrowser)

        self.CViewer.drillin_signal.connect(view_verdicts)

        self.VBrowser.view_file_signal.connect(self.view_file)

        def view_graph(file: File):
            self.GViewer.setEnabled(T)
            self.GViewer.set_file(file)
            self.tabWidget_2.setCurrentWidget(self.GViewer)

        self.VBrowser.view_graph_signal.connect(view_graph)

        self.TEditor.edit_file_signal.connect(self.edit_file)

        ##### TASKS
        self.model: TaskModel = None
        self.idx: QModelIndex = None
        self.task: Task = None

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

        #### SUBMIT
        self.submitButton.setShortcut("F6")
        self.submitButton.setToolTip("Submit (F6)")
        self.submitButton.setIcon(QIcon(paths.img("send.png")))
        self.submitButton.clicked.connect(self.submit_task)

    def set_model(self, model, idx):
        self.model = model
        self.idx = idx
        self.task = model.row(idx)
        self.setWindowTitle(str(self.task))
        self.task.create_symlinks()
        self.SEditor = self.edit_file(self.task.solver)
        # self.SEditor.set_file(self.task.solver)
        self.VBrowser.setData(self.task)
        self.CViewer.setData(self.task)
        self.TEditor.set_model(self.model, self.idx)

    def edit_file(self, file: File) -> CodeEditor | FileViewer:
        label = os.path.splitext(os.path.basename(file.path))[0].title()
        if len(file) < 5 * 1024**2:  # TODO
            for w in self.all_editors:
                if w.path == file.path:
                    self.tabWidget.setCurrentWidget(w)
                    return w
            w = CodeEditor(self)
            w.set_file(file)
            idx = self.tabWidget.addTab(w, label)
            self.tabWidget.setCurrentIndex(idx)
            self.tabWidget.setTabToolTip(idx, file.path)
            w.changed_signal.connect(
                lambda w=w, label=label: self.tabWidget.setTabText(
                    self.tabWidget.indexOf(w), f"{label}*"
                )
            )
            w.saved_signal.connect(
                lambda w=w, label=label: self.tabWidget.setTabText(
                    self.tabWidget.indexOf(w), f"{label}"
                )
            )
            return w
        else:
            return self.view_file(file)

    def view_file(self, file: File) -> FileViewer:
        self.FViewer.set_file(file)
        idx = self.tabWidget_2.indexOf(self.FViewer)
        self.tabWidget_2.setCurrentIndex(idx)
        self.tabWidget_2.setTabToolTip(idx, file.path)
        return self.FViewer

    @property
    def all_btns(self):
        return (
            self.buildButton,
            self.runButton,
            self.stopButton,
            self.submitButton,
        )

    @property
    def all_editors(self):
        return (
            w
            for w in (
                self.tabWidget.widget(idx) for idx in range(self.tabWidget.count())
            )
            if isinstance(w, CodeEditor)
        )

    def pre_task(self):
        for w in self.all_btns:
            w.setEnabled(F)
        self.stopButton.setEnabled(T)
        global_stopflag.clear()
        if self.tabWidget_2.currentWidget() not in (self.CViewer, self.VBrowser):
            self.tabWidget_2.setCurrentWidget(self.CViewer)
        self.FViewer.setEnabled(F)
        self.CViewer.setEnabled(F)

    def build_task(self):
        self.machine = statemachine_of_build(self.task, [self.VBrowser, self.CViewer])
        self.machine.started.connect(self.pre_task)
        self.machine.finished.connect(self.post_task)
        self.machine.start()

    def run_task(self):
        self.machine = statemachine_of_run(self.task, [self.VBrowser, self.CViewer])
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

    def done(self, arg__1: int) -> None:
        for w in self.all_editors:
            w.save()
        self.fa.show()
        return super().done(arg__1)

    # def open_console(self):
    #     if self.console is None:
    #         self.console = IPythonConsole(self)
    #     self.console.show()
