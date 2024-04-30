# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'fileviewerdialog.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QSizePolicy, QVBoxLayout,
    QWidget)

from cchelper.fileviewer import FileViewer

class Ui_FileViewerDialog(object):
    def setupUi(self, FileViewerDialog):
        if not FileViewerDialog.objectName():
            FileViewerDialog.setObjectName(u"FileViewerDialog")
        FileViewerDialog.resize(568, 483)
        self.verticalLayout = QVBoxLayout(FileViewerDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = FileViewer(FileViewerDialog)
        self.widget.setObjectName(u"widget")

        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(FileViewerDialog)

        QMetaObject.connectSlotsByName(FileViewerDialog)
    # setupUi

    def retranslateUi(self, FileViewerDialog):
        FileViewerDialog.setWindowTitle(QCoreApplication.translate("FileViewerDialog", u"View File", None))
    # retranslateUi

