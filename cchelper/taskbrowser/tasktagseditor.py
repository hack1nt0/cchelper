from cchelper import *
from .tasktagseditor_ui import Ui_TaskTagsEditor

class TaskTagsEditor(QDialog, Ui_TaskTagsEditor):
    def __init__(self, parent: QWidget, model) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.model = model
        self.task: Task = model.row()
        self.tagsComboBox.addItems(conf.tags)
        self.tagsComboBox.setCurrentIndex(self.task.tags)
        self.urlLineEdit.setText(self.task.url)
        self.docLineEdit.setText(self.task.doc)
        self.statusComboBox.addItems([ts.value for ts in TS])
        self.statusComboBox.setCurrentText(self.task.status.value)
        self.nameLineEdit.setText(self.task.name)

        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).clicked.connect(
            lambda: self.done(1)
        )

    def done(self, arg__1: int) -> None:
        if arg__1:
            newname, oldname = self.nameLineEdit.text().strip(), self.task.name
            if oldname != newname:
                if not self.task.rename(newname):
                    logger.error(f"{newname} already exists! Cannot rename to that name.")
                    return
            self.task.name = newname 
            self.task.tags = self.tagsComboBox.currentIndex()
            self.task.url = self.urlLineEdit.text().strip()
            self.task.doc = self.docLineEdit.text().strip()
            self.task.status = TS(self.statusComboBox.currentText())
            self.task.save()
            self.model.refresh()
        return super().done(arg__1)
