from cchelper import *


class TaskModel(QSqlTableModel):
    def __init__(
        self,
        view: QTableView,
    ) -> None:
        super().__init__(view)
        self.cols = ["name"]
        self.dats: List[Task] = []

    def rowCount(self, parent: QModelIndex = None) -> int:
        return len(self.dats)

    def columnCount(self, parent: QModelIndex = None) -> int:
        return len(self.cols)

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if not index.isValid():
            return None
        dat = self.dats[index.row()]
        col = self.cols[index.column()]
        raw = getattr(dat, col)
        ret = None
        match role:
            case Qt.ItemDataRole.ToolTipRole:
                ret = raw
            case Qt.ItemDataRole.DisplayRole:
                ret = raw
            case Qt.ItemDataRole.EditRole:
                ret = raw
            case Qt.ItemDataRole.TextAlignmentRole:
                ret = Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignVCenter
        return ret

    def setData(
        self,
        index: QModelIndex | QPersistentModelIndex,
        value: Any,
        role: int = Qt.ItemDataRole.EditRole,
    ) -> bool:
        # if not index.isValid():
        #     return F
        match role:
            case Qt.ItemDataRole.EditRole | Qt.ItemDataRole.CheckStateRole:
                dat = self.dats[index.row()]
                col = self.cols[index.column()]
                setattr(dat, col, value)
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
        if orientation == Qt.Orientation.Vertical:
            match role:
                case Qt.ItemDataRole.DisplayRole:
                    return section + 1
            return
        ret = None
        col = self.cols[section]
        match role:
            case Qt.ItemDataRole.DisplayRole:
                match col:
                    case "interact":
                        ret = "I"
                    case "submit_main":
                        ret = "M"
                    case _:
                        ret = col.capitalize()
            case Qt.ItemDataRole.ToolTipRole:
                ret = col
        return ret
