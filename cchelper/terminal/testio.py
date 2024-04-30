
from PySide6.QtCore import QTimerEvent, Qt
from PySide6.QtWidgets import QWidget
from cchelper import *
from .testio_ui import Ui_TestIO
from .backend import LocalPty
import queue

class TestIO(QMainWindow, Ui_TestIO):
    def __init__(self, parent: QWidget=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.runButton.clicked.connect(self.run)
        self.pty = LocalPty(100, 100)

        # self.loop = asyncio.get_event_loop()
        # self.loop.create_task(self.read())
        # self.loop.run_forever()

        self.que = queue.Queue()
        global_threadpool.submit(self.read)

        self.startTimer(100)

    def run(self):
        self.output.clear()
        self.pty.write(self.input.toPlainText().encode())
    
    def read(self):
            while T:
                # await asyncio.sleep(0)
                data = self.pty.read()
                # if not data:
                #     return
                self.que.put(data)
    
    def timerEvent(self, event: QTimerEvent) -> None:
        if not self.que.empty():
            data = self.que.get().decode('utf-8', 'replace')
            self.output.appendPlainText(data)
            self.display.setPlainText(str(self.pty))
            ptr = self.display.textCursor()
            ptr.setPosition(self.pty.cursorP())
            ptr.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)
            self.display.setTextCursor(ptr)
        return super().timerEvent(event)
    
    def close(self) -> bool:
        self.pty.close()
        return super().close()