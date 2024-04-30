from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from cchelper import *
from .langform_ui import Ui_LangForm


class LangForm(QDialog, Ui_LangForm):
    def __init__(self, model, idx, parent: QWidget) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        font = QFont(*conf.font)
        self.templateTextEdit.setFont(font)
        self.templateTextEdit.setTabStopDistance(QFontMetricsF(font).horizontalAdvance(' ' * 4))

        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.ManualSubmit)
        self.mapper.setModel(model)
        self.mapper.addMapping(self.nameLineEdit, model.cols.index('name'))
        self.mapper.addMapping(self.suffixLineEdit, model.cols.index('suffix'))
        self.mapper.addMapping(self.templateTextEdit, model.cols.index('template'), b'plainText')
        self.mapper.addMapping(self.debugLineEdit, model.cols.index('debug'))
        self.mapper.addMapping(self.releaseLineEdit, model.cols.index('release'))
        self.mapper.addMapping(self.runLineEdit, model.cols.index('run'))
        self.mapper.setCurrentIndex(idx)
        
    def done(self, arg__1: int) -> None:
        if arg__1:
            self.mapper.submit()
        return super().done(arg__1)