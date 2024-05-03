from PySide6.QtCore import QObject, QTimerEvent
from PySide6.QtGui import QCloseEvent, QFocusEvent, QKeyEvent, QMouseEvent
import pyte.charsets
import pyte.escape
import pyte.modes
from cchelper import *
from cchelper.fileviewer import FileViewerD

import sys
import traceback
from datetime import datetime
import pyte
import paramiko
import tempfile
from typing import Iterable

from .backend import BasePty, LocalPty, SshPty

pyte.escape.CHA
keymap = {
    # Qt.Key.Key_Tab: b"\x09",
    # Qt.Key_Backspace: chr(127).encode(),
    # Qt.Key_Escape: chr(27).encode(),
    # Qt.Key_AsciiTilde: chr(126).encode(),
    Qt.Key_Up: b"\x1bOA",
    Qt.Key_Down: b"\x1bOB",
    Qt.Key_Left: b"\x1bOD",
    Qt.Key_Right: b"\x1bOC",
    Qt.Key.Key_Home: b"\x1bOH",
    Qt.Key.Key_End: b"\x1bOF",
    Qt.Key.Key_Insert: b"\x1b[2~",
    Qt.Key.Key_Delete: b"\x1b[3~",
    Qt.Key.Key_PageUp: b"\x1b[5~",
    Qt.Key.Key_PageDown: b"\x1b[6~",
    Qt.Key_F1: b"\x1bOP",
    Qt.Key_F2: b"\x1bOQ",
    Qt.Key_F3: b"\x1bOR",
    Qt.Key_F4: b"\x1bOS",
    Qt.Key_F5: b"\x1b[15~",
    Qt.Key_F6: b"\x1b[17~",
    Qt.Key_F7: b"\x1b[18~",
    Qt.Key_F8: b"\x1b[19~",
    Qt.Key_F9: b"\x1b[20~",
    Qt.Key_F10: b"\x1b[21~",
    Qt.Key_F11: b"\x1b[23~",
    Qt.Key_F12: b"\x1b[24~",
}

align: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeading

# backend: pty, ssh
colors = {
    "black": QColor(0x00, 0x00, 0x00),
    "red": QColor(0xAA, 0x00, 0x00),
    "green": QColor(0x00, 0xAA, 0x00),
    "blue": QColor(0x00, 0x00, 0xAA),
    "cyan": QColor(0x00, 0xAA, 0xAA),
    "brown": QColor(0xAA, 0xAA, 0x00),
    "yellow": QColor(0xFF, 0xFF, 0x44),
    "magenta": QColor(0xAA, 0x00, 0xAA),
    "white": QColor(0xFF, 0xFF, 0xFF),
}


