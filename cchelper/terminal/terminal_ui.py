# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'terminal.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QSizePolicy, QVBoxLayout,
    QWidget)

from cchelper.terminal.frontend import TextEditTerminal

class Ui_Terminal(object):
    def setupUi(self, Terminal):
        if not Terminal.objectName():
            Terminal.setObjectName(u"Terminal")
        Terminal.resize(400, 300)
        Terminal.setWindowTitle(u"Terminal")
        self.verticalLayout = QVBoxLayout(Terminal)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.textEdit = TextEditTerminal(Terminal)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout.addWidget(self.textEdit)


        self.retranslateUi(Terminal)

        QMetaObject.connectSlotsByName(Terminal)
    # setupUi

    def retranslateUi(self, Terminal):
        pass
    # retranslateUi

