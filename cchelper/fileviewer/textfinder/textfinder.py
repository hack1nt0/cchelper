from cchelper import *
from .textfinder_ui import Ui_TextFinder

class TextFinder(QDialog, Ui_TextFinder):
    find_signal: Signal = Signal(str, int)
    find_kill_signal: Signal = Signal()
    closed_signal: Signal = Signal()

    def __init__(
        self,
        parent: QWidget,
    ) -> None:
        super().__init__(parent)
        self.setupUi(self)
        # self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        # self.setWindowFlags(Qt.WindowType.Tool)
        # self.setWindowModality(Qt.WindowModality.WindowModal)

        self.stopButton.setEnabled(F)
        self.stopButton.clicked.connect(self.find_kill_signal.emit)
        self.lineEdit.installEventFilter(self)
        self.spinBox.setReadOnly(T)

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() == Qt.Key.Key_L and e.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.lineEdit.setFocus()
            return T
        if e.key() == Qt.Key.Key_C and e.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.stopButton.animateClick()
            return T
        return super().keyPressEvent(e)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        # print(event, watched)
        if watched == self.lineEdit and event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Return and event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
            self.block_widgets(T)
            self.find_signal.emit(self.lineEdit.text(), -1)
            return T
        if watched == self.lineEdit and event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Return:
            self.block_widgets(T)
            self.find_signal.emit(self.lineEdit.text(), +1)
            return T
        return super().eventFilter(watched, event)

    def update_num(self, idx, tot):
        self.spinBox.setValue(idx)
        self.spinBox.setSuffix(f'/{tot}')
        self.block_widgets(F)

    def update_ret(self, v):
        if v:
            self.lineEdit.setStyleSheet('background-color: auto')
        else:
            self.lineEdit.setStyleSheet('background-color: red')
        self.block_widgets(F)
    
    def block_widgets(self, v):
        self.lineEdit.setEnabled(not v)
        if not v:
            self.lineEdit.setFocus()
        self.spinBox.setEnabled(not v)
        self.stopButton.setEnabled(v)
    
    def done(self, arg__1: int) -> None:
        self.closed_signal.emit()
        return super().done(arg__1)