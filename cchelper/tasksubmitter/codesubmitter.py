from cchelper import *
from .codesubmit_ui import Ui_CodeSubmitter
import tempfile
from subprocess import Popen, PIPE
import cchelper.tasksubmitter.cpp as cpp

class CodeSubmitter(QDialog, Ui_CodeSubmitter):
    def __init__(self, parent: QWidget) -> None:
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

    def set_task(self, task: Task):
        self.task = task
        self.final = None
        self.file = task.solver
        match self.file.suffix:
            case '.cpp':
                self.final, pp = cpp.preprocess(self.file)
                pp = ''.join(pp)
                self.ppTextEdit.setPlainText(pp)
            case _:
                with open(self.file.path, 'r') as s:
                    self.final = s.readlines()
            # self.removeMainButton.setEnabled(F)
        self.main = File(f"Main{self.file.suffix}").create()
        self.main.taskname = self.task.name
        with open(self.main.path, 'w') as w:
            w.writelines(self.final)
        self.finalTextEdit.setPlainText(''.join(self.final))
        assert os.path.exists(self.main.path)

    def switch_tab(self):
        self.current_tab_idx += 1
        self.current_tab_idx %= self.tabWidget.count()
        self.tabWidget.setCurrentIndex(self.current_tab_idx)
        
    def validate(self):
        cmpl_cmd = self.main.compile_cmd
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

    def copy(self):
        QGuiApplication.clipboard().setText(self.finalTextEdit.toPlainText().replace('\t', ' ' * 4))
        self.label.setText('Copied')
    
    def remove_main(self):
        txt = self.final
        lines = []
        MAIN = ''
        match os.path.splitext(self.file.path)[1]:
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