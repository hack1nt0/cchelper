from cchelper import *
from cchelper.fileviewer import FileViewer
from .logviewer_ui import Ui_LogViewer


class LogViewer(QWidget, Ui_LogViewer):
    def __init__(self, parent: QWidget=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.widget.set_file(paths.data('cchelper.log'))
        self.widget.tailButton.setChecked(T)

        self.levelMenu = QMenu(self)
        self.levelOpts = QActionGroup(self)
        self.levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARN': logging.WARN,
            'ERROR': logging.ERROR,
        }
        for k in self.levels.keys():
            act = self.levelOpts.addAction(self.levelMenu.addAction(k))
            act.setCheckable(T)
            if k == 'DEBUG':
                act.setChecked(T)
        self.levelMenu.triggered.connect(lambda act: self.change_level(act.text()))
        self.levelButton.setMenu(self.levelMenu)
        self.levelButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        self.clearButton.clicked.connect(self.clear)

    def clear(self):
        with open(paths.data('cchelper.log'), 'w') as w:
            pass
    
    def change_level(self, v):
        logger.set_level(self.levels[v])

    # def closeEvent(self, event: QCloseEvent) -> None:
    #     self.close()
    #     self.deleteLater()
    #     del windows[self.__class__.__name__]
    #     return super().closeEvent(event)
    