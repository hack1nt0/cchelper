from PySide6.QtCore import QTimerEvent
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
import pyperclip as clipboard

import select

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

        self.pixmap = QPixmap(self.width(), self.height())
        self.need_fullrepaint = F
        self.need_paintcursor = F
        self.set_font()
        self.lock = threading.Lock()
        self.cursorX = 0
        self.cursorY = 0
        ### Start-up
        self.set_pty()
        self.resize(800, 600)

    def set_pty(
        self,
        ip="localhost",
        # username="root",
        # password="root",
        # port=10022,
        username="dy",
        password="6666",
        port=22,
        rows=24,
        cols=80,
    ):
        self.rows = rows
        self.cols = cols
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(ip, username=username, password=password, port=port)

        self.ssh_client.exec_command
        # t = self.ssh_client.get_transport()
        # t.window_size = 2147483647
        # t.packetizer.REKEY_BYTES = pow(2, 40)
        # t.packetizer.REKEY_PACKETS = pow(2, 40)
        self.channel: paramiko.Channel = None
        self.ptimer: int = None
        self.rtimer: int = None

        self.bscreen = pyte.HistoryScreen(
            columns=cols, lines=rows, history=9999, ratio=0.3
        )
        self.bstream = pyte.ByteStream(self.bscreen)

        self.default_pen: QColor = None
        self.default_brush: QColor = None
        self.set_color(QApplication.palette())

        self.painting = F

    def new_shell(self, wd: str):
        if self.channel is not None:
            self.killTimer(self.ptimer)
            self.killTimer(self.rtimer)
            self.channel.close()

        # env = os.environ.copy()
        # env["LANG"] = "zh_CN.UTF-8"
        self.channel = self.ssh_client.invoke_shell(
            term='xterm',
            width=self.cols, height=self.rows,
        )
        self.channel.set_combine_stderr(T)
        self.channel.settimeout(None)

        timeout = 60
        while not self.channel.recv_ready() and timeout > 0:
            time.sleep(0.1)  # TODO
            timeout -= 0.1

        assert self.channel.recv_ready()
        self.ptimer = self.startTimer(100)
        self.rtimer = self.startTimer(20)

        self.bscreen.reset()
        self.write(b"export LANG=zh_CN.UTF-8\n")
        self.write(b"export TERM=xterm\n")
        self.write(f"cd {wd}\n".encode())
        self.write(b"clear\n")

    
    def read(self):
        if self.channel.recv_ready():
            b = self.channel.recv(1024*4)
            if len(b) == 0:
                return
            self.lock.acquire()
            try:
                self.bstream.feed(b)
            except Exception as e:
                logger.exception(e)
            self.lock.release()

    def write(self, v: bytes | bytearray):
        # TODO send_ready
        if not v:
            return
        extra = len(v)
        while extra:
            send = self.channel.send(v)
            if send == 0 and extra:
                logger.error(f"Pty closed before write: {v.decode(errors='replace')}")
                return
            extra -= send
            v = v[send:]

    def set_color(self, v: QPalette):
        self.default_pen = v.text().color()
        self.default_brush = v.window().color()
        self.need_fullrepaint = T
    
    def set_font(self):
        if conf.font is None:
            return
        # self._font = QFont('Courier New', 15)
        self._font = conf.font
        # self.setFont(self._font) #TODO not working
        self.fm = QFontMetricsF(self._font)
        self.CH = self.fm.height()
        self.CW = self.fm.horizontalAdvance("W")
        self.XM = 0.0
        self.YM = 0.0
        self.need_fullrepaint = T

    def get_pen(self, color_name: str = 'default') -> QColor:
        ret = None
        match color_name:
            case None:
                ret = self.default_brush
            case 'default':
                ret = self.default_pen
            case _:
                ret = colors[color_name] if color_name in colors else QColor(int(color_name, 16))
        return ret

    def get_brush(self, color_name: str = 'default') -> QColor:
        ret = None
        match color_name:
            case None:
                ret = self.default_pen
            case 'default':
                ret = self.default_brush
            case _:
                ret = colors[color_name] if color_name in colors else QColor(int(color_name, 16))
        return ret

    def paintEvent(self, event):
        if self.painting:
            return
        self.lock.acquire()
        # self.read()
        self.painting = T
        dirty = {}
        if self.need_fullrepaint:
            self.need_fullrepaint = F
            W, H = self.width(), self.height()
            self.rows, self.cols = int(H / self.CH), int(W / self.CW)
            if not (W == self.pixmap.width() and H == self.pixmap.height()):
                self.pixmap = QPixmap(W, H)
            if not (self.rows == self.bscreen.lines and self.cols == self.bscreen.columns):
                self.bscreen.resize(self.rows, self.cols)
                self.channel.resize_pty(self.cols, self.rows)
            self.pixmap.fill(self.get_brush())
            dirty = set(range(self.rows))
            self.need_paintcursor = T
        else:
            dirty = self.bscreen.dirty

        painter = QPainter(self.pixmap)
        painter.setFont(self._font)

        def drawText(text: str, fg: str, bg: str, x: int, y: int):
            if not text:
                return 0
            print(fg, bg, text)
            w = self.fm.horizontalAdvance(text)
            # w = self.fontMetrics().boundingRect(text).width()
            box = QRectF(x, y, w, self.CH)
            # if bg != 'default':
            painter.fillRect(box, self.get_brush(bg))
            painter.setPen(self.get_pen(fg))
            painter.drawText(box, text)
            return w

        # text = "xs = preorder.split(',')"
        # drawText(text, 'default', 'default', 0, 0)

        cursor = self.bscreen.cursor
        if self.cursorX != cursor.x or self.cursorY != cursor.y:
            dirty.add(self.cursorY)
            self.cursorX = cursor.x
            self.cursorY = cursor.y
            # self.bscreen.dirty.add(self.cursorY)
            self.need_paintcursor = T

        # Paint text

        for lnum in dirty:
            x = self.XM
            y = self.YM + lnum * self.CH
            clear_rect = QRectF(x, y, self.width(), self.CH)
            painter.fillRect(clear_rect, self.get_brush())
            line = self.bscreen.buffer[lnum]
            if not line:
                continue
            text, fg, bg = "", None, None
            for col in range(self.bscreen.columns):
                c = line[col]
                if c.bg == bg and c.fg == fg:
                    text += c.data
                else:
                    x += drawText(text, fg, bg, x, y)
                    text = c.data
                    fg, bg = c.fg, c.bg
            drawText(text, fg, bg, x, y)
        self.bscreen.dirty.clear()
        # Paint cursor TODO blink
        if self.need_paintcursor:
            self.need_paintcursor = F
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
        else:
            pass  # TODO
        painter.end()
        # Paint pixmap
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pixmap)
        painter.end()
        self.painting = F
        self.lock.release()

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

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.need_paintcursor = T
        self.mouse_select_begin = event.pos()
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.pos() == self.mouse_select_begin:
            return super().mouseReleaseEvent(event)
        self.lock.acquire()
        _, tmpfn = tempfile.mkstemp(suffix=".pyte")
        with open(tmpfn, "w") as w:

            def write_lines(
                lines: Iterable[pyte.screens.StaticDefaultDict[int, pyte.screens.Char]]
            ):
                for line in lines:
                    for col in range(self.cols):
                        c = line[col]
                        w.write(c.data)
                    w.write("\n")

            write_lines(self.bscreen.history.top)
            write_lines((self.bscreen.buffer[row] for row in range(self.rows)))
            write_lines(self.bscreen.history.bottom)
        self.lock.release()
        w = FileViewerD(self)
        w.set_file(File(tmpfn))
        w.exec()

    # def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
    #     x, y = event.pos().x(), event.pos().y()
    #     row = max(0, int((y + self.CH - 1) // self.CH) - 1)
    #     col = max(0, int((x + self.CW - 1) // self.CW) - 1)
    #     #TODO pos -> row/col
    #     self.view_file()
    #     return super().mouseDoubleClickEvent(event)

    def resizeEvent(self, event):
        self.need_fullrepaint = T
        return super().resizeEvent(event)

    def timerEvent(self, event: QTimerEvent) -> None:
        match event.timerId():
            case self.ptimer:
                self.update()
            case self.rtimer:
                self.read()
        return super().timerEvent(event)

    def wheelEvent(self, event: QWheelEvent):
        y = event.angleDelta().y()
        if y > 0:
            self.bscreen.prev_page()
            self.nxt_page_signal.emit(-1)
        else:
            self.bscreen.next_page()
            self.nxt_page_signal.emit(+1)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.channel.close()
        self.ssh_client.close()
        return super().closeEvent(event)