class TerminalWidget(QWidget):
    nxt_page_signal: Signal = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.IBeamCursor)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.default_pen: QColor = None
        self.default_brush: QColor = None
        self.set_color(QApplication.palette())
        self.painting = F
        self.pixmap = QPixmap(0, 0)
        self.need_fullrepaint = F
        self.need_paintcursor = F
        self.lock = threading.Lock()
        self.cursorX = 0
        self.cursorY = 0

        ### Start-up
        self.backend: BasePty = None
        # self.set_pty()
        # self.resize(800, 600)


    def set_pty(
        self,
    ):
        if self.backend is not None:
            self.killTimer(self.ptimer)
            # self.killTimer(self.rtimer)
            self.backend.close()

        self.backend = SshPty()
        self.backend.connect("localhost", 22, "dy", "6666")
        # self.backend = LocalPty()
        # self.backend.connect()
        self.set_font()
        self._resize()

        self.ptimer = self.startTimer(100)
        # self.rtimer = self.startTimer(20)
        
        class ReadThread(QThread):
            def __init__(self, terminal: TerminalWidget, parent: QObject) -> None:
                super().__init__(parent)
                self.terminal = terminal
                
            def run(self) -> None:
                while T:
                    if not self.terminal.read():
                        return
                    time.sleep(0.02)
        
        self.read_thread = ReadThread(self, self)
        self.read_thread.start()

        self.backend.write(b"export LANG=zh_CN.UTF-8\n")
        self.backend.write(b"export TERM=xterm\n")
        # self.backend.write(f"cd {os.getcwd()}\n".encode())
        # self.backend.write(b"clear\n")

    def set_color(self, v: QPalette):
        self.default_pen = v.text().color()
        self.default_brush = v.window().color()
        self.need_fullrepaint = T

    def set_font(self):
        # self._font = QFont('Courier New', 15)
        self._font = conf.font
        # self.setFont(self._font) #TODO not working
        self.fm = QFontMetricsF(self._font)
        self.CH = self.fm.height()
        self.CW = self.fm.horizontalAdvance("W")
        self.XM = 0.0
        self.YM = 0.0
        self.need_fullrepaint = T

    def _resize(self):
        self.lock.acquire()
        W, H = self.width(), self.height()
        self.rows, self.cols = int(H / self.CH), int(W / self.CW)
        if not (W == self.pixmap.width() and H == self.pixmap.height()):
            self.pixmap = QPixmap(W, H)
        if self.backend is not None and not (
            self.rows == self.backend.rows and self.cols == self.backend.cols
        ):
            self.backend.resize(self.rows, self.cols)
        self.need_fullrepaint = T
        self.lock.release()

    def get_pen(self, color_name: str = "default") -> QColor:
        ret = None
        match color_name:
            case None:
                ret = self.default_brush
            case "default":
                ret = self.default_pen
            case _:
                ret = (
                    colors[color_name]
                    if color_name in colors
                    else QColor(int(color_name, 16))
                )
        return ret

    def get_brush(self, color_name: str = "default") -> QColor:
        ret = None
        match color_name:
            case None:
                ret = self.default_pen
            case "default":
                ret = self.default_brush
            case _:
                ret = (
                    colors[color_name]
                    if color_name in colors
                    else QColor(int(color_name, 16))
                )
        return ret

    def paintEvent(self, event):
        if self.painting:
            return
        self.lock.acquire()
        self.painting = T

        # Paint text
        painter = QPainter(self.pixmap)
        painter.setFont(self._font)
        dirtyRows = self.backend.dirtyRows
        if self.need_fullrepaint:
            self.need_fullrepaint = F
            self.pixmap.fill(self.get_brush())
            self.need_paintcursor = T
            # dirties = self.backend.dirties(refresh=T)
            dirtyRows = range(self.backend.rows)
        elif (
            self.cursorX != self.backend.cursor.x
            or self.cursorY != self.backend.cursor.y
        ):
            # dirties = self.backend.dirties(old_cursor_line=self.cursorY)
            dirtyRows.add(self.cursorY)
            self.cursorX = self.backend.cursor.x
            self.cursorY = self.backend.cursor.y
            self.need_paintcursor = T

        def drawText(text: str, fg: str, bg: str, x: int, y: int):
            if not text:
                return 0
            print(text, fg, bg, x, y)
            w = self.fm.horizontalAdvance(text)
            # w = self.fontMetrics().boundingRect(text).width()
            box = QRectF(x, y, w, self.CH)
            # if bg != 'default':
            painter.fillRect(box, self.get_brush(bg))
            painter.setPen(self.get_pen(fg))
            painter.drawText(box, text)
            return w

        for row in dirtyRows:
            x = 0
            y = row * self.CH
            clear_rect = QRectF(x, y, self.width(), self.CH)  # TODO margin
            painter.fillRect(clear_rect, self.get_brush())
            text, fg, bg = "", None, None
            for c in self.backend.row(row):
                if c.bg == bg and c.fg == fg:
                    text += c.data
                else:
                    if text:
                        x += drawText(text, fg, bg, x, y)
                    text = c.data
                    fg, bg = c.fg, c.bg
            if text:
                x += drawText(text, fg, bg, x, y)

        self.backend.clearDirty()

        # Paint cursor TODO blink
        if self.need_paintcursor:
            bcol = QColor(0x00, 0xAA, 0x00, 80)
            brush = QBrush(bcol)
            painter.setPen(Qt.NoPen)
            painter.setBrush(brush)
            painter.drawRect(
                QRectF(
                    self.cursorX * self.CW + self.XM,
                    self.cursorY * self.CH + self.YM,
                    self.CW,
                    self.CH,
                )
            )
        painter.end()
        # Paint pixmap
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pixmap)
        painter.end()
        self.painting = F
        self.lock.release()

    def write(self, dat: bytes):
        # self.lock.acquire()
        self.backend.write(dat)
        # self.lock.release()

    def read(self) -> bytes:
        dat = self.backend.read()
        if dat:
            self.lock.acquire()
            self.backend.write_to_screen(dat)
            self.lock.release()
        return dat

    def keyPressEvent(self, event: QKeyEvent) -> None:
        logger.debug(f"I: {event}")
        text = event.text()
        key = event.key()
        modifiers = event.modifiers()
        ctrl = modifiers == Qt.KeyboardModifier.ControlModifier
        if ctrl and key == Qt.Key.Key_V:
            self.write(QGuiApplication.clipboard().text().encode())
            return
        elif text:
            self.write(text.encode())
            return
        else:
            self.write(keymap.get(key))
            return
        return super().keyPressEvent(event)

    def focusInEvent(self, event: QFocusEvent) -> None:
        self.need_paintcursor = T
        return super().focusInEvent(event)

    def focusOutEvent(self, event: QFocusEvent) -> None:
        self.need_paintcursor = F
        return super().focusOutEvent(event)

    # def mousePressEvent(self, event: QMouseEvent) -> None:
    #     self.need_paintcursor = T
    #     self.mouse_select_begin = event.pos()
    #     return super().mousePressEvent(event)

    # def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    #     if event.pos() == self.mouse_select_begin:
    #         return super().mouseReleaseEvent(event)
    #     self.lock.acquire()
    #     _, tmpfn = tempfile.mkstemp(suffix=".pyte")
    #     with open(tmpfn, "w") as w:

    #         def write_lines(
    #             lines: Iterable[pyte.screens.StaticDefaultDict[int, pyte.screens.Char]]
    #         ):
    #             for line in lines:
    #                 for col in range(self.cols):
    #                     c = line[col]
    #                     w.write(c.data)
    #                 w.write("\n")

    #         write_lines(self.backend.screen.history.top)
    #         write_lines((self.backend.screen.buffer[row] for row in range(self.backend.rows)))
    #         write_lines(self.backend.screen.history.bottom)
    #     self.lock.release()
    #     w = FileViewerD(self)
    #     w.set_file(File(tmpfn))
    #     w.exec()

    def resizeEvent(self, event):
        self._resize()
        return super().resizeEvent(event)

    def timerEvent(self, event: QTimerEvent) -> None:
        match event.timerId():
            case self.ptimer:
                self.update()
            # case self.rtimer:
            #     self.read()
        return super().timerEvent(event)

    def wheelEvent(self, event: QWheelEvent):
        y = event.angleDelta().y()
        if y > 0:
            self.backend.screen.prev_page()
            self.nxt_page_signal.emit(-1)
        else:
            self.backend.screen.next_page()
            self.nxt_page_signal.emit(+1)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.backend.close()
        self.read_thread.terminate()
        return super().closeEvent(event)
