from typing import Union
from PySide6.QtCore import QModelIndex, QPersistentModelIndex
from PySide6.QtWidgets import QStyleOptionViewItem, QWidget
from cchelper import *


class TaskDelegate(QStyledItemDelegate):
    drill_in_signal: Signal = Signal(int, str)

    def createEditor(
        self,
        parent: QWidget,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> QWidget:
        dat = index.model().dats[index.row()]
        val = dat['solver']
        self.drill_in_signal.emit(dat["id"], val)
        return

    # def setEditorData(
    #     self, editor: QWidget, index: QModelIndex | QPersistentModelIndex
    # ) -> None:
    #     dat = index.model().dats[index.row()]
    #     col = index.model().cols[index.column()]
    #     self.drill_in_signal.emit(dat["id"], col)
