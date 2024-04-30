from typing import Any
from PySide6.QtCore import QModelIndex, QPersistentModelIndex
from cchelper import *


class TestModel(QAbstractTableModel):
    def __init__(
        self, spinBox: QSpinBox, suffix: str, parent: QObject | None = ...
    ) -> None:
        super().__init__(parent)
        self.cols: List[str] = [
            "V",
            "#",
            "input",
            "answer",
        ]
        self.dats: List[Test] = []
        self.offset = 0

        self.spinBox = spinBox
        self.spinBox.setRange(0, 0)
        self.suffix = suffix

        def jump2page(idx: int):
            self.offset = idx - 1
            self.refresh()

        self.spinBox.valueChanged.connect(jump2page)

        self.nxtpage_key = QShortcut(Qt.Key.Key_PageDown, parent)
        self.nxtpage_key.activated.connect(
            lambda: self.spinBox.setValue(self.spinBox.value() + 1)
        )
        self.prepage_key = QShortcut(Qt.Key.Key_PageUp, parent)
        self.prepage_key.activated.connect(
            lambda: self.spinBox.setValue(self.spinBox.value() - 1)
        )

    def rowCount(self, parent: QModelIndex = None) -> int:
        return min(1, len(self.dats))

    def columnCount(self, parent: QModelIndex = None) -> int:
        return len(self.cols)

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if not index.isValid():
            return None
        ret = None
        col = self.cols[index.column()]
        dat = self.dats[self.offset]
        match role:
            case Qt.ItemDataRole.CheckStateRole:
                match col:
                    case 'V':
                        ret = Qt.CheckState.Checked if dat.checked else Qt.CheckState.Unchecked
            case Qt.ItemDataRole.DisplayRole | Qt.ItemDataRole.ToolTipRole:
                match col:
                    case "V":
                        ret = None
                    case "input":
                        ret = dat.input.tail()
                    case "answer":
                        ret = dat.answer.tail()
                    case "#":
                        ret = f"id: {dat.id}\nlast run: {dat.status.value}\n" \
                            + f"cnt.: {dat.count}\nI/T: {dat.input_type.value}\nA/T: {dat.answer_type.value}"
            case Qt.ItemDataRole.TextAlignmentRole:
                match col:
                    case "input" | "answer":
                        ret = (
                            Qt.AlignmentFlag.AlignLeading
                            | Qt.AlignmentFlag.AlignVCenter
                        )
                    case _:
                        ret = Qt.AlignmentFlag.AlignCenter
        return ret

    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlags:
        mask = Qt.ItemFlag.NoItemFlags
        match self.cols[index.column()]:
            case "V":
                mask |= Qt.ItemFlag.ItemIsEnabled
                mask |= Qt.ItemFlag.ItemIsUserCheckable
            case _:
                mask |= Qt.ItemFlag.ItemIsEnabled
                mask |= Qt.ItemFlag.ItemIsSelectable
                mask |= Qt.ItemFlag.ItemIsEditable
        return mask
    
    def setData(self, index: QModelIndex | QPersistentModelIndex, value: Any, role: int) -> bool:
        if role == Qt.ItemDataRole.CheckStateRole:
            self.row().checked = not self.row().checked
            self.dataChanged.emit(index, index)
            return T
        return F

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
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

    def row(self) -> Test:
        return self.dats[self.offset]

    def col(self, idx: QModelIndex) -> str:
        return self.cols[idx.column()]

    def refresh(self):
        self.dataChanged.emit(self.index(0, 0), self.index(0, self.columnCount() - 1))

    def set_dats(self, dats):
        self.beginResetModel()
        self.dats = dats
        self.offset = 0
        tot = len(dats)
        self.spinBox.blockSignals(T)
        self.spinBox.setRange(1, tot)
        self.spinBox.setSuffix(f" /{tot} {self.suffix}")
        self.spinBox.setValue(1)
        self.spinBox.blockSignals(F)
        self.endResetModel()

    def add_dat(self, dat):
        self.beginResetModel()
        tot = len(self.dats)
        self.dats.append(dat)
        self.offset = tot
        self.spinBox.blockSignals(T)
        self.spinBox.setRange(1, tot + 1)
        self.spinBox.setSuffix(f" /{tot + 1} {self.suffix}")
        self.spinBox.setValue(tot + 1)
        self.spinBox.blockSignals(F)
        self.endResetModel()

    def del_dat(self):
        self.beginResetModel()
        tot = len(self.dats)
        self.dats.pop(self.offset)
        self.spinBox.blockSignals(T)
        self.spinBox.setRange(1, tot - 1)
        self.spinBox.setSuffix(f" /{tot - 1} {self.suffix}")
        self.spinBox.setValue(self.offset + 1)
        self.spinBox.blockSignals(F)
        self.offset = self.spinBox.value() - 1
        self.endResetModel()
