from cchelper import *
from .fileviewer_ui import Ui_FileViewer
from .textfinder.textfinder import TextFinder

class FileViewer(QWidget, Ui_FileViewer):
    found_num_signal: Signal = Signal(int, int)
    found_ret_signal: Signal = Signal(int)
    edit_file_signal: Signal = Signal(File)

    def __init__(
        self,
        parent: QWidget = None,
    ) -> None:
        super().__init__(parent)
        self.setupUi(self)
        # self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        # font = QFont(*conf.font)
        # self.textEdit.setFont(font)
        self.textEdit.setTabStopDistance(self.textEdit.fontMetrics().horizontalAdvance(' ' * 4))
        # self.label.setStyleSheet("background-color : blue; color : white;")
        # self.label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        self.path = None
        self.url = None

        self.textEdit.setReadOnly(True) # Cannot select by keyboard
        self.textEdit.setTextInteractionFlags(self.textEdit.textInteractionFlags() | Qt.TextInteractionFlag.TextSelectableByKeyboard)

        # self.closeButton.setShortcut('Esc')
        # self.closeButton.clicked.connect(self.done)
        # self.textEdit.textChanged.connect(self.highlight)
        self.highlighter: QSyntaxHighlighter = FindHighlighter(self.textEdit.document())
        self.textEdit.setFocus()
        self.pageSzSpinBox.valueChanged.connect(self.psz_changed)
        self.pageNoSpinBox.valueChanged.connect(self.pno_changed)
        self.filling = F
        self.headButton.clicked.connect(self.head)
        self.tailButton.setShortcut('Ctrl+T')
        self.tailButton.toggled.connect(self.tail)
        self.timer: QTimer = None

        self.pattern = None
        d = TextFinder(self)
        # d.setWindowModality(Qt.WindowModality.WindowModal)
        d.find_signal.connect(self.find_wrapper)
        d.find_kill_signal.connect(self.kill_find)
        self.found_num_signal.connect(d.update_num)
        self.found_num_signal.connect(self.jump_and_select_found)
        self.found_ret_signal.connect(d.update_ret)
        d.hide()
        self.textFinder = d
        self.findButton.clicked.connect(self.textFinder.exec)
        self.findButton.setShortcut('Ctrl+F')
        self.founds = []
        self.idxF = 0
        self.idxP = 0
        self.totP = 1
        self.found_zero = T
        self.found_killed = F


        self.iniB = conf.bytes_per_page

        # self.editButton.setShortcut("Ctrl+E")
        # self.editButton.clicked.connect(self.edit_file)

        # self.closeButton.clicked.connect(lambda: self.done(0))
        

    def find_wrapper(self, pattern, direction):
        global_threadpool.submit(self.find, pattern, direction)

    def kill_find(self):
        self.found_killed = T
    
    def find(self, pattern, direction):
        if self.pattern != pattern:
            self.founds = []
            self.idxF = 0 if direction > 0 else -1
            self.idxP = 0 if direction > 0 else self.totP - 1
            self.found_zero = T
            self.pattern = pattern
            self.highlight(pattern)
        else:
            if self.found_zero:
                self.found_num_signal.emit(0, 0)
                return
        
        self.found_killed = F
        
        def nxt_idxP():
            return (self.idxP + 1) % self.totP if direction > 0 else (self.idxP - 1) % self.totP

        while T:
            if self.found_killed:
                break
            if self.founds:
                if 0 <= self.idxF < len(self.founds):
                    break
                else:
                    self.idxP = nxt_idxP()
                    self.founds.clear()
                    continue
            else:
                assert(not self.founds)
                try:
                    for m in re.finditer(self.pattern, self.get_text(self.pageSzSpinBox.value(), self.idxP + 1)[1]):
                        s, c = m.start(), m.end() - m.start()
                        self.founds.append((s, c))
                except re.error:
                    self.found_ret_signal.emit(0)
                    return
                if self.founds:
                    self.idxF = 0 if direction > 0 else len(self.founds) - 1
                    break
                if self.found_zero and nxt_idxP() == (0 if direction > 0 else self.totP - 1):
                    break
                self.idxP = nxt_idxP()
                continue
        
        if self.founds:
            self.found_zero = F
            n = len(self.founds)
            self.found_num_signal.emit(self.idxF + 1, n)
            self.idxF += 1 if direction > 0 else -1
        else:
            self.found_num_signal.emit(0, 0)
    
    def jump_and_select_found(self, idx, tot):
        if tot == 0:
            return
        if self.idxP + 1 != self.pageNoSpinBox.value():
            self.pageNoSpinBox.setValue(self.idxP + 1)
        #TODO ptr.movePosition(QTextCursor.MoveOperation.NextCharacter, QTextCursor.MoveMode.MoveAnchor, n) always return false
        ptr = self.textEdit.textCursor()
        p, c = self.founds[idx - 1]
        ptr.setPosition(p) # TODO movePosition not working
        ptr.movePosition(QTextCursor.MoveOperation.NextCharacter, QTextCursor.MoveMode.KeepAnchor, c)
        self.textEdit.setTextCursor(ptr) #TODO
        self.textEdit.ensureCursorVisible()

    def find_next_in_page(self, pattern):
        if self.pattern != pattern:
            self.pattern = pattern
            self.founds.clear()
            try:
                for m in re.finditer(self.pattern, self.textEdit.toPlainText()):
                    s, c = m.start(), m.end() - m.start()
                    self.founds.append((s, c))
            except re.error:
                self.found_ret_signal.emit(0)
                return
            self.found_ret_signal.emit(1)
            self.idxF = len(self.founds) - 1
            self.highlight(pattern)
            self.found_tot_signal.emit(len(self.founds))

        if self.founds:
            #TODO ptr.movePosition(QTextCursor.MoveOperation.NextCharacter, QTextCursor.MoveMode.MoveAnchor, n) always return false
            ptr = self.textEdit.textCursor()
            nxt_idx = (self.idxF + 1) % len(self.founds)
            p, c = self.founds[nxt_idx]
            ptr.setPosition(p)
            ptr.movePosition(QTextCursor.MoveOperation.NextCharacter, QTextCursor.MoveMode.KeepAnchor, c)
            self.textEdit.setTextCursor(ptr) #TODO
            self.textEdit.ensureCursorVisible()
            self.idxF = nxt_idx
            self.found_cur_signal.emit(self.idxF + 1)
        else:
            self.found_cur_signal.emit(0)
    
    def set_file(self, url: str | File):
        if isinstance(url, File):
            self.path = url.path
            self.file = url
        else:
            self.path = url
            self.file = File(url)
        self.filling = T
        # self.label.setText(url)
        # self.textEdit.setStyleSheet('color: auto')
        with open(self.path, 'rb') as s:
            self.totB = s.seek(0, 2)
            self.pageSzSpinBox.setRange(1, self.totB)
            self.pageSzSpinBox.setSuffix(f'/{self.totB} bytes')
            self.pageSzSpinBox.setValue(self.iniB)
            self.totP = (self.totB + self.iniB - 1) // self.iniB
            self.pageNoSpinBox.setRange(1, self.totP)
            self.pageNoSpinBox.setSuffix(f'/{self.totP} pages')
            self.pageNoSpinBox.setValue(1)
            self.fill_text()
            # cursor = self.textEdit.textCursor()
            # cursor.setPosition()
            # cursor.setfo
        self.filling = F

    def tail_file(self):
        if self.filling:
            return
        self.filling = T
        try:
            with open(self.path, 'rb') as r:
                self.totB = r.seek(0, 2)
                self.pageSzSpinBox.setRange(1, self.totB)
                self.pageSzSpinBox.setSuffix(f'/{self.totB} bytes')
                self.pageSzSpinBox.setValue(max(self.pageSzSpinBox.value(), self.iniB))
                psz = self.pageSzSpinBox.value()
                self.totP = (self.totB + psz - 1) // psz 
                self.pageNoSpinBox.setRange(1, self.totP)
                self.pageNoSpinBox.setSuffix(f'/{self.totP} pages')
                self.pageNoSpinBox.setValue(self.totP)
                self.fill_text()
                self.textEdit.verticalScrollBar().setValue(self.textEdit.verticalScrollBar().maximum())
        except:
            self.textEdit.clear()
        self.filling = F
        
    def tail(self, v):
        if v:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.tail_file)
            self.pageNoSpinBox.setEnabled(F)
            self.pageSzSpinBox.blockSignals(T)
            self.timer.setInterval(1000 // conf.refresh_rate)
            self.timer.start()
        else:
            self.timer.stop()
            self.timer = None
            self.pageNoSpinBox.setEnabled(T)
            self.pageSzSpinBox.blockSignals(F)

    def head(self):
        self.tailButton.setChecked(F)
        self.pageNoSpinBox.setValue(1)
        self.fill_text()
    
    def highlight(self, pattern: str):
        self.highlighter.pattern = pattern
        self.highlighter.rehighlight()

    def clear_hightlight(self):
        self.highlighter.pattern = None
    
    def get_text(self, psz, pno, ) -> Tuple[bool, str]:
        s_byte = (pno - 1) * psz
        e_byte = min(self.totB, s_byte + psz)
        s = None
        # with open(self.path, 'rb') as r: #TODO
        #     s_byte0, e_byte0 = s_byte, e_byte
        #     while T:
        #         # print(s_byte, e_byte)
        #         r.seek(s_byte)
        #         try:
        #             s = r.read(e_byte - s_byte).decode()
        #             break
        #         except UnicodeDecodeError as e:
        #             # print(e.start, e.end, s_byte, e_byte)
        #             if e.end == e_byte - s_byte:
        #                 if e_byte < self.totB:
        #                     e_byte += 1
        #                     continue
        #                 else:
        #                     break
        #             elif e.start == 0:
        #                 if 0 <= s_byte:
        #                     s_byte -= 1
        #                     continue
        #                 else:
        #                     break
        #     if s is None: 
        #         s = r.read(e_byte0 - s_byte0).decode(errors='replace')
        #         s.replace('�', '<span style="color: red">�</span>')
        #         s = f'<pre style="font-size: 12px; font-family: \'JetBrains Mono\'">{html.escape(s)}</pre>'
        #         return F, s
        #     elif e_byte0 < e_byte:
        #         s = f'<pre style="font-size: 12px; font-family: \'JetBrains Mono\'">{html.escape(s[:-1])}<span style="color: red">{s[-1]}</span></pre>'
        #         return F, s
        #     elif s_byte < s_byte0:
        #         s = f'<pre style="font-size: 12px; font-family: \'JetBrains Mono\'"><span style="color: red">{s[0]}</span>{html.escape(s[1:])}</pre>'
        #         return F, s
        #     else:
        #         return T, s
        with open(self.path, 'rb') as r: #TODO
            r.seek(s_byte)
            s = r.read(e_byte - s_byte).decode(errors='replace')
        return T, s
        
    def fill_text(self):
        psz = self.pageSzSpinBox.value()
        pno = self.pageNoSpinBox.value()
        ret, txt = self.get_text(psz, pno)
        if ret:
            self.textEdit.setPlainText(txt)
        else:
            self.textEdit.clear()
            self.textEdit.appendHtml(txt)

    def psz_changed(self, psz):
        if self.filling:
            return
        self.filling = T
        self.totP = (self.totB + psz - 1) // psz
        self.pageNoSpinBox.setRange(1, self.totP)
        self.pageNoSpinBox.setSuffix(f'/{self.totP} pages')
        self.fill_text()
        self.filling = F
    
    def pno_changed(self, pno):
        if self.filling:
            return
        self.fill_text()

    def edit_file(self):
        # cmd = f"{conf.editor} {self.path}"
        # subprocess.run(cmd, check=T, shell=T)
        self.edit_file_signal.emit(self.file)

    def done(self, v):
        self.tailButton.setChecked(F)
        # self.clear_hightlight() 
        # self.textEdit.clear()
        return super().done(v)

class FindHighlighter(QSyntaxHighlighter):
    found_singal: Signal = Signal(object)

    def __init__(self, document: QTextDocument):
        super().__init__(document)
        self.pattern: re.Pattern = None
        self.fmt = QTextCharFormat()
        self.fmt.setBackground(BLUE)
        self.fmt.setForeground(GREEN)

    def highlightBlock(self, text: str) -> None:
        # print(f'[[{self.currentBlock().blockNumber()}]] - [[{text}]]')
        if not self.pattern or not text:
            return
        for m in re.finditer(self.pattern, text):
            s, c = m.start(), m.end() - m.start()
            self.setFormat(s, c, self.fmt)
        # super().highlightBlock(text)