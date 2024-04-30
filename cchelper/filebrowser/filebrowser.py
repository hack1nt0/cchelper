from PySide6.QtCore import QTimerEvent
from PySide6.QtGui import QCloseEvent
from cchelper import *
from .model import FoundModel, FileTreeModel
import glob
from cchelper.fileeditor import CodeEditor
from .delegate import FileDelegate, FoundDelegate
from .filebrowser_ui import Ui_FileBrowser
from cchelper.filefinder import FileFinder
import html


class FileBrowser(QWidget, Ui_FileBrowser):
    edit_file_signal: Signal = Signal(File)
    found_file_signal: Signal = Signal(object)

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        # self.model = FileModel(self)
        self.model = FileTreeModel(self)
        self.model.setNameFilterDisables(False)

        self.view.setModel(self.model)
        self.deleg = FileDelegate(self)
        self.deleg.edit_signal.connect(self.edit_file_signal.emit)
        self.deleg.expand_signal.connect(self.expand)
        self.view.setItemDelegate(self.deleg)
        self.view.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.view.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.view.header().hideSection(2)
        self.view.header().hideSection(3)

        self.found_model = FoundModel(self)
        self.tableView.setModel(self.found_model)
        self.found_deleg = FoundDelegate(self)
        self.found_deleg.edit_signal.connect(self.edit_file_signal.emit)
        self.tableView.setItemDelegate(self.found_deleg)
        self.tableView.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self.tableView.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        self.tableView.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.tableView.verticalHeader().setVisible(F)

        # self.found_file_signal.connect(lambda v: print(v))

        self.menu = QMenu(self)
        self.menu.addAction("Expand Recursively", self.expand_rec)
        self.menu.addAction("Collpase All", self.collapse_all)
        self.menu.addAction("Delete", self.del_file)
        self.view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.popup_menu)
        self.view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.newButton.setShortcut("Ctrl+N")
        self.newButton.clicked.connect(self.new_file)

        self.find_pattern: str = None
        self.find_killed: threading.Event = threading.Event()
        self.foundW.hide()
        self.timer_id = self.startTimer(1000)
        self.found_file_signal.connect(self.found_file)

        ### FIND
        # self.findButton.setToolTip("Find File (Shift+Ctrl+F)")
        # self.findButton.setIcon(QIcon(paths.img("search.png")))
        # self.findButton.clicked.connect(self.find_file)
        # self.findButton.setShortcut("Shift+Ctrl+F")


    def set_root(self, root: File):
        self.view.setRootIndex(self.model.setRootPath(root.path))
        # self.model.endResetModel()
        # self.model.beginResetModel()
        # self.model.dats.clear()

        # for path in glob.glob(os.path.join(root.path, '**', '*'), recursive=T):
        #     if os.path.isfile(path):
        #         file = File(os.path.relpath(path, root.path))
        #         self.model.dats.append(file)
        # self.model.endResetModel()

    def popup_menu(self, point: QPoint):
        idx = self.view.indexAt(point)
        if not idx.isValid():
            return
        self.menu.popup(QCursor().pos())

    def expand_rec(self):
        idxs = self.view.selectionModel().selectedIndexes()
        if not idxs:
            return
        for idx in idxs:
            self.view.expandRecursively(idx)
    
    def expand(self, idx: QModelIndex):
        if self.view.isExpanded(idx):
            self.view.collapse(idx)
        else:
            self.view.expand(idx)

    def collapse_all(self):
        self.view.collapseAll()

    def new_file(self):
        fn, ok = QInputDialog.getText(
            self,
            "New File",
            "Input filename (Unix-like): ",
            # flags=Qt.WindowType.ToolTip,
        )
        if ok:
            try:
                with open(fn, "w") as w:
                    pass
            except Exception as e:
                logger.exception(e)

    def find_file(self):
        try:
            for root, dns, fns in os.walk(self.model.rootPath()):
                # logger.debug(fns)
                # logger.debug(self.find_killed.is_set())
                if self.find_killed.is_set():
                    break
                for fn in fns:
                    if self.find_killed.is_set():
                        break
                    try:
                        fn = os.path.join(root, fn)
                        text = open(fn).read()  # TODO
                    except:
                        pass
                    else:
                        for m in re.finditer(self.find_pattern, text):
                            if self.find_killed.is_set():
                                break
                            s, t = m.start(), m.end()
                            C = 100
                            ss, tt = max(0, s - C), t + C
                            ret = (
                                fn,
                                f"<pre style=\"font-size: 12px; font-family: 'JetBrains Mono', 'Courier New'\">{html.escape(text[ss:s])}<span style=\"color: red\">{html.escape(text[s:t])}</span>{html.escape(text[t:tt])}</pre>",
                            )
                            # logger.debug(ret)
                            self.found_file_signal.emit(ret)
                            # self.found_model.insert(ret)
                            # self.found_file(ret)  # TODO
                            # print(ret)
                            break
            if self.find_killed.is_set():
                self.find_killed.clear()
        except Exception as e:
            logger.exception(e)

    def found_file(self, v):
        # logger.debug(v)
        self.found_model.beginInsertRows(
            QModelIndex(), self.found_model.rowCount(), self.found_model.rowCount()
        )
        self.found_model.dats.append(v)
        self.found_model.endInsertRows()
        self.tableView.updateGeometries()

    def del_file(self):
        idxs = self.view.selectionModel().selectedIndexes()
        for idx in idxs:
            if idx.isValid():
                (
                    self.model.rmdir(idx)
                    if self.model.isDir(idx)
                    else self.model.remove(idx)
                )

    def timerEvent(self, event: QTimerEvent) -> None:
        if event.timerId() == self.timer_id:
            if self.lineEdit.text() != self.find_pattern:
                self.find_pattern = self.lineEdit.text().strip()
                if not self.find_pattern:
                    self.find_killed.set()
                    self.fsW.show()
                    self.foundW.hide()
                else:
                    self.fsW.hide()
                    self.foundW.show()
                    self.find_killed.set()
                    self.find_killed.clear()
                    self.found_model.clear()
                    global_threadpool.submit(self.find_file)
        else:
            return super().timerEvent(event)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.killTimer(self.timer_id)
        return super().closeEvent(event)
