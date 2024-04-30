from cchelper import *
from .langbrowser_ui import Ui_LangBrowser
from .model import LangModel
from .langform import LangForm


class LangBrowser(QWidget, Ui_LangBrowser):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.label.setStyleSheet("background-color : blue; color : white;")
        self.view.setTabKeyNavigation(False)
        self.view.setAlternatingRowColors(True)

        self.model = LangModel(self)
        self.view.setModel(self.model)
        # self.newButton.clicked.connect(self.new)
        # self.editButton.clicked.connect(self.edit)
        self.view.doubleClicked.connect(lambda idx: self.edit())
        self.menu = QMenu(self)
        self.new_act = self.menu.addAction("New Language", self.new)
        # self.edit_act = self.menu.addAction("Edit Language", self.edit)
        self.del_act = self.menu.addAction("Delete Language", self.remove)
        self.view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.popup)
        # self.delButton.clicked.connect(self.remove)
    
        # self.buttonBox.accepted.connect(self.accept)
        # self.buttonBox.rejected.connect(self.reject)

    def new(self):
        idx = self.model.rowCount()
        self.model.dats.append({})
        d = LangForm(self.model, idx, self)
        d.setWindowTitle('New Language')
        if d.exec():
            self.model.beginResetModel()
            self.model.endResetModel()
            self.view.scrollToBottom()
            self.view.selectionModel().setCurrentIndex(self.model.index(self.model.rowCount() - 1, 0), QItemSelectionModel.SelectionFlag.ClearAndSelect)
        else:
            self.model.dats.pop(idx)
    
    def edit(self):
        if not self.view.currentIndex():
            return
        idx = self.view.currentIndex().row()
        d = LangForm(self.model, idx, self)
        d.setWindowTitle('Edit Language')
        if d.exec():
            self.model.beginResetModel()
            self.model.endResetModel()
        
    def remove(self):
        rows = [idx.row() for idx in self.view.selectedIndexes()]
        self.model.beginResetModel()
        for row in reversed(rows):
            self.model.dats.pop(row)
        self.model.endResetModel()

    def popup(self, pos):
        idx = self.view.indexAt(pos)
        # self.edit_act.setEnabled(idx.isValid())
        self.del_act.setEnabled(idx.isValid())
        # self.menu.popup(self.mapToGlobal(pos)) #TODO
        self.menu.popup(QCursor().pos()) #TODO


    # def done(self, arg__1: int) -> None:
    #     conf.save()
    #     return super().done(arg__1)
        