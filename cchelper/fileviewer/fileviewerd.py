from cchelper import *
from .fileviewerdialog_ui import Ui_FileViewerDialog


class FileViewerD(QDialog, Ui_FileViewerDialog):
    def __init__(
        self,
        parent: QWidget = None,
    ) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        # self.setWindowFlags(Qt.WindowType.Tool)

    def set_file(self, file: File):
        file = file if isinstance(file, File) else File(file)
        self.widget.set_file(file)
        path = file.path
        self.setWindowTitle(f"View [{os.path.basename(path)}]")
        self.setToolTip(path)

    def show(self) -> None:
        super().show()
        self.raise_()
        self.activateWindow()
    
        