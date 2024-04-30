from cchelper import *


class TestModel(QAbstractTableModel):
    def __init__(self, parent: QObject | None = ...) -> None:
        super().__init__(parent)
        self.cols: List[str] = [
            "input",
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
                ret = raw
            case Qt.ItemDataRole.ToolTipRole:
                ret = raw
            case Qt.ItemDataRole.TextAlignmentRole:
                ret = (
                    Qt.AlignmentFlag.AlignLeading
                    | Qt.AlignmentFlag.AlignTop
                )
        return ret

    def setData(
        self,
        index: QModelIndex | QPersistentModelIndex,
        value: Any,
        role: int = Qt.ItemDataRole.EditRole,
    ) -> bool:
        dat = self.dats[index.row()]
        col = self.cols[index.column()]
        match role:
            case Qt.ItemDataRole.EditRole:
                if role == Qt.ItemDataRole.CheckStateRole:
                    value = T if value else F
                setattr(dat, col, value)
                self.dataChanged.emit(index, index)
                return T
        return F

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
                    case 'input_type':
                        ret = 'I/T'
                    case 'answer_type':
                        ret = 'A/T'
                    case "id":
                        ret = "#"
                    case _:
                        ret = ' '.join(map(lambda s: s.capitalize(), col.split('_')))
            case Qt.ItemDataRole.ToolTipRole:
                ret = col
        return ret
