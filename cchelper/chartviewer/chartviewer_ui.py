# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'chartviewer.ui'
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

from cchelper.chartviewer.chartview import ChartView

class Ui_ChartViewer(object):
    def setupUi(self, ChartViewer):
        if not ChartViewer.objectName():
            ChartViewer.setObjectName(u"ChartViewer")
        ChartViewer.resize(400, 300)
        ChartViewer.setWindowTitle(u"CViewer")
        self.verticalLayout = QVBoxLayout(ChartViewer)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.view = ChartView(ChartViewer)
        self.view.setObjectName(u"view")

        self.verticalLayout.addWidget(self.view)


        self.retranslateUi(ChartViewer)

        QMetaObject.connectSlotsByName(ChartViewer)
    # setupUi

    def retranslateUi(self, ChartViewer):
        pass
    # retranslateUi

