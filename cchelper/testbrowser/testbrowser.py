from PySide6.QtGui import QContextMenuEvent
from cchelper import *
from .testbrowser_ui import Ui_TestBrowser
from .model import TestModel
from .delegate import TestDelegate
from cchelper.fileeditor import CodeEditorD
from .testeditor import TestEditor


class TestBrowser(QWidget, Ui_TestBrowser):

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.view.setTabKeyNavigation(False)
        self.view.setAlternatingRowColors(True)

        self.model = TestModel(self.spinBox, "tests", self)
        self.view.setModel(self.model)
        self.delegate = TestDelegate()
        self.view.setItemDelegate(self.delegate)
        self.view.verticalHeader().setVisible(F)
        self.view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.view.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        self.view.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        self.view.setTabKeyNavigation(False)

        self.view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.popup_context_menu)
        self.context_menu = QMenu(self)
        self.new_act = self.context_menu.addAction("New test", self.new_tst)
        self.del_act = self.context_menu.addAction("Delete test", self.del_tst)
        self.copy_input_act = self.context_menu.addAction(
            "Copy input from existing file", lambda: self.copy_input_file("input")
        )

        self.delegate.edit_file_signal.connect(self.edit_file)
        self.delegate.edit_types_signal.connect(self.edit_types)

        self.newButton.setToolTip("New Task (Ctrl+N)")
        self.newButton.setIcon(QIcon(paths.img("add.png")))
        self.newButton.setShortcut("Ctrl+N")
        self.newButton.clicked.connect(self.new_tst)

    def set_task(self, task: Task):
        self.task = task
        self.model.set_dats(task.tests)

    def new_tst(self):
        test = self.task.new_test()
        self.add_test(test)

    def add_test(self, test: Test):
        self.model.add_dat(test)
        self.view.setFocus()

    def del_tst(self):
        if (
            ConfirmBox(
                self,
                f"Are you sure to delete this test?",
            ).exec()
            == ConfirmBox.YES
        ):
            self.model.row().remove()
            self.model.del_dat()
            self.view.setFocus()

    def copy_input_file(self, col: str):
        d = QFileDialog(self)
        # d.setDirectory(QDir.home()) #TODO
        d.setFileMode(QFileDialog.FileMode.ExistingFile)
        d.setWindowModality(Qt.WindowModality.WindowModal)
        if d.exec():
            test = self.model.row()
            s = d.selectedFiles()[0]
            t = test.input.path if col == "input" else test.answer.path
            with (
                open(s, "r") as r,
                open(t, "w") as w,
            ):
                for line in r:
                    w.write(line)

    def popup_context_menu(self, point):
        idx = self.view.indexAt(point)
        self.del_act.setEnabled(idx.isValid())
        self.copy_input_act.setEnabled(idx.isValid())
        self.context_menu.popup(QCursor().pos())

    def edit_file(self, file: File):
        w = CodeEditorD(self)
        w.set_file(file)
        w.exec()

    def edit_types(self):
        w = TestEditor(self, self.model)
        w.exec()