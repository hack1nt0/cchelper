from cchelper import *


class VerdictDelegate(QStyledItemDelegate):
    view_signal: Signal = Signal(File)

    def createEditor(
        self,
        parent: QWidget,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> QWidget:
        if not index.isValid():
            return
        col = index.model().cols[index.column()]
        assert col != "added_as_test"
        self.view_signal.emit(index.model().data(index, role=Qt.ItemDataRole.EditRole))
        return
