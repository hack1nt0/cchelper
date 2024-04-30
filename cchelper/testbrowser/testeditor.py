from cchelper import *
from .testeditor_ui import Ui_TestEditor

class TestEditor(QDialog, Ui_TestEditor):
    def __init__(self, parent: QWidget, model) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.model = model
        self.test: Test = model.row()
        self.countSpinBox.setRange(1, 1001)
        self.countSpinBox.setValue(self.test.count)
        self.inputTypeComboBox.addItems([it.value for it in IT])
        self.inputTypeComboBox.setCurrentText(self.test.input_type.value)
        self.answerTypeComboBox.addItems([it.value for it in AT])
        self.answerTypeComboBox.setCurrentText(self.test.answer_type.value)

    def done(self, arg__1: int) -> None:
        if arg__1:
            self.test.count = self.countSpinBox.value()
            self.test.input_type = IT(self.inputTypeComboBox.currentText())
            self.test.answer_type = AT(self.answerTypeComboBox.currentText())
        return super().done(arg__1)
