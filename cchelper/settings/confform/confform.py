from cchelper import *
from .confform_ui import Ui_ConfForm
from .model import ConfModel
from .delegate import ConfDelegate


class ConfForm(QWidget, Ui_ConfForm):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.ManualSubmit)
        self.model = ConfModel(self)
        self.mapper.setModel(self.model)
        self.deleg = ConfDelegate(self)
        self.mapper.setItemDelegate(self.deleg)
        self.mapper.addMapping(self.projectEdit, self.model.cols.index("project_dir"))
        self.mapper.addMapping(self.SLineEdit, self.model.cols.index("solver"))
        self.mapper.addMapping(self.GLineEdit, self.model.cols.index("generator"))
        self.mapper.addMapping(self.JLineEdit, self.model.cols.index("jurger"))
        self.mapper.addMapping(self.editorEdit, self.model.cols.index("editor"))
        self.mapper.addMapping(
            self.bytesPerCellSpinBox, self.model.cols.index("bytes_per_cell")
        )
        self.mapper.addMapping(
            self.rowsPerPageSpinBox, self.model.cols.index("rows_per_page")
        )
        self.mapper.addMapping(
            self.bytesPerPageSpinBox, self.model.cols.index("bytes_per_page")
        )
        self.mapper.addMapping(
            self.bytesPerReadSpinBox, self.model.cols.index("bytes_per_read")
        )
        self.mapper.addMapping(
            self.buildDebugRadioButton, self.model.cols.index("build_debug")
        )
        self.mapper.addMapping(
            self.buildReleaseRadioButton, self.model.cols.index("build_release")
        )
        self.mapper.addMapping(
            self.buildAsNeedCheckBox, self.model.cols.index("build_asneed")
        )
        self.mapper.addMapping(
            self.runinshellCheckBox, self.model.cols.index("run_inshell")
        )
        self.mapper.addMapping(self.parallelSpinBox, self.model.cols.index("parallel"))
        self.mapper.addMapping(
            self.refreshRateSpinBox, self.model.cols.index("refresh_rate")
        )
        self.mapper.addMapping(
            self.exeDumpSpinBox, self.model.cols.index("exe_dump_delay")
        )
        self.mapper.addMapping(
            self.exeWarmSpinBox, self.model.cols.index("exe_warm_delay")
        )
        self.mapper.addMapping(self.fontLineEdit, self.model.cols.index("font"))
        self.fontLineEdit.setReadOnly(T)
        self.fontButton.clicked.connect(self.pick_font)
        self.mapper.addMapping(self.graphvizLineEdit, self.model.cols.index("graphviz"))
        self.mapper.toFirst()

        # self.buttonBox.button(QDialogButtonBox.StandardButton.Reset).clicked.connect(self.mapper.revert)
        # self.buttonBox.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self.apply)

        self.openButton.clicked.connect(self.pick_dir)

    def pick_dir(self):
        d = QFileDialog(self)
        d.setDirectory(QDir.home())  # TODO
        d.setFileMode(QFileDialog.FileMode.Directory)
        d.setWindowModality(Qt.WindowModality.WindowModal)
        if d.exec():
            self.projectEdit.setText(d.selectedFiles()[0])

    def pick_font(self):
        ret, font = QFontDialog.getFont(["JetBrains Mono", "Courier New"], self)
        if ret:
            self.fontLineEdit.setText(
                f"{font.family()},{font.pointSize()}"
            )
