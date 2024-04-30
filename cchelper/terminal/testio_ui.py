# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'testio.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QMainWindow,
    QPlainTextEdit, QSizePolicy, QSpacerItem, QStatusBar,
    QToolButton, QVBoxLayout, QWidget)

class Ui_TestIO(object):
    def setupUi(self, TestIO):
        if not TestIO.objectName():
            TestIO.setObjectName(u"TestIO")
        TestIO.resize(704, 562)
        TestIO.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QWidget(TestIO)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFlat(False)
        self.horizontalLayout = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.input = QPlainTextEdit(self.groupBox_2)
        self.input.setObjectName(u"input")

        self.horizontalLayout.addWidget(self.input)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.runButton = QToolButton(self.groupBox_2)
        self.runButton.setObjectName(u"runButton")

        self.verticalLayout_2.addWidget(self.runButton)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.output = QPlainTextEdit(self.groupBox_2)
        self.output.setObjectName(u"output")

        self.horizontalLayout.addWidget(self.output)


        self.verticalLayout_3.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.display = QPlainTextEdit(self.groupBox)
        self.display.setObjectName(u"display")

        self.verticalLayout.addWidget(self.display)


        self.verticalLayout_3.addWidget(self.groupBox)

        TestIO.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(TestIO)
        self.statusbar.setObjectName(u"statusbar")
        TestIO.setStatusBar(self.statusbar)

        self.retranslateUi(TestIO)

        QMetaObject.connectSlotsByName(TestIO)
    # setupUi

    def retranslateUi(self, TestIO):
        TestIO.setWindowTitle(QCoreApplication.translate("TestIO", u"Test Term/IO", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("TestIO", u"I/O", None))
        self.runButton.setText(QCoreApplication.translate("TestIO", u"Run", None))
        self.groupBox.setTitle(QCoreApplication.translate("TestIO", u"Display", None))
        self.display.setDocumentTitle("")
    # retranslateUi

