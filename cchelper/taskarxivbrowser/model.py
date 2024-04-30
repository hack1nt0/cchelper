from cchelper import *


class TaskModel(QSqlTableModel):
    def __init__(
        self,
        view: QTableView,
    ) -> None:
        super().__init__(view)
        self.dats: List[Dict[str, Any]] = []
        self.conditions = None

    @property
    def cols(self):
        return list(self.dats[0].keys()) if self.dats else []

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
        raw = dat[col]
        ret = None
        match role:
            case Qt.ItemDataRole.EditRole:
                ret = raw
            case Qt.ItemDataRole.ToolTipRole:
                match col:
                    case "tags":
                        ret = bin(raw)
                    case _:
                        ret = raw
            case Qt.ItemDataRole.DisplayRole:
                match col:
                    case "interactive" | "checked":
                        ret = None
                    case "ctime" | "mtime":
                        ret = None if raw is None else QDateTime.fromSecsSinceEpoch(raw).toString()
                    case "tags":
                        ret = [conf.tags[b + 1] for b in range(len(conf.tags) - 1) if (raw >> b & 1)]
                        ret = ",".join(ret) if ret else "*"
                    case _:
                        ret = raw
            case Qt.ItemDataRole.CheckStateRole:
                match col:
                    case "interactive" | "checked":
                        # dat = [Qt.CheckState.Unchecked, Qt.CheckState.PartiallyChecked, Qt.CheckState.Checked][raw]
                        ret = Qt.CheckState.Checked if raw else Qt.CheckState.Unchecked
            case Qt.ItemDataRole.TextAlignmentRole:
                match col:
                    case "id" | "task_id" | "test_id" | "cpu" | "mem" | "qry" | "gcount" | "tests" | "ctime" | "mtime":
                        ret = (
                            Qt.AlignmentFlag.AlignTrailing
                            | Qt.AlignmentFlag.AlignVCenter
                        )
                    case 'name':
                        ret = (
                            Qt.AlignmentFlag.AlignLeading
                            | Qt.AlignmentFlag.AlignVCenter
                        )
                    case _:
                        ret = Qt.AlignmentFlag.AlignCenter
        return ret

    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlags:
        mask = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        # col = self.cols[index.column()]
        # if col in ["interactive", "checked"]:
        #     mask |= Qt.ItemFlag.ItemIsSelectable
        # if col in [
        #     "solver",
        #     "generator",
        #     "jurger",
        #     "tests",
        # ]:
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
                    case "interactive":
                        ret = "I"
                    case "checked":
                        ret = "C"
                    case _:
                        ret = ' '.join(map(lambda s: s.capitalize(), col.split('_')))
            case Qt.ItemDataRole.ToolTipRole:
                ret = col
        return ret


    def row(
        self,
        index: QModelIndex | QPersistentModelIndex,
    ):
        return self.dats[index.row()]