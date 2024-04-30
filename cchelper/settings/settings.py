from cchelper import *
from .settings_ui import Ui_Settings


class Settings(QDialog, Ui_Settings):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

    def done(self, arg__1: int) -> None:
        if arg__1:
            self.confform.mapper.submit()
            conf.save()
        return super().done(arg__1)