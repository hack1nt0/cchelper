from cchelper import *


class ConfModel(QSqlTableModel):
    def __init__(
        self,
        view: QTableView,
    ) -> None:
        super().__init__(view)
        self.dat = conf.dat
        self.cols = list(conf.dat.keys())

    def rowCount(self, parent: QModelIndex = None) -> int:
        return 1

    def columnCount(self, parent: QModelIndex = None) -> int:
        return len(self.cols)

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        col = self.cols[index.column()]
        raw = self.dat[col]
        ret = None
        match role:
            case Qt.ItemDataRole.EditRole:
                ret = raw
        return ret

    def setData(
        self,
        index: QModelIndex | QPersistentModelIndex,
        value: Any,
        role: int = Qt.ItemDataRole.EditRole,
    ) -> bool:
        match role:
            case Qt.ItemDataRole.EditRole:
                self.dat[self.cols[index.column()]] = value
                self.dataChanged.emit(index, index)
                return T
        return F

    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlags:
        mask = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        mask |= Qt.ItemFlag.ItemIsEditable
        return mask

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation = Qt.Orientation.Horizontal,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        ret = None
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            ret = self.cols[section]
        return ret
