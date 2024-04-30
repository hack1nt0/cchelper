# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'filesubmit.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QSizePolicy,
    QSpacerItem, QToolButton, QVBoxLayout, QWidget)

from cchelper.fileviewer import FileViewerWidget

class Ui_FileSubmitter(object):
    def setupUi(self, FileSubmitter):
        if not FileSubmitter.objectName():
            FileSubmitter.setObjectName(u"FileSubmitter")
        FileSubmitter.resize(400, 300)
        FileSubmitter.setWindowTitle(u"Submit FIle")
        self.horizontalLayout = QHBoxLayout(FileSubmitter)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.iV = FileViewerWidget(FileSubmitter)
        self.iV.setObjectName(u"iV")

        self.horizontalLayout.addWidget(self.iV)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.toolButton = QToolButton(FileSubmitter)
        self.toolButton.setObjectName(u"toolButton")

        self.verticalLayout.addWidget(self.toolButton)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.oV = FileViewerWidget(FileSubmitter)
        self.oV.setObjectName(u"oV")

        self.horizontalLayout.addWidget(self.oV)


        self.retranslateUi(FileSubmitter)

        QMetaObject.connectSlotsByName(FileSubmitter)
    # setupUi

    def retranslateUi(self, FileSubmitter):
        self.toolButton.setText(QCoreApplication.translate("FileSubmitter", u">>>>", None))
        pass
    # retranslateUi

