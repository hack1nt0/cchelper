from typing import Optional
import PySide6.QtCore
from cchelper import *


class VerdictModel(QAbstractTableModel):
    COLORS = [RED, GREEN, YELLOW, YELLOW]

    def __init__(self, parent: QObject | None = ...) -> None:
        super().__init__(parent)
        self.dats: List[Verdict] = []
        self.cols: List[str] = [
            "added_as_test",
            "id",
            "status",
            "cmd",
            "input",
            "actual",
            "answer",
            "stderr",
            "chat",
        ]
        self.tail_bytes: int = 0
        self.offset: int = 0
        self.limit: int = 0

    def rowCount(self, parent: QModelIndex = None) -> int:
        return min(1, len(self.dats))

    def columnCount(self, parent: QModelIndex = None) -> int:
        return len(self.cols)

    def refresh(self):
        if self.rowCount():
            self.dataChanged.emit(
                self.index(0, 0),
                self.index(0, self.columnCount() - 1),
            )

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if not index.isValid():
            return None
        dat = self.dats[index.row() + self.offset]
        col = self.cols[index.column()]
        raw = getattr(dat, col)
        ret = None
        match role:
            case Qt.ItemDataRole.EditRole:
                ret = raw
            case Qt.ItemDataRole.DisplayRole:
                if isinstance(raw, File):
                    ret = raw.tail(self.tail_bytes)
                elif col == "id":
                    ret = f"{dat.id}/{dat.test_id}"
                elif col == "status":
                    ret = f"{dat.status_detail}\nCpu: {dat.cpu}MS\nMemory: {dat.mem}MB\nPipe: {bytes_str(dat.flow_bytes)}/{dat.progress}%"
                else:
                    ret = raw
            # case Qt.ItemDataRole.DecorationRole:
            #     match col:
            #         case 'status':
            #             iw, ih = 16, 16
            #             pixmap = QPixmap(iw, ih)
            #             painter = QPainter(pixmap)
            #             painter.setPen(QColor(255, 0, 0, 128))
            #             painter.drawText(QRect(0, 0, iw, ih), dat.status.name)
            #             ret = QIcon(pixmap)
            case Qt.ItemDataRole.ToolTipRole:
                pass
            case Qt.ItemDataRole.CheckStateRole:
                match col:
                    case "id":
                        ret = (
                            Qt.CheckState.Checked
                            if dat.added_as_test
                            else Qt.CheckState.Unchecked
                        )
            case Qt.ItemDataRole.ForegroundRole:
                if col == "status":
                    ret = VerdictModel.COLORS[VS.kind(dat.status)]
            case Qt.ItemDataRole.TextAlignmentRole:
                if isinstance(raw, File):
                    ret = Qt.AlignmentFlag.AlignLeading
                else:
                    ret = Qt.AlignmentFlag.AlignCenter
        return ret

    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlags:
        mask = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        col = self.cols[index.column()]
        match col:
            case "id":
                mask |= Qt.ItemFlag.ItemIsSelectable
            case "input" | "actual" | "answer" | "stderr" | "chat":
                mask |= Qt.ItemFlag.ItemIsEditable
        return mask

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        ret = None
        match orientation:
            case Qt.Orientation.Vertical:
                match role:
                    case Qt.ItemDataRole.DisplayRole:
                        dat = self.dats[section + self.offset]
                        ret = dat.id

            case Qt.Orientation.Horizontal:
                match role:
                    case Qt.ItemDataRole.DisplayRole:
                        col = self.cols[section]
                        col = self.cols[section]
                        match col:
                            case "id":
                                ret = "+/#"
                            case _:
                                ret = " ".join(
                                    map(lambda s: s.capitalize(), col.split("_"))
                                )
                    case Qt.ItemDataRole.ToolTipRole:
                        col = self.cols[section]
                        match col:
                            case "id":
                                ret = "added as test/vid/tid"
                            case _:
                                ret = " ".join(
                                    map(lambda s: s.capitalize(), col.split("_"))
                                )
        return ret
