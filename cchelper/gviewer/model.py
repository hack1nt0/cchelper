from cchelper import *

class GModel(QAbstractTableModel):
    def __init__(
        self,
        parent,
    ) -> None:
        super().__init__(parent)
        self.dats: List = []

    def rowCount(self, parent: QModelIndex = None) -> int:
        return len(self.dats)

    def columnCount(self, parent: QModelIndex = None) -> int:
        return 1

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        dat = self.dats[index.row()]
        raw = dat.name
        ret = None
        match role:
            case Qt.ItemDataRole.DisplayRole:
                ret = raw
            case Qt.ItemDataRole.TextAlignmentRole:
                ret = Qt.AlignmentFlag.AlignCenter
        return ret

    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlags:
        mask = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        return mask

    # def headerData(
    #     self,
    #     section: int,
    #     orientation: Qt.Orientation = Qt.Orientation.Horizontal,
    #     role: int = Qt.ItemDataRole.DisplayRole,
    # ) -> Any:
    #     if orientation == Qt.Orientation.Vertical:
    #         match role:
    #             case Qt.ItemDataRole.DisplayRole:
    #                 return section + 1
    #         return
    #     ret = None
    #     col = self.cols[section]
    #     match role:
    #         case Qt.ItemDataRole.DisplayRole:
    #             match col:
    #                 case "interactive":
    #                     ret = "I"
    #                 case "checked":
    #                     ret = "C"
    #                 case _:
    #                     ret = ' '.join(map(lambda s: s.capitalize(), col.split('_')))
    #         case Qt.ItemDataRole.ToolTipRole:
    #             ret = col
    #     return ret
