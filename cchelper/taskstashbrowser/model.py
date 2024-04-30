from typing import Any, Union
from PySide6.QtCore import QModelIndex, QPersistentModelIndex
from cchelper import *


class TaskModel(QAbstractTableModel):
    def __init__(
        self,
        view: QTableView,
    ) -> None:
        super().__init__(view)
        self.dats: List[Task] = []
        self.cols = list(map(lambda field: field.name, dataclasses.fields(Task)))

    def rowCount(self, parent: QModelIndex = None) -> int:
        return len(self.dats)

    def columnCount(self, parent: QModelIndex = None) -> int:
        return len(self.cols)

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        col = self.cols[index.column()]
        dat = self.dats[index.row()]
        raw = getattr(dat, col)
        ret = None
        match role:
            case Qt.ItemDataRole.EditRole:
                ret = raw
            case Qt.ItemDataRole.DisplayRole:
                ret = raw
        return ret

    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlags:
        mask = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        if self.cols[index.column()] != "name":
            mask |= Qt.ItemFlag.ItemIsEditable
        return mask

    def setData(
        self,
        index: QModelIndex | QPersistentModelIndex,
        value: Any,
        role: int = Qt.ItemDataRole.EditRole,
    ) -> bool:
        dat = self.dats[index.row()]
        col = self.cols[index.column()]
        setattr(dat, col, value)
        self.dataChanged.emit(index, index)
        return T

    # def headerData(
    #     self,
    #     section: int,
    #     orientation: Qt.Orientation = Qt.Orientation.Horizontal,
    #     role: int = Qt.ItemDataRole.DisplayRole,
    # ) -> Any:
    #     if orientation == Qt.Orientation.Vertical:
    #         match role:
    #             case Qt.ItemDataRole.DisplayRole:
    #                 return section + 1
    #         return
    #     ret = None
    #     col = self.cols[section]
    #     match role:
    #         case Qt.ItemDataRole.DisplayRole:
    #             match col:
    #                 case "interactive":
    #                     ret = "I"
    #                 case "checked":
    #                     ret = "C"
    #                 case _:
    #                     ret = ' '.join(map(lambda s: s.capitalize(), col.split('_')))
    #         case Qt.ItemDataRole.ToolTipRole:
    #             ret = col
    #     return ret

    def row(
        self,
        index: QModelIndex | QPersistentModelIndex,
    ):
        return self.dats[index.row()]
