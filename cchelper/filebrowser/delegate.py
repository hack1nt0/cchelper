from PySide6.QtCore import QModelIndex, QPersistentModelIndex, QSize
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QStyleOptionViewItem
from cchelper import *


class FileDelegate(QStyledItemDelegate):
    edit_signal: Signal = Signal(File)
    expand_signal: Signal = Signal(QModelIndex)

    def createEditor(
        self,
        parent: QWidget,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> QWidget:
        if not index.isValid():
            return
        path = index.model().filePath(index)
        if os.path.isfile(path):
            self.edit_signal.emit(File(path))
        else:
            self.expand_signal.emit(index)


class FoundDelegate(QStyledItemDelegate):
    edit_signal: Signal = Signal(File)

    def createEditor(
        self,
        parent: QWidget,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> QWidget:
        if not index.isValid():
            return
        if index.column() == 0:
            self.edit_signal.emit(File(index.data(role=Qt.ItemDataRole.EditRole)))

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> None:
        if index.column() == 1:
            self.initStyleOption(option, index)
            painter.save()
            doc = QTextDocument()
            doc.setHtml(option.text)
            painter.translate(option.rect.left(), option.rect.top())
            clip = QRect(0, 0, option.rect.width(), option.rect.height())
            doc.drawContents(painter, clip)
            painter.restore()
        else:
            return super().paint(painter, option, index)
    
    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex) -> QSize:
        if index.column() == 1:
            self.initStyleOption(option, index)
            doc = QTextDocument()
            doc.setHtml(option.text)
            doc.setTextWidth(option.rect.width())
            return QSize(doc.idealWidth(), doc.size().height())
        else:
            return super().sizeHint(option, index)
