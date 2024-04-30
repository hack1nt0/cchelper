from PySide6.QtCore import QTimerEvent
from PySide6.QtGui import QCloseEvent, QKeyEvent, QPaintEvent, QResizeEvent
from cchelper import *
from .backend import SshTty, LocalPty


import pty
import shlex
import signal
import tty


KEY_MAP = {
    Qt.Key_Backspace: chr(127).encode(),
    Qt.Key_Escape: chr(27).encode(),
    Qt.Key_AsciiTilde: chr(126).encode(),
    Qt.Key_Up: b"\x1b[A",
    Qt.Key_Down: b"\x1b[B",
    Qt.Key_Left: b"\x1b[D",
    Qt.Key_Right: b"\x1b[C",
    Qt.Key_PageUp: "~1".encode(),
    Qt.Key_PageDown: "~2".encode(),
    Qt.Key_Home: "~H".encode(),
    Qt.Key_End: "~F".encode(),
    Qt.Key_Insert: "~3".encode(),
    Qt.Key_Delete: "~4".encode(),
    Qt.Key_F1: "~a".encode(),
    Qt.Key_F2: "~b".encode(),
    Qt.Key_F3: "~c".encode(),
    Qt.Key_F4: "~d".encode(),
    Qt.Key_F5: "~e".encode(),
    Qt.Key_F6: "~f".encode(),
    Qt.Key_F7: "~g".encode(),
    Qt.Key_F8: "~h".encode(),
    Qt.Key_F9: "~i".encode(),
    Qt.Key_F10: "~j".encode(),
    Qt.Key_F11: "~k".encode(),
    Qt.Key_F12: "~l".encode(),
}


class TextEditTerminal(QPlainTextEdit):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setCursor(Qt.IBeamCursor)
        self.setFocusPolicy(Qt.StrongFocus)
        font = QFont(*conf.font)
        self.setFont(font)
        self.fm = QFontMetricsF(font)
        self.setTabStopDistance(self.fm.horizontalAdvance(" " * 4))
        self._char_height = self.fm.height()
        self._char_width = self.fm.horizontalAdvance("W")

        # self.backend.refresh_signal.connect(self.refresh)

        # self.pty = SshTty(100, 100, "localhost", username="dy", password="6666")
        self.pty = LocalPty(100, 100)
        # self.pty_thread = threading.Thread(target=self.open_pty)

        self.startTimer(1000)

    def refresh(self, data: bytes = None):
        # if not self.pty._screen.dirty:
        #     return
        print(str(self.pty))
        self.setPlainText(str(self.pty))
        # self.pty._screen.dirty.clear()
        try:
            ptr = self.textCursor()
            ptr.setPosition(self.pty.cursorP())
            self.setTextCursor(ptr)
        except:
            pass

    def timerEvent(self, e: QTimerEvent) -> None:
        self.refresh()
        # return super().timerEvent(e)

    def resizeEvent(self, e: QResizeEvent) -> None:
        if self.pty:
            self.pty.resize(
                int(e.size().height() / self._char_height),
                int(e.size().width() / self._char_width),
            )
        return super().resizeEvent(e)

    def keyPressEvent(self, e: QKeyEvent) -> None:
        text = e.text()
        key = e.key()
        data = None
        if text and key != Qt.Key_Backspace:
            data = text.encode("utf-8")
        else:
            s = KEY_MAP.get(key)
            if s:
                data = s
        if data:
            self.pty.write(data)
        # return super().keyPressEvent(e)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.pty.close()
        return super().closeEvent(event)
