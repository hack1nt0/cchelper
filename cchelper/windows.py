from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtSql import *
from typing import Sequence, List, Tuple

__all__ = [
    "OpenedDialog",
    "UpDownWindow",
    "MultiComboBox",
    "AlertBox",
    "ConfirmBox",
]
T, F = True, False


class OpenedDialog(QDialog):
    resize_signal: Signal = Signal()

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.P = parent
        if hasattr(self.P, 'resize_signal'):
            self.P.resize_signal.connect(self._resize)
    
    def resizeEvent(self, event: QResizeEvent) -> None:
        self.resize_signal.emit()
        super().resizeEvent(event)

    def _resize(self):
        if self.P:
            W, H = self.P.width(), self.P.height()
            if hasattr(self.P, 'statusbar'):
                H -= self.P.statusbar.height()
            self.resize(W, H)

    def done(self, arg__1: int=0) -> None:
        return super().done(arg__1)
    
    

class UpDownWindow(QDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setAutoFillBackground(T)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.A = QPropertyAnimation(self, b'pos', self)
        self.A.setDuration(100)
        self.is_down = F
        self.setEnabled(F)
        self.hide()

    def down(self):
        if self.A.state() == QAbstractAnimation.State.Running:
            return
        self.is_down = T
        P = self.parentWidget()
        W, H = P.width(), P.height()
        if hasattr(P, 'statusbar'):
            H -= P.statusbar.height()
        self.setFixedSize(W, H)
        P.setEnabled(F)
        self.setEnabled(T)
        self.show()
        x = 0
        ys = -H
        yt = 0
        self.A.setStartValue(QPoint(x, ys))
        self.A.setEndValue(QPoint(x, yt))
        self.A.start()

    def up(self) -> bool:
        if not self.is_down:
            return T
        if self.A.state() == QAbstractAnimation.State.Running:
            return
        self.is_down = F
        self.parentWidget().setEnabled(T)
        self.setEnabled(F)
        self.show()
        W, H = self.width(), self.height()
        x = 0
        yt = -H
        ys = 0
        self.A.setStartValue(QPoint(x, ys))
        self.A.setEndValue(QPoint(x, yt))
        self.A.start()
        return T
    
    def setEnabled(self, arg__1: bool) -> None:
        for chd in self.children():
            if isinstance(chd, QWidget):
                chd.setEnabled(arg__1)
    
    # def resizeEvent(self, event: QResizeEvent) -> None:
    #     logger.debug(event.size())
    #     return super().resizeEvent(event)

    def _resize(self, size: QSize) -> None:
        self.setFixedSize(size)
        for w in self.children():
            if isinstance(w, UpDownWindow) and w.is_down:
                w._resize(size)

class MultiComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

        self.currentIndexChanged.connect(
            lambda: self.model().item(0).setText(self.currentText())
        )

    def eventFilter(self, object, event):
        if object == self.view().viewport():
            if event.type() == QEvent.MouseButtonRelease:
                index = self.view().indexAt(event.pos())
                if index.row() == 0:
                    return T
                item: QStandardItem = self.model().item(index.row())
                if item.checkState() == Qt.Checked:
                    item.setCheckState(Qt.Unchecked)
                else:
                    item.setCheckState(Qt.Checked)
                self.currentIndexChanged.emit(self.currentIndex())
                return T
        return F

    def addItem(self, text, data=None, first=F):
        item = QStandardItem()
        item.setText(text)
        if data is None:
            item.setData(text)
        else:
            item.setData(data)
        if first:
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        else:
            item.setFlags(
                Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable
            )
        item.setData(Qt.Unchecked, Qt.CheckStateRole)
        self.model().appendRow(item)

    def addItems(self, texts: Sequence[str]) -> None:
        self.addItem(texts[0], first=T)
        for txt in texts[1:]:
            self.addItem(txt)

    def setCurrentIndex(self, index: int) -> None:
        for row in range(1, self.model().rowCount()):
            item: QStandardItem = self.model().item(row)
            item.setCheckState(Qt.CheckState.Checked if (index >> row - 1) & 1 else Qt.CheckState.Unchecked)
        self.currentIndexChanged.emit(index)

    def currentIndex(self) -> int:
        mask = 0
        for i in range(1, self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                mask |= 1 << (i - 1)
        return mask

    def currentText(self) -> str:
        display = []
        for row in range(1, self.model().rowCount()):
            item: QStandardItem = self.model().item(row)
            if item.checkState() == Qt.Checked:
                display.append(item.data())
        return ",".join(display) if display else "*"


class AlertBox(QDialog):
    def __init__(self, parent, text, title="CcAlert") -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setWindowTitle(title)
        self.vlayout = QVBoxLayout(self)
        self.label = QLabel(self)
        self.label.setText(text)
        self.vlayout.addWidget(self.label)


class ConfirmBox(QDialog):
    YES = 1
    NO = 2
    CANCEL = 0

    def __init__(self, parent, text, title="CcConfirmation") -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setWindowTitle(title)
        self.vlayout = QVBoxLayout(self)

        self.label = QLabel(self)
        self.label.setText(text)
        self.vlayout.addWidget(self.label)

        self.spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.CButton = QPushButton(self)
        self.CButton.setText("Cancel")
        self.YButton = QPushButton(self)
        self.YButton.setText("Yes")
        self.YButton.setFocus()
        self.NButton = QPushButton(self)
        self.NButton.setText("No")

        self.hlayout = QHBoxLayout()
        self.hlayout.addItem(self.spacer)
        self.hlayout.addWidget(self.YButton)
        self.hlayout.addWidget(self.NButton)
        self.hlayout.addWidget(self.CButton)
        self.CButton.clicked.connect(lambda: self.done(ConfirmBox.CANCEL))
        self.YButton.clicked.connect(lambda: self.done(ConfirmBox.YES))
        self.NButton.clicked.connect(lambda: self.done(ConfirmBox.NO))
        self.vlayout.addLayout(self.hlayout)

        # self.setFixedSize(self.sizeHint())
        self.setMaximumSize(600, 600)  # TODO now working


# class FeedbackBox(QDialog):
#     OK = 0
#     RETRY = 1

#     def __init__(
#         self, parent, msgs: List[Tuple[bool, str]], title="CcFeedbacks"
#     ) -> None:
#         super().__init__(parent)
#         # self.setWindowModality(Qt.WindowModality.WindowModal)
#         self.setWindowTitle(title)
#         self.vlayout = QVBoxLayout(self)

#         self.tbl = QTableWidget(len(msgs), 2, self)
#         self.tbl.horizontalHeader().setSectionResizeMode(
#             0, QHeaderView.ResizeMode.ResizeToContents
#         )
#         self.tbl.horizontalHeader().setSectionResizeMode(
#             1, QHeaderView.ResizeMode.Stretch
#         )
#         self.tbl.horizontalHeader().setVisible(F)
#         self.tbl.setTabKeyNavigation(F)
#         # self.tbl.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
#         # self.lst.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
#         for row, (status, msg) in enumerate(msgs):
#             item = QTableWidgetItem(MARK_V if status else MARK_X)
#             item.setForeground(GREEN if status else RED)
#             item.setFlags(Qt.ItemFlag.ItemIsEnabled)
#             self.tbl.setItem(row, 0, item)
#             item = QTableWidgetItem(msg)
#             item.setToolTip(msg)
#             item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
#             self.tbl.setItem(row, 1, item)
#         self.vlayout.addWidget(self.tbl)

#         self.hlayout = QHBoxLayout()
#         self.retryButton = QPushButton(self)
#         self.retryButton.setText("Retry")
#         self.retryButton.clicked.connect(lambda: self.done(FeedbackBox.RETRY))
#         self.okButton = QPushButton(self)
#         self.okButton.setText("OK")
#         self.okButton.setFocus()
#         self.okButton.clicked.connect(lambda: self.done(FeedbackBox.OK))
#         self.spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
#         self.hlayout.addItem(self.spacer)
#         self.hlayout.addWidget(self.retryButton)
#         self.hlayout.addWidget(self.okButton)
#         self.vlayout.addLayout(self.hlayout)
