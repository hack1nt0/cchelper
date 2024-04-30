from typing import Union
from PySide6.QtCore import QAbstractItemModel, QModelIndex, QPersistentModelIndex
from PySide6.QtWidgets import QStyleOptionViewItem, QWidget
from cchelper import *


class TaskDelegate(QStyledItemDelegate):
    edit_tp_signal: Signal = Signal(Task)
    edit_tags_signal: Signal = Signal(Task)

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex) -> QWidget:
        match index.column():
            # case 0:
            #     return super().createEditor(parent, option, index)
            case 1:
                self.edit_tp_signal.emit(index.model().row())
            case 2:
                self.edit_tags_signal.emit(index.model().row())
