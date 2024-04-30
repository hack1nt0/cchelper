import PySide6.QtCore
from PySide6.QtGui import QCloseEvent, QKeyEvent
from cchelper import *
from .codeeditor_ui import Ui_CodeEditor
from cchelper.fileviewer import TextFinder, FindHighlighter


class CodeEditor(QWidget, Ui_CodeEditor):
    reset_signal: Signal = Signal()
    changed_signal: Signal = Signal()
    saved_signal: Signal = Signal()
    renamed_signal: Signal = Signal()
    ee_signal: Signal = Signal()

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        # logger.debug(self.textEdit.font())

#         self.setStyleSheet(r"""
# QPlainTextEdit {
#     /* font: 12px "JetBrains Mono"; */
#     color: white;
#     background-color: rgb(2,4,94);
#     selection-background-color: rgb(5,128,128);
#     selection-color: black;
#     /* selection-background-color: darkblue;
#     selection-color: white; */
# }
#                            """)
        # font = QFont(*conf.font)
        # if font != self.textEdit.font():
        #     self.textEdit.setFont(font)
        self.textEdit.setTabStopDistance(self.textEdit.fontMetrics().horizontalAdvance(" " * 4))
        # self.label.setStyleSheet("background-color : blue; color : white;")
        # self.label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        # self.buttonBox.button(QDialogButtonBox.StandardButton.Save).clicked.connect(
        #     self.save
        # )

        self.saveButton.setShortcut("Ctrl+S")
        self.saveButton.clicked.connect(self.save)
        # self.closeButton.clicked.connect(self.done)
        # self.editButton.setShortcut("Ctrl+E")
        # self.editButton.clicked.connect(self.edit_external)

        # self.textEdit.installEventFilter(self)
        self.currentLine = 0
        self.lines = 0
        self.textEdit.blockCountChanged.connect(self.lines_changed)
        self.textEdit.cursorPositionChanged.connect(self.cursor_changed)
        self.textEdit.textChanged.connect(self.changed_signal.emit)

        # Find
        self.highlighter = FindHighlighter(self.textEdit.document())
        self.finder = TextFinder(self)
        self.finder.find_signal.connect(self.find_text)
        self.finder.closed_signal.connect(self.find_clear)
        self.finder.hide()
        self.findButton.clicked.connect(self.finder.exec)
        self.findButton.setShortcut('Ctrl+F')
        self.regex: QRegularExpression = None

    # def eventFilter(self, watched: QObject, e: QEvent) -> bool:
    #     if watched is self.textEdit:
    #         if e.type() == QEvent.Type.KeyPress and e.key() == Qt.Key.Key_Tab:
    #             self.textEdit.insertPlainText(" " * 4)
    #             return T
    #     return super().eventFilter(watched, e)

    def set_file(self, file: File):
        self.file = file
        self.path = file.path
        try:
            with open(self.file.path, "r") as s:
                self.textEdit.setPlainText(s.read())
            self.reset_signal.emit()
        except UnicodeDecodeError as e:
            self.saveButton.setEnabled(F)
            return

        self.mtime = os.path.getmtime(self.file.path)

        # if os.path.splitext(self.file.path)[1] in (
        #     lang.suffix for lang in conf.languages
        # ):
        self.langMenu = QMenu(self)
        self.langExclusiveSet = QActionGroup(self)
        for lang in conf.languages:
            act = self.langExclusiveSet.addAction(
                self.langMenu.addAction(lang.name)
            )
            act.setCheckable(T)
            if lang.suffix == self.file.suffix:
                act.setChecked(T)
        self.langMenu.triggered.connect(self.change_language)
        self.langButton.setMenu(self.langMenu)
        # else:
        #     self.langButton.setEnabled(F)

    def clear(self):
        self.textEdit.clear()

    def save(self):
        if os.path.getmtime(self.file.path) > self.mtime:
            self.set_file(self.file)
        else:
            with open(self.file.path, "w") as w:
                w.write(self.textEdit.toPlainText())
            # try:
            #     source = self.file.path
            #     target = conf.working_dir(os.path.basename(self.file.path))
            #     os.symlink(source, target)
            # except:
            #     pass
            self.mtime = os.path.getmtime(self.file.path)
        self.saved_signal.emit()

    def edit_external(self):
        self.save()
        path = self.file.path
        new_path = os.path.join(conf.working_dir(), os.path.basename(path))
        if os.path.exists(new_path):
            path = new_path
        cmd = f"{conf.editor} {path}"
        subprocess.run(cmd, check=T, shell=T)

    def change_language(self, act: QAction):
        self.save()
        lang = [lang for lang in conf.languages if lang.name == act.text()][0]
        path = os.path.splitext(self.file.path)[0] + lang.suffix
        if not os.path.exists(path):
            with open(path, 'w') as w:
                w.write(lang.template)
        self.file.path = path
        self.set_file(self.file)

    def lines_changed(self, v: int):
        self.lines = v
        self.statLabel.setText(f"{self.currentLine}/{self.lines}")

    def cursor_changed(self, v: QTextCursor = None):
        if v is None:
            v = self.textEdit.textCursor()
        self.currentLine = v.blockNumber()
        self.statLabel.setText(f"{self.currentLine}/{self.lines}")

    def find_text(self, regex: str, dir: int):
        if self.regex is None or self.regex.pattern() != regex:
            self.regex = QRegularExpression(regex)
            self.highlighter.pattern = regex
            self.highlighter.rehighlight()
        if not regex:
            return
        if dir < 0:
            ptr = self.textEdit.document().find(self.regex, self.textEdit.textCursor(), options=QTextDocument.FindFlag.FindBackward)
        else:
            ptr = self.textEdit.document().find(self.regex, self.textEdit.textCursor())
        self.textEdit.setTextCursor(ptr)
        self.finder.block_widgets(F)

    def find_clear(self):
        self.highlighter.pattern = ''
        self.highlighter.rehighlight()

    
    def closeEvent(self, event: QCloseEvent) -> None:
        logger.debug('CE close')
        return super().closeEvent(event)