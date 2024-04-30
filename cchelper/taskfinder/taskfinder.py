from cchelper import *
from .taskfinder_ui import Ui_TaskFinder


class TaskFinder(QDialog, Ui_TaskFinder):
    def __init__(self, parent: QWidget, condition) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.label.setStyleSheet("background-color : blue; color : white;")

        self.buttonBox.button(QDialogButtonBox.StandardButton.Reset).clicked.connect(
            self.reset
        )
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).clicked.connect(
            lambda: self.done(1)
        )

        self.tagsComboBox.addItems(conf.tags)

        self.statusComboBox.addItem('*')
        for ts in TS:
            self.statusComboBox.addItem(ts.value)
            
        self.reset()

        self.condition = condition

    def get_bool(self, state: Qt.CheckState) -> bool:
        match state:
            case Qt.CheckState.Unchecked:
                return F
            case Qt.CheckState.Checked:
                return T
            case Qt.CheckState.PartiallyChecked:
                return None

    def done(self, arg__1: int) -> None:
        if arg__1:
            c = self.condition
            c.url = self.urlLineEdit.text().strip().lower()
            c.name = self.nameLineEdit.text().strip().lower()
            c.tags = self.tagsComboBox.currentIndex()
            c.solver = self.solverContainsTextEdit.toPlainText().strip().lower()
            c.ctimeL = self.cTimeLEdit.dateTime().toSecsSinceEpoch()
            c.ctimeR = self.cTimeREdit.dateTime().toSecsSinceEpoch()
            c.status = self.statusComboBox.currentText()
            if c.status == '*':
                c.status = None
            else:
                c.status = TS(c.status)
        return super().done(arg__1)

    def reset(self):
        self.urlLineEdit.clear()
        self.nameLineEdit.clear()
        self.solverContainsTextEdit.clear()
        self.tagsComboBox.setCurrentIndex(0)
        self.cTimeLEdit.setDate(QDate.currentDate().addYears(-1))
        self.cTimeREdit.setDate(QDate.currentDate().addDays(1))


def compare(e, q):
    if q is None:
        return True
    ok = True
    for k in ["tags"]:
        ev, qv = getattr(e, k), q[k]
        ok &= (ev & qv) == qv
        if not ok:
            return False
    for k in ["level"]:
        ev, qv = getattr(e, k), q[k]
        ok &= qv == 0 or ev == qv
        if not ok:
            return False
    for k in ["solved", "interact"]:
        ev, qv = getattr(e, k), q[k]
        ok &= qv is None or ev == qv
        if not ok:
            return False
    for k in ["contest", "problem", "url"]:
        ev, qv = getattr(e, k), q[k]
        ok &= not qv or qv.lower() in ev.lower()
        if not ok:
            return False
    for k in ["ctime"]:
        ev, ql, qr = getattr(e, k), q[k + "_l"], q[k + "_r"]
        ok &= ql <= ev < qr
        if not ok:
            return False

    return ok
