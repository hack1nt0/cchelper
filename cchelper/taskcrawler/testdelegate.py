from typing import Union
from PySide6.QtCore import QAbstractItemModel, QModelIndex, QPersistentModelIndex
from PySide6.QtWidgets import QWidget
from cchelper import *


class TestDelegate(QStyledItemDelegate):
    edit_signal: Signal = Signal(File)

    def createEditor(
        self,
        parent: QWidget,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> QWidget:
        editor = None
        model = index.model()
        col = model.cols[index.column()]
        dat = model.dats[index.row()]
        raw = model.data(index, role=Qt.ItemDataRole.EditRole)
        editor = QPlainTextEdit(parent=parent)
        editor.setPlainText(raw)
        editor.setAutoFillBackground(T)
        return editor

    def setModelData(
        self,
        editor: QWidget,
        model: QAbstractItemModel,
        index: QModelIndex | QPersistentModelIndex,
    ) -> None:
        model.setData(index, editor.toPlainText())

    # # TODO
    # def updateEditorGeometry(
    #     self,
    #     editor: QWidget,
    #     option: QStyleOptionViewItem,
    #     index: QModelIndex | QPersistentModelIndex,
    # ) -> None:
    #     if type(editor) == QFileDialog:
    #         return
    #     if type(editor) == QPlainTextEdit:
    #         R = option.rect
    #         x, y, w, h = R.x(), R.y(), R.width(), R.height()
    #         h = max(400, h)
    #         editor.setGeometry(x, y, w, h)
    #     else:
    #         super().updateEditorGeometry(editor, option, index)
