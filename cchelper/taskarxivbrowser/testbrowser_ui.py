# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'testbrowser.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHeaderView, QLabel,
    QSizePolicy, QTableView, QVBoxLayout, QWidget)

class Ui_TestArxivBrowser(object):
    def setupUi(self, TestArxivBrowser):
        if not TestArxivBrowser.objectName():
            TestArxivBrowser.setObjectName(u"TestArxivBrowser")
        TestArxivBrowser.resize(400, 300)
        self.verticalLayout = QVBoxLayout(TestArxivBrowser)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(TestArxivBrowser)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.view = QTableView(TestArxivBrowser)
        self.view.setObjectName(u"view")

        self.verticalLayout.addWidget(self.view)


        self.retranslateUi(TestArxivBrowser)

        QMetaObject.connectSlotsByName(TestArxivBrowser)
    # setupUi

    def retranslateUi(self, TestArxivBrowser):
        TestArxivBrowser.setWindowTitle(QCoreApplication.translate("TestArxivBrowser", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("TestArxivBrowser", u"Arxiv - tests", None))
    # retranslateUi

