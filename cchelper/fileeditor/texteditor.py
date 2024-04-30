from cchelper import *
from .texteditor_ui import Ui_TextEditor

LIMIT = 1024 ** 2 * 5

class TextEditor(QWidget, Ui_TextEditor):
    reset_signal: Signal = Signal()
    changed_signal: Signal = Signal()
    saved_signal: Signal = Signal()
    renamed_signal: Signal = Signal()
    ee_signal: Signal = Signal()

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.saveButton.setShortcut("Ctrl+S")
        self.saveButton.clicked.connect(self.save)

        font = QFont(*conf.font)
        self.textEdit.setFont(font)
        self.textEdit.setTabStopDistance(QFontMetricsF(font).horizontalAdvance(" " * 4))
        # self.label.setStyleSheet("background-color : blue; color : white;")
        # self.label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.currentLine = 0
        self.lines = 0
        self.textEdit.blockCountChanged.connect(self.lines_changed)
        self.textEdit.cursorPositionChanged.connect(self.cursor_changed)
        self.textEdit.textChanged.connect(self.changed_signal.emit)

    def set_file(self, file: File | str):
        #TODO check too large size
        self.file = file
        if file is None:
            return
        self.file = file if isinstance(file, File) else File(file)
        # self.label.setText(self.file.path)
        if os.path.getsize(self.file.path) > LIMIT:
            self.saveButton.setEnabled(F)
            self.textEdit.setPlainText(self.file.tail(LIMIT))
        else:
            try:
                with open(self.file.path, "r") as s:
                    self.textEdit.setPlainText(s.read())
                self.reset_signal.emit()
            except UnicodeDecodeError as e:
                self.saveButton.setEnabled(F)
                return

    def save(self):
        if self.saveButton.isEnabled():
            with open(self.file.path, "w") as w:
                w.write(self.textEdit.toPlainText())
            # try:
            #     source = self.file.path
            #     target = conf.working_dir(os.path.basename(self.file.path))
            #     os.symlink(source, target)
            # except:
            #     pass
        self.saved_signal.emit()

    def lines_changed(self, v: int):
        self.lines = v
        self.statLabel.setText(f"{self.currentLine}/{self.lines}")

    def cursor_changed(self, v: QTextCursor = None):
        if v is None:
            v = self.textEdit.textCursor()
        self.currentLine = v.blockNumber()
        self.statLabel.setText(f"{self.currentLine}/{self.lines}")
