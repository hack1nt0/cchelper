from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from cchelper import *
from .testparams_ui import Ui_TestParamsEditor
from cchelper.taskstashbrowser.model import TaskModel
from cchelper.taskstashbrowser.delegate import TaskDelegate


class TestParamsEditor(QDialog, Ui_TestParamsEditor):
    def __init__(self, model: TaskModel, idx: int, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        # self.header.setStyleSheet("background-color : blue; color : white;")
        # self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.footer.setStyleSheet("background-color : blue; color : white;")
        # self.footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.task: Task = model.row(idx)

        self.interactiveCheckBox.stateChanged.connect(
            lambda v: self.qryBox.setEnabled(T if v else F)
        )
        self.qryBox.setEnabled(F)

        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.ManualSubmit)
        self.mapper.setModel(model)
        self.deleg = TaskDelegate(self)
        self.mapper.setItemDelegate(self.deleg)
        self.mapper.addMapping(
            self.interactiveCheckBox, model.cols.index("interactive")
        )
        self.mapper.addMapping(self.gcountSpinBox, model.cols.index("gcount"))
        self.comparatorComboBox.addItems([ct.value for ct in CT])
        self.mapper.addMapping(self.comparatorComboBox, model.cols.index("comp_type"))
        self.mapper.addMapping(self.cpuBox, model.cols.index("cpu"))
        self.mapper.addMapping(self.memBox, model.cols.index("mem"))
        self.mapper.addMapping(self.qryBox, model.cols.index("qry"))
        self.mapper.setCurrentModelIndex(idx)

        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).clicked.connect(lambda: self.done(1))
        self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).clicked.connect(lambda: self.done(0))

    def sel_file(self, key: str):
        def f():
            d = QFileDialog(self)
            d.setDirectory(self.task.file_dir())  # TODO
            d.setFileMode(QFileDialog.FileMode.ExistingFile)
            d.setWindowModality(Qt.WindowModality.WindowModal)
            if d.exec():
                new_path = d.selectedFiles()[0]
                getattr(self.task, key).path = new_path
                self.task.arxiv()
                self.task.stash()
                self.txt_btns()
        return f

    def txt_btns(self):
        for k, v in self.file2btns.items():
            v.setText(os.path.relpath(getattr(self.task, k).path, self.task.file_dir()))

    def done(self, arg__1: int = 1) -> None:
        if arg__1:
            self.mapper.submit()
        return super().done(arg__1)
