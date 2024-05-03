from typing import Any
from PySide6.QtCore import QModelIndex, QPersistentModelIndex
from cchelper import *


class TaskModel(QAbstractTableModel):

    def __init__(
        self,
        view: QTableView,
    ) -> None:
        super().__init__(view)
        self.dats: List[Task] = []
        self.cols = ["name", "test params", "tags"]
        self.offset = 0

    def rowCount(self, parent: QModelIndex = None) -> int:
        return min(1, len(self.dats))

    def columnCount(self, parent: QModelIndex = None) -> int:
        return len(self.cols)

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        col = index.column()
        dat = self.dats[self.offset]
        ret = None
        match role:
            case Qt.ItemDataRole.EditRole:
                match col:
                    case 0:
                        ret = dat.name
                    case _:
                        ret = dat
            case Qt.ItemDataRole.DisplayRole | Qt.ItemDataRole.ToolTipRole:
                match col:
                    case 0:
                        ret = "\n".join(dat.name.split(os.sep))
                    case 1:
                        ret = f"comparator: {dat.comp_type.value}\ncpu <= {dat.cpu}\nmem <= {dat.mem}\ninteractive: {dat.interactive}\nqry <= {dat.qry}"
                    case 2:
                        tags = [
                            conf.tags[b + 1]
                            for b in range(len(conf.tags) - 1)
                            if (dat.tags >> b & 1)
                        ]
                        tags = ",".join(tags) if ret else "*"
                        ctime = QDateTime.fromSecsSinceEpoch(dat.ctime).toString()
                        doc = dat.doc
                        url = dat.url
                        ret = f"status: {dat.status.value}\ntags: {tags}\ndoc: {doc}\nurl: {url}\nctime: {ctime}"
            # case Qt.ItemDataRole.CheckStateRole:
            #     match col:
            #         case 0:
            #             ret = Qt.CheckState.Checked if raw else Qt.CheckState.Unchecked
            #         case "interactive" | "checked":
            #             # dat = [Qt.CheckState.Unchecked, Qt.CheckState.PartiallyChecked, Qt.CheckState.Checked][raw]
            # case Qt.ItemDataRole.ForegroundRole:
            #     match col:
            #         case 0:
            #             match dat.status:
            #                 case TS.SOLVED:
            #                     ret = GREEN
            #                 case TS.UNSOLVED:
            #                     ret = RED
            case Qt.ItemDataRole.TextAlignmentRole:
                match col:
                    case 2:
                        ret = (
                            Qt.AlignmentFlag.AlignLeading
                            | Qt.AlignmentFlag.AlignVCenter
                        )
                    case _:
                        ret = Qt.AlignmentFlag.AlignCenter
        return ret

    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlags:
        mask = Qt.ItemFlag.NoItemFlags
        match index.column():
            # case 0:
            #     pass
            case _:
                mask |= Qt.ItemFlag.ItemIsEnabled
                mask |= Qt.ItemFlag.ItemIsSelectable
                mask |= Qt.ItemFlag.ItemIsEditable
        return mask

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation = Qt.Orientation.Horizontal,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if orientation == Qt.Orientation.Vertical:
            return
        ret = None
        col = self.cols[section]
        match role:
            case Qt.ItemDataRole.DisplayRole:
                ret = " ".join(map(lambda s: s.capitalize(), col.split("_")))
        return ret


    def del_dat(self):
        # self.beginResetModel()
        # tot = len(self.dats)
        # self.dats.pop(self.offset)
        # self.spinBox.blockSignals(T)
        # self.spinBox.setRange(1, tot - 1)
        # self.spinBox.setSuffix(f" /{tot - 1} {self.suffix}")
        # self.spinBox.setValue(self.offset + 1)
        # self.spinBox.blockSignals(F)
        # self.offset = self.spinBox.value() - 1
        # self.endResetModel()
        pass

    def row(self) -> Task | None:
        return self.dats[self.offset] if self.rowCount() else None

    def refresh(self):
        self.dataChanged.emit(self.index(0, 0), self.index(0, self.columnCount() - 1))
