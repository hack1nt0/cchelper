from typing import Union
from PySide6.QtCore import QAbstractItemModel, QModelIndex, QPersistentModelIndex
from PySide6.QtWidgets import QWidget
from cchelper import *


class TestDelegate(QStyledItemDelegate):
    edit_file_signal: Signal = Signal(File)
    edit_types_signal: Signal = Signal()

    def createEditor(
        self,
        parent: QWidget,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> QWidget:
        editor = None
        model = index.model()
        col = model.cols[index.column()]
        dat = model.row()
        match col:
            case "#":
                self.edit_types_signal.emit()
            case "input":
                self.edit_file_signal.emit(dat.input)
            case "answer":
                self.edit_file_signal.emit(dat.answer)

    # def setModelData(
    #     self,
    #     editor: QWidget,
    #     model: QAbstractItemModel,
    #     index: QModelIndex | QPersistentModelIndex,
    # ) -> None:
    #     model = index.model()
    #     col = model.cols[index.column()]
    #     dat = model.row()
    #     match col:
    #         case 'V':
    #             dat.checked = index.data(role=Qt.ItemDataRole.CheckStateRole) == Qt.CheckState.Checked
    #             model.dataChanged.emit(index, index)
