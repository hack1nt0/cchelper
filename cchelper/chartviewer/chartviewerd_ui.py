# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'chartviewerd.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QSizePolicy, QVBoxLayout, QWidget)

from cchelper.chartviewer.chartviewer import ChartViewer

class Ui_ChartViewerD(object):
    def setupUi(self, ChartViewerD):
        if not ChartViewerD.objectName():
            ChartViewerD.setObjectName(u"ChartViewerD")
        ChartViewerD.resize(400, 300)
        self.verticalLayout = QVBoxLayout(ChartViewerD)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = ChartViewer(ChartViewerD)
        self.widget.setObjectName(u"widget")

        self.verticalLayout.addWidget(self.widget)

        self.buttonBox = QDialogButtonBox(ChartViewerD)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok|QDialogButtonBox.Reset)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(ChartViewerD)
        self.buttonBox.accepted.connect(ChartViewerD.accept)
        self.buttonBox.rejected.connect(ChartViewerD.reject)

        QMetaObject.connectSlotsByName(ChartViewerD)
    # setupUi

    def retranslateUi(self, ChartViewerD):
        ChartViewerD.setWindowTitle(QCoreApplication.translate("ChartViewerD", u"Chart", None))
    # retranslateUi

