# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'terminal.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QSpacerItem,
    QToolButton, QVBoxLayout, QWidget)

from cchelper.terminal.qterminal.widget import TerminalWidget

class Ui_Terminal(object):
    def setupUi(self, Terminal):
        if not Terminal.objectName():
            Terminal.setObjectName(u"Terminal")
        Terminal.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Terminal)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = TerminalWidget(Terminal)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u".AppleSystemUIFont"])
        self.widget.setFont(font)
        self.widget.setFocusPolicy(Qt.StrongFocus)

        self.verticalLayout.addWidget(self.widget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.viewButton = QToolButton(Terminal)
        self.viewButton.setObjectName(u"viewButton")
        self.viewButton.setFocusPolicy(Qt.ClickFocus)

        self.horizontalLayout_2.addWidget(self.viewButton)

        self.clearButton = QToolButton(Terminal)
        self.clearButton.setObjectName(u"clearButton")
        self.clearButton.setFocusPolicy(Qt.ClickFocus)

        self.horizontalLayout_2.addWidget(self.clearButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.reconnectButton = QToolButton(Terminal)
        self.reconnectButton.setObjectName(u"reconnectButton")
        self.reconnectButton.setFocusPolicy(Qt.ClickFocus)

        self.horizontalLayout_2.addWidget(self.reconnectButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Terminal)

        QMetaObject.connectSlotsByName(Terminal)
    # setupUi

    def retranslateUi(self, Terminal):
        Terminal.setWindowTitle(QCoreApplication.translate("Terminal", u"Form", None))
        self.viewButton.setText(QCoreApplication.translate("Terminal", u"View", None))
        self.clearButton.setText(QCoreApplication.translate("Terminal", u"Clear", None))
        self.reconnectButton.setText(QCoreApplication.translate("Terminal", u"Reconnect", None))
    # retranslateUi

