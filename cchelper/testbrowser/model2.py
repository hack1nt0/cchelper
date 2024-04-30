from cchelper import *


class TestModel(QAbstractTableModel):
    def __init__(self, parent: QObject | None = ...) -> None:
        super().__init__(parent)
        self.cols: List[str] = [
            "checked",
            "id",
            "status",
            "input_type",
            "input",
            "answer_type",
            "answer",
        ]
        self.dats: List[Test] = []

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if not index.isValid():
            return None
        ret = None
        col = self.cols[index.column()]
        dat = self.dats[index.row()]
        raw = getattr(dat, col)
        match role:
            case Qt.ItemDataRole.EditRole:
                ret = raw
            case Qt.ItemDataRole.DisplayRole:
                match col:
                    case "input" | "answer":
                        ret = "..."
                    case "checked":
                        ret = None
                    case "status" | "input_type" | "answer_type":
                        ret = raw.name
                    case _:
                        ret = raw
            case Qt.ItemDataRole.ToolTipRole:
                match col:
                    case "input" | "answer":
                        ret = raw.path
            case Qt.ItemDataRole.TextAlignmentRole:
                match col:
                    case "input" | "answer":
                        ret = (
                            Qt.AlignmentFlag.AlignLeading
                            | Qt.AlignmentFlag.AlignVCenter
                        )
                    case _:
                        ret = Qt.AlignmentFlag.AlignCenter
            case Qt.ItemDataRole.CheckStateRole:
                match col:
                    case "checked":
                        ret = Qt.CheckState.Checked if raw else Qt.CheckState.Unchecked
        return ret

    def setData(
        self,
        index: QModelIndex | QPersistentModelIndex,
        value: Any,
        role: int = Qt.ItemDataRole.EditRole,
    ) -> bool:
        dat = self.row(index)
        col = self.col(index)
        setattr(dat, col, value)
        self.dataChanged.emit(index, index)
        return T

    def rowCount(self, parent: QModelIndex = None) -> int:
        return len(self.dats)

    def columnCount(self, parent: QModelIndex = None) -> int:
        return len(self.cols)

    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlags:
        mask = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        match self.cols[index.column()]:
            case "checked":
                mask |= Qt.ItemFlag.ItemIsUserCheckable
            case _:
                mask |= Qt.ItemFlag.ItemIsEditable
        return mask

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
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
                    case "checked":
                        ret = "C"
                    case "input_type":
                        ret = "I/T"
                    case "answer_type":
                        ret = "A/T"
                    case "id":
                        ret = "#"
                    case "status":
                        ret = "VS"
                    case _:
                        ret = " ".join(map(lambda s: s.capitalize(), col.split("_")))
            case Qt.ItemDataRole.ToolTipRole:
                ret = col
        return ret

    def row(self, idx: QModelIndex) -> Test:
        return self.dats[idx.row()]

    def col(self, idx: QModelIndex) -> str:
        return self.cols[idx.column()]