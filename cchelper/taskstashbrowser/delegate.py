from typing import Union
from PySide6.QtCore import QAbstractItemModel, QModelIndex, QPersistentModelIndex
from PySide6.QtWidgets import QStyleOptionViewItem, QWidget
from cchelper import *


class TaskDelegate(QStyledItemDelegate):

    def setEditorData(
        self, editor: QWidget, index: QModelIndex | QPersistentModelIndex
    ) -> None:
        dat = index.model().dats[index.row()]
        col = index.model().cols[index.column()]
        raw = getattr(dat, col)
        match col:
            case "tags":
                editor.setCurrentIndex(raw)
            case "comp_type":
                editor.setCurrentText(raw.value)
            case _:
                super().setEditorData(editor, index)

    def setModelData(
        self,
        editor: QWidget,
        model: QAbstractItemModel,
        index: QModelIndex | QPersistentModelIndex,
    ) -> None:
        dat = index.model().dats[index.row()]
        col = index.model().cols[index.column()]
        match col:
            case "tags":
                model.setData(index, editor.currentIndex())
            case "comp_type":
                model.setData(index, CT(editor.currentText()))
            case _:
                super().setModelData(editor, model, index)
