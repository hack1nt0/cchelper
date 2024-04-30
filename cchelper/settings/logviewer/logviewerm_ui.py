# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'logviewerm.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QSizePolicy,
    QSpacerItem, QToolButton, QVBoxLayout, QWidget)

from cchelper.fileviewer import FileViewer

class Ui_LogViewer(object):
    def setupUi(self, LogViewer):
        if not LogViewer.objectName():
            LogViewer.setObjectName(u"LogViewer")
        LogViewer.resize(540, 417)
        self.centralwidget = QWidget(LogViewer)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.clearButton = QToolButton(self.centralwidget)
        self.clearButton.setObjectName(u"clearButton")

        self.horizontalLayout.addWidget(self.clearButton)

        self.levelButton = QToolButton(self.centralwidget)
        self.levelButton.setObjectName(u"levelButton")

        self.horizontalLayout.addWidget(self.levelButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.widget = FileViewer(self.centralwidget)
        self.widget.setObjectName(u"widget")

        self.verticalLayout.addWidget(self.widget)

        LogViewer.setCentralWidget(self.centralwidget)

        self.retranslateUi(LogViewer)

        QMetaObject.connectSlotsByName(LogViewer)
    # setupUi

    def retranslateUi(self, LogViewer):
        LogViewer.setWindowTitle(QCoreApplication.translate("LogViewer", u"Log", None))
        self.clearButton.setText(QCoreApplication.translate("LogViewer", u"Clear", None))
        self.levelButton.setText(QCoreApplication.translate("LogViewer", u"Level", None))
    # retranslateUi

