# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'langbrowser.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QListView,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_LangBrowser(object):
    def setupUi(self, LangBrowser):
        if not LangBrowser.objectName():
            LangBrowser.setObjectName(u"LangBrowser")
        LangBrowser.resize(279, 333)
        LangBrowser.setWindowTitle(u"Languages")
        self.verticalLayout = QVBoxLayout(LangBrowser)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.view = QListView(LangBrowser)
        self.view.setObjectName(u"view")

        self.verticalLayout.addWidget(self.view)

        self.label = QLabel(LangBrowser)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)


        self.retranslateUi(LangBrowser)

        QMetaObject.connectSlotsByName(LangBrowser)
    # setupUi

    def retranslateUi(self, LangBrowser):
        self.label.setText(QCoreApplication.translate("LangBrowser", u"** Suffixes of langs should be unique.", None))
        pass
    # retranslateUi

