from cchelper import *
from .form_ui import Ui_TaskEditor
from cchelper.taskstashbrowser.model import TaskModel
from cchelper.taskstashbrowser.delegate import TaskDelegate

class TaskEditor(QDialog, Ui_TaskEditor):
    def __init__(self, model: TaskModel, idx: int, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.tagsComboBox.addItems(conf.tags)

        self.model = model
        self.deleg = TaskDelegate(self)
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setModel(self.model)
        self.mapper.setItemDelegate(self.deleg) #TODO
        self.mapper.addMapping(
            self.tagsComboBox,
            self.model.cols.index("tags"),
            # b"currentIndex",
        )
        self.mapper.addMapping(self.urlLineEdit, self.model.cols.index("url"))
        self.mapper.addMapping(self.docLineEdit, self.model.cols.index("doc"))
        self.mapper.setCurrentIndex(idx)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.ManualSubmit)

        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).clicked.connect(
            lambda: self.done(1)
        )
        # self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).clicked.connect(
        #     lambda: self.done(0)
        # )

    def done(self, arg__1: int) -> None:
        if arg__1:
            self.mapper.submit()  # TODO checkbox
        return super().done(arg__1)
