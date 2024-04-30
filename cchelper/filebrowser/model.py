from cchelper import *

class FileTreeModel(QFileSystemModel):
    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlags:
        mask = (
            Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsSelectable
            | Qt.ItemFlag.ItemIsEditable
        )
        return mask

class FileModel(QAbstractTableModel):
    def __init__(
        self,
        view: QTableView,
    ) -> None:
        super().__init__(view)
        self.cols = [
            "path",
            "mtime",
            "length",
        ]
        self.dats: List[File] = []
        self.conditions = None

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
            case Qt.ItemDataRole.ToolTipRole:
                match col:
                    case "mtime":
                        ret = None if raw is None else QDateTime.fromSecsSinceEpoch(raw)
                    case "kind":
                        ret = raw.name
                    case _:
                        ret = raw
            case Qt.ItemDataRole.DisplayRole:
                match col:
                    case "kind":
                        ret = raw.name
                    case _:
                        ret = raw
            case Qt.ItemDataRole.EditRole:
                ret = raw
            case Qt.ItemDataRole.CheckStateRole:
                if dat.path.startswith("T" + os.sep):
                    ret = raw
            case Qt.ItemDataRole.TextAlignmentRole:
                match col:
                    case "kind":
                        ret = Qt.AlignmentFlag.AlignCenter
                    case "mtime":
                        ret = (
                            Qt.AlignmentFlag.AlignTrailing
                            | Qt.AlignmentFlag.AlignVCenter
                        )
                    case _:
                        ret = (
                            Qt.AlignmentFlag.AlignLeading
                            | Qt.AlignmentFlag.AlignVCenter
                        )
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
        mask = (
            Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsSelectable
            | Qt.ItemFlag.ItemIsEditable
        )
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
                    case _:
                        ret = " ".join(map(lambda s: s.capitalize(), col.split("_")))
            case Qt.ItemDataRole.ToolTipRole:
                ret = col
        return ret

    def row(self, index: QModelIndex | QPersistentModelIndex):
        return self.dats[index.row()]


class FoundModel(QAbstractTableModel):
    def __init__(
        self,
        parent,
    ) -> None:
        super().__init__(parent)
        self.cols = [
            "File Name",
            "First Match in Context",
        ]
        self.dats: List[Tuple[str, str]] = []

    def rowCount(self, parent: QModelIndex = None) -> int:
        return len(self.dats)

    def columnCount(self, parent: QModelIndex = None) -> int:
        return len(self.cols)

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        col = index.column()
        dat = self.dats[index.row()]
        raw = dat[col]
        ret = None
        match role:
            case Qt.ItemDataRole.ToolTipRole:
                match col:
                    case 0:
                        ret = raw
            case Qt.ItemDataRole.DisplayRole:
                ret = raw
            case Qt.ItemDataRole.EditRole:
                ret = raw
            case Qt.ItemDataRole.TextAlignmentRole:
                match col:
                    case 0:
                        ret = Qt.AlignmentFlag.AlignCenter
                    case 0:
                        ret = (
                            Qt.AlignmentFlag.AlignLeading
                            | Qt.AlignmentFlag.AlignTop
                        )
        return ret

    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlags:
        if index.column() == 0:
            mask = (
                Qt.ItemFlag.ItemIsEnabled
                | Qt.ItemFlag.ItemIsSelectable
                | Qt.ItemFlag.ItemIsEditable
            )
        else:
            mask = Qt.ItemFlag.NoItemFlags
        return mask

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation = Qt.Orientation.Horizontal,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.cols[section].title()

    def row(self, index: QModelIndex | QPersistentModelIndex):
        return self.dats[index.row()]
    
    def clear(self):
        self.beginResetModel()
        self.dats.clear()
        self.endResetModel()

