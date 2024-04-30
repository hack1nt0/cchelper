from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from cchelper import *
from .tasktestparamseditor_ui import Ui_TaskTestParamsEditor


class TaskTestParamsEditor(QDialog, Ui_TaskTestParamsEditor):
    def __init__(self, parent: QWidget, model) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.model = model
        self.task: Task = model.row()

        self.comparatorComboBox.addItems([ct.value for ct in CT])
        self.comparatorComboBox.setCurrentText(self.task.comp_type.value)
        self.cpuBox.setValue(self.task.cpu)
        self.memBox.setValue(self.task.mem)
        self.qryBox.setValue(self.task.qry)
        self.qryBox.setEnabled(F)
        self.interactiveCheckBox.stateChanged.connect(
            lambda v: self.qryBox.setEnabled(T if v else F)
        )
        self.interactiveCheckBox.setChecked(self.task.interactive)

        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).clicked.connect(
            lambda: self.done(1)
        )
        self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).clicked.connect(
            lambda: self.done(0)
        )

    def done(self, arg__1: int = 1) -> None:
        if arg__1:
            self.task.comp_type = CT(self.comparatorComboBox.currentText())
            self.task.cpu = self.cpuBox.value()
            self.task.mem = self.memBox.value()
            self.task.qry = self.qryBox.value()
            self.task.interactive = self.interactiveCheckBox.isChecked()
            self.task.save()
            self.model.refresh()
        return super().done(arg__1)
