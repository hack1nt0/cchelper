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
        match col:
            case "count":
                editor = QSpinBox(parent=parent)
                editor.setMinimum(1)
                editor.setMaximum(10000)
                editor.setSingleStep(100)
            case "input_type":
                editor = QComboBox(parent=parent)
                editor.addItems([e.value for e in IT])
                editor.setCurrentText(raw.value)
            case "answer_type":
                editor = QComboBox(parent=parent)
                editor.addItems([e.value for e in AT])
                editor.setCurrentText(raw.value)
            case "input":
                self.edit_signal.emit(dat.input)
            case "answer":
                self.edit_signal.emit(dat.answer)
        if editor:
            editor.setAutoFillBackground(T)
        return editor

    def setModelData(
        self,
        editor: QWidget,
        model: QAbstractItemModel,
        index: QModelIndex | QPersistentModelIndex,
    ) -> None:
        col = model.cols[index.column()]
        match col:
            case 'input_type':
                model.setData(index, IT(editor.currentText()))
            case 'answer_type':
                model.setData(index, AT(editor.currentText()))
            case _:
                super().setModelData(editor, model, index)

    # TODO
    def updateEditorGeometry(
        self,
        editor: QWidget,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> None:
        if type(editor) == QFileDialog:
            return
        if type(editor) == QPlainTextEdit:
            R = option.rect
            x, y, w, h = R.x(), R.y(), R.width(), R.height()
            h = max(400, h)
            editor.setGeometry(x, y, w, h)
        else:
            super().updateEditorGeometry(editor, option, index)
