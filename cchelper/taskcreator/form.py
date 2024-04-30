from cchelper import *
from .form_ui import Ui_TaskCreator
import copy
from cchelper.taskarxivbrowser import TaskDelegate

class TaskCreator(QDialog, Ui_TaskCreator):
    def __init__(self, parent: QWidget=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        # self.langModel = LangModel(self)
        # self.languageComboBox.setModel(self.langModel)

        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).clicked.connect(lambda: self.done(1))
        self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).clicked.connect(lambda: self.done(0))

    def done(self, arg__1: int) -> None:
        if arg__1:
            self.task = Task()
            self.task.name = self.nameLineEdit.text().strip().title()
            # self.task.lang_id = self.languageComboBox.currentIndex()
            if not self.task.name:
                logger.error('Name field is NULL !')
                return
        return super().done(arg__1)