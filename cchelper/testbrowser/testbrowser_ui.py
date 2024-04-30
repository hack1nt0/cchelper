# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'testbrowser.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QSizePolicy,
    QSpacerItem, QSpinBox, QTableView, QToolButton,
    QVBoxLayout, QWidget)

class Ui_TestBrowser(object):
    def setupUi(self, TestBrowser):
        if not TestBrowser.objectName():
            TestBrowser.setObjectName(u"TestBrowser")
        TestBrowser.resize(552, 454)
        TestBrowser.setWindowTitle(u"Test Browser")
        self.verticalLayout = QVBoxLayout(TestBrowser)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.spinBox = QSpinBox(TestBrowser)
        self.spinBox.setObjectName(u"spinBox")

        self.horizontalLayout.addWidget(self.spinBox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.view = QTableView(TestBrowser)
        self.view.setObjectName(u"view")

        self.verticalLayout.addWidget(self.view)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.newButton = QToolButton(TestBrowser)
        self.newButton.setObjectName(u"newButton")

        self.horizontalLayout_2.addWidget(self.newButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(TestBrowser)

        QMetaObject.connectSlotsByName(TestBrowser)
    # setupUi

    def retranslateUi(self, TestBrowser):
        self.newButton.setText(QCoreApplication.translate("TestBrowser", u"N", None))
        pass
    # retranslateUi

