from cchelper import *


class TagModel(QAbstractTableModel):
    def __init__(
        self,
        view: QObject = None,
    ) -> None:
        super().__init__(view)
        self.dats = conf.dat['tags']
    
    def rowCount(self, parent: QModelIndex = None) -> int:
        return len(self.dats)

    def columnCount(self, parent: QModelIndex = None) -> int:
        return 1

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        raw = self.dats[index.row()]
        ret = None
        match role:
            case Qt.ItemDataRole.ToolTipRole:
                ret = raw
            case Qt.ItemDataRole.DisplayRole:
                ret = raw
            case Qt.ItemDataRole.EditRole:
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
                self.dats[index.row()] = value
                self.dataChanged.emit(index, index)
                return T
        return F

    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlags:
        mask = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        if index.row() >= 2:
            mask |= Qt.ItemFlag.ItemIsEditable
        return mask

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation = Qt.Orientation.Horizontal,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if orientation == Qt.Orientation.Vertical and role == Qt.ItemDataRole.DisplayRole:
            return section + 1

