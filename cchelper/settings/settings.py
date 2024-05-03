from cchelper import *
from .settings_ui import Ui_Settings


class Settings(QDialog, Ui_Settings):
    project_changed_signal: Signal = Signal()
    font_changed_signal: Signal = Signal()
    ssh_changed_signal: Signal = Signal()

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        # self.buttonBox.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self.apply)

    def done(self, arg__1: int) -> None:
        project = conf.project_dir
        font = conf.font
        if arg__1:
            self.confform.mapper.submit()
        if not conf.project_dir:
            logger.error('Please select Project dir!')
            return
        if not conf.font:
            logger.error('Please choose font!')
            return
        if conf.darktheme:
            windows['app'].setStyleSheet(open(paths.data("dark.css")).read())
        else:
            windows['app'].setStyleSheet(open(paths.data("cchelper.css")).read())
        if project != conf.project_dir:
            self.project_changed_signal.emit()
        if font != conf.font:
            self.font_changed_signal.emit()
        conf.save()
        os.makedirs(os.path.join(conf.project_dir, 'tasks'), exist_ok=True)
        return super().done(arg__1)