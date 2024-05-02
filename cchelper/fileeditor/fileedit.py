from PySide6.QtGui import QPaintEvent
from cchelper import *

NORMAL = "normal"
INSERT = "insert"
COMMAND = "command"
VISUAL = "visual"
VISUAL_LINE_MODE = "visual line mode"
VISUAL_BLOCK_MODE = "visual block mode"


class FileEdit(QPlainTextEdit):
    mode_signal: Signal = Signal(str)

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        font = conf.font
        self.setFont(font)
        self.setTabStopDistance(QFontMetricsF(font).horizontalAdvance(" " * 4))
        self._mode = None
        self.mode = NORMAL

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, v):
        self._mode = v
        self.mode_signal.emit(v)

    # def paintEvent(self, e: QPaintEvent) -> None:
    #     super().paintEvent(e)
    #     self.textCursor()
    #     ptr = self.cursor()
    #     painter = QPainter()
    #     painter.begin(self.viewport())
    #     painter.setPen(RED)
    #     painter.setBrush(YELLOW)
    #     painter.drawText(ptr.pos(), "HI")
    #     print(ptr.pos())
    #     painter.end()

    # def eventFilter(self, watched: QObject, e: QEvent) -> bool:
    #     if watched is self.textEdit:
    #         if e.type() == QEvent.Type.KeyPress and e.key() == Qt.Key.Key_Tab:
    #             self.textEdit.insertPlainText(" " * 4)
    #             return T
    #     return super().eventFilter(watched, e)


    def keyPressEvent(self, e: QKeyEvent) -> None:
        blocked = False
        match (e.modifiers(), e.key()):
            case (Qt.KeyboardModifier.NoModifier, Qt.Key.Key_Tab):
                self._indent(tabs=1)
            case (Qt.KeyboardModifier.ShiftModifier, Qt.Key.Key_Backtab):
                self._indent(tabs=-1)
            case (Qt.KeyboardModifier.NoModifier, Qt.Key.Key_Return):
                ptr = self.textCursor()
                ptr.beginEditBlock()
                prev_tabs = self._current_indents()
                super().keyPressEvent(e)
                self._indent(tabs=prev_tabs)
                ptr.endEditBlock()
            case _:
                super().keyPressEvent(e)
        # if self.mode == NORMAL:
        #     blocked = True
        #     match (e.modifiers(), e.key()):
        #         case (Qt.KeyboardModifier.NoModifier, Qt.Key.Key_J):
        #             self.moveCursor(QTextCursor.MoveOperation.Down)
        #             ptr = self.textCursor()
        #             if self.mode == VISUAL_LINE_MODE:
        #                 ptr.select(QTextCursor.SelectionType.BlockUnderCursor)
        #                 self.setTextCursor(ptr)
        #         case (Qt.KeyboardModifier.NoModifier, Qt.Key.Key_K):
        #             self.moveCursor(QTextCursor.MoveOperation.Up)
        #         case (Qt.KeyboardModifier.NoModifier, Qt.Key.Key_H):
        #             self.moveCursor(QTextCursor.MoveOperation.Left)
        #         case (Qt.KeyboardModifier.NoModifier, Qt.Key.Key_L):
        #             self.moveCursor(QTextCursor.MoveOperation.Right)
        #         case (Qt.KeyboardModifier.NoModifier, Qt.Key.Key_I):
        #             self.mode = INSERT
        #         case (_, Qt.Key.Key_V):
        #             self.mode = VISUAL_LINE_MODE
        #         case _:
        #             blocked = False
        # elif self.mode == INSERT:
        #     match (e.modifiers(), e.key()):
        #         case (_, Qt.Key.Key_Escape) | (
        #             Qt.KeyboardModifier.MetaModifier,
        #             Qt.Key.Key_BracketLeft,
        #         ):
        #             self.mode = NORMAL
        #             blocked = True
        #         case _:
        #             print(e)
        # if not blocked:
        #     return super().keyPressEvent(e)
    
    def _indent(self, tabs: int=1):
        ptr = self.textCursor()
        ptr.beginEditBlock()
        S, E = ptr.position(), ptr.position()
        if ptr.hasSelection():
            S, E = ptr.selectionStart(), ptr.selectionEnd()
            if S > E:
                S, E = E, S
        ptr.setPosition(S)
        ptr.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        L = 0
        while True:
            L += 1
            before = ptr.blockNumber()
            ptr.movePosition(QTextCursor.MoveOperation.NextBlock)
            if ptr.blockNumber() == before or ptr.position() >= E:
                break
        ptr.setPosition(S)
        ptr.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        while L:
            self._indent_line(ptr, tabs)
            ptr.movePosition(QTextCursor.MoveOperation.NextBlock)
            L -= 1
        # ptr.setPosition(S + 1)
        # ptr.movePosition(QTextCursor.MoveOperation.NextCharacter, QTextCursor.MoveMode.KeepAnchor, E - S + tabs * L)
        # self.setTextCursor(ptr)
        ptr.endEditBlock()
        
    def _indent_line(self, ptr: QTextCursor, tabs: int=1):
        if tabs < 0:
            ptr.movePosition(QTextCursor.MoveOperation.NextCharacter, QTextCursor.MoveMode.KeepAnchor, 1)
            match ptr.selectedText():
                case '\t' | ' ':
                    ptr.removeSelectedText()
                case _:
                    pass
        else:
            ptr.insertText('\t' * tabs)

    def _current_indents(self) -> int:
        ptr = self.textCursor()
        ptr.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        while True:
            ptr.movePosition(QTextCursor.MoveOperation.NextCharacter, QTextCursor.MoveMode.KeepAnchor, 1)
            if not ptr.selectedText().endswith('\t'):
                break
        return len(ptr.selectedText()) - 1
    
    
