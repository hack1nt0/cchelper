from cchelper import *
from .codesubmit_ui import Ui_CodeSubmitter
import tempfile
from subprocess import Popen, PIPE
import pyperclip as clipboard
import cchelper.tasksubmitter.cpp as cpp

class CodeSubmitter(QDialog, Ui_CodeSubmitter):
    def __init__(self, file: File, parent: QWidget) -> None:
        super().__init__(parent, Qt.WindowType.Dialog)
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        font = QFont(*conf.font)
        for te in [self.finalTextEdit, self.ppTextEdit, self.errTextEdit]:
            te.setFont(font)
            te.setTabStopDistance(QFontMetricsF(font).horizontalAdvance(' ' * 4))
        
        # self.finalTextEdit.setStyleSheet('color: blue')
        # self.ppTextEdit.setStyleSheet('color: blue')
        self.errTextEdit.setStyleSheet('color: red')
        self.finalTextEdit.setReadOnly(True)
        self.ppTextEdit.setReadOnly(True)
        self.errTextEdit.setReadOnly(True)

        self.final = None
        self.path = file.path
        if self.path.endswith('.cpp'):
            self.final, pp = cpp.preprocess(self.path)
            pp = ''.join(pp)
            self.ppTextEdit.setPlainText(pp)
        else:
            with open(self.path, 'r') as s:
                self.final = s.readlines()
            # self.removeMainButton.setEnabled(F)
        self.finalTextEdit.setPlainText(''.join(self.final))

        self.removeMainButton.setShortcut("Alt+R")
        self.removeMainButton.clicked.connect(self.remove_main)

        self.validateButton.setShortcut("Alt+V")
        self.validateButton.clicked.connect(self.validate)
        self.copyButton.setShortcut("Alt+C")
        self.copyButton.clicked.connect(self.copy)

        self.switch_tab_key = QShortcut(QKeySequence("Alt+Tab"), self)
        self.current_tab_idx = 0
        self.switch_tab_key.activated.connect(self.switch_tab)
        self.tabWidget.setCurrentIndex(self.current_tab_idx)

    def switch_tab(self):
        self.current_tab_idx += 1
        self.current_tab_idx %= 3
        self.tabWidget.setCurrentIndex(self.current_tab_idx)

    def switch_tab(self):
        self.current_tab_idx += 1
        self.current_tab_idx %= self.tabWidget.count()
        self.tabWidget.setCurrentIndex(self.current_tab_idx)
        
    def validate(self):
        if not self.path.endswith('.cpp'):
            return
        _, tmpfn = tempfile.mkstemp(suffix='.cpp')
        with open(tmpfn, 'w') as s:
            s.write(self.finalTextEdit.toPlainText())
        cmpl_cmd = File(tmpfn).compile_cmd
        p = Popen(cmpl_cmd.split(), stderr=PIPE, text=True)
        if p.wait():
            self.errTextEdit.setPlainText(p.stderr.read())
            self.label.setText("Compilation Error")
            # self.tab_3.setFocus() #TODO
            self.tabWidget.setCurrentIndex(2)
        else:
            self.tabWidget.setCurrentIndex(0)
            self.errTextEdit.clear()
            self.label.setText("Compilation Ok")
        os.remove(tmpfn)

    def copy(self):
        clipboard.copy(self.finalTextEdit.toPlainText().replace('\t', ' ' * 4))
        self.label.setText('Copied')
    
    def remove_main(self):
        txt = self.final
        lines = []
        MAIN = ''
        match os.path.splitext(self.path)[1]:
            case '.cpp':
                MAIN = r'\s*(int|void)\s+main\('
            case '.py':
                MAIN = r'if\s+__name__\s*==\s*[\'"]__main__[\'"]:'
        for line in txt:
            if re.match(MAIN, line):
                break
            lines.append(line)
        txt = ''.join(lines)
        self.finalTextEdit.setPlainText(txt)
        self.label.setText('Main removed')