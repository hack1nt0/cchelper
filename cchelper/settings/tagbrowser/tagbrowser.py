from cchelper import *
from .tagbrowser_ui import Ui_TagBrowser
from .model import TagModel


class TagBrowser(QWidget, Ui_TagBrowser):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.label.setStyleSheet("background-color : blue; color : white;")
        self.view.setTabKeyNavigation(False)
        self.view.setAlternatingRowColors(True)

        self.model = TagModel(self)
        self.view.setModel(self.model)
        self.menu = QMenu(self)
        self.new_act = self.menu.addAction("New Tag", self.new)
        self.del_act = self.menu.addAction("Delete Tag", self.remove)
        self.view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.popup)
    
        # self.buttonBox.accepted.connect(self.accept)
        # self.buttonBox.rejected.connect(self.reject)

    def new(self):
        self.model.beginResetModel()
        self.model.dats.append("New Tag")
        self.model.endResetModel()
        self.view.scrollToBottom()
        self.view.selectionModel().setCurrentIndex(self.model.index(self.model.rowCount() - 1, 0), QItemSelectionModel.SelectionFlag.ClearAndSelect)

    def remove(self):
        rows = [idx.row() for idx in self.view.selectedIndexes() if idx.row() >= 2]
        self.model.beginResetModel()
        for row in reversed(rows):
            self.model.dats.pop(row)
        self.model.endResetModel()

    def popup(self, pos):
        idx = self.view.indexAt(pos)
        self.del_act.setEnabled(idx.isValid())
        # self.menu.popup(self.mapToGlobal(pos)) #TODO
        self.menu.popup(QCursor().pos()) #TODO
        
    # def done(self, arg__1: int) -> None:
    #     conf.save()
    #     # else:
    #     #     conf.reload()
    #     return super().done(arg__1)
    