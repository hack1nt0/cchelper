from typing import Optional
from PySide6.QtCore import QObject
from cchelper import *


class LangModel(QAbstractTableModel):
    def __init__(
        self,
        view: QObject = None,
    ) -> None:
        super().__init__(view)
        self.dats = conf.dat['languages']
        self.cols = list(self.dats[0].keys())
    
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
        raw = dat.get(col, None)
        ret = None
        match role:
            case Qt.ItemDataRole.EditRole:
                ret = raw
            case Qt.ItemDataRole.ToolTipRole:
                ret = raw
            case Qt.ItemDataRole.DisplayRole:
                ret = raw
            case Qt.ItemDataRole.TextAlignmentRole:
                ret = Qt.AlignmentFlag.AlignCenter
        return ret

    def setData(
        self,
        index: QModelIndex | QPersistentModelIndex,
        value: Any,
        role: int = Qt.ItemDataRole.EditRole,
    ) -> bool:
        match role:
            case Qt.ItemDataRole.EditRole:
                dat = self.dats[index.row()]
                col = self.cols[index.column()]
                dat[col] = value
                self.dataChanged.emit(index, index)
                return T
        return F

    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlags:
        mask = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        # mask |= Qt.ItemFlag.ItemIsEditable
        return mask

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation = Qt.Orientation.Horizontal,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if orientation == Qt.Orientation.Vertical and role == Qt.ItemDataRole.DisplayRole:
            return section + 1
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.cols[section].capitalize()

