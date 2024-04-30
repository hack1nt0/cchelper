# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'taskcomposerm.ui'
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
    QSpacerItem, QStackedWidget, QStatusBar, QTabWidget,
    QToolButton, QVBoxLayout, QWidget)

from cchelper.filebrowser import FileBrowser
from cchelper.taskbrowser import TaskBrowser
from cchelper.terminal.qterminal.widget import TerminalWidget
from cchelper.testbrowser import TestBrowser
from cchelper.verdictbrowser.verdictbrowser import VerdictBrowser

class Ui_TaskComposerM(object):
    def setupUi(self, TaskComposerM):
        if not TaskComposerM.objectName():
            TaskComposerM.setObjectName(u"TaskComposerM")
        TaskComposerM.resize(694, 661)
        self.centralwidget = QWidget(TaskComposerM)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(12, 12, 12, 12)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.helpButton = QToolButton(self.centralwidget)
        self.helpButton.setObjectName(u"helpButton")

        self.horizontalLayout_2.addWidget(self.helpButton)

        self.settingButton = QToolButton(self.centralwidget)
        self.settingButton.setObjectName(u"settingButton")

        self.horizontalLayout_2.addWidget(self.settingButton)

        self.solveButton = QToolButton(self.centralwidget)
        self.solveButton.setObjectName(u"solveButton")
        font = QFont()
        font.setFamilies([u".AppleSystemUIFont"])
        self.solveButton.setFont(font)

        self.horizontalLayout_2.addWidget(self.solveButton)

        self.buildButton = QToolButton(self.centralwidget)
        self.buildButton.setObjectName(u"buildButton")
        self.buildButton.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.horizontalLayout_2.addWidget(self.buildButton)

        self.stopButton = QToolButton(self.centralwidget)
        self.stopButton.setObjectName(u"stopButton")

        self.horizontalLayout_2.addWidget(self.stopButton)

        self.runButton = QToolButton(self.centralwidget)
        self.runButton.setObjectName(u"runButton")
        self.runButton.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.horizontalLayout_2.addWidget(self.runButton)

        self.submitButton = QToolButton(self.centralwidget)
        self.submitButton.setObjectName(u"submitButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.submitButton.sizePolicy().hasHeightForWidth())
        self.submitButton.setSizePolicy(sizePolicy)
        self.submitButton.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.horizontalLayout_2.addWidget(self.submitButton)

        self.graphButton = QToolButton(self.centralwidget)
        self.graphButton.setObjectName(u"graphButton")

        self.horizontalLayout_2.addWidget(self.graphButton)

        self.terminalButton = QToolButton(self.centralwidget)
        self.terminalButton.setObjectName(u"terminalButton")

        self.horizontalLayout_2.addWidget(self.terminalButton)

        self.dbButton = QToolButton(self.centralwidget)
        self.dbButton.setObjectName(u"dbButton")

        self.horizontalLayout_2.addWidget(self.dbButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout = QVBoxLayout(self.page)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.page)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setMovable(True)
        self.taskBrowser = TaskBrowser()
        self.taskBrowser.setObjectName(u"taskBrowser")
        self.tabWidget.addTab(self.taskBrowser, "")
        self.testBrowser = TestBrowser()
        self.testBrowser.setObjectName(u"testBrowser")
        self.tabWidget.addTab(self.testBrowser, "")
        self.fileBrowser = FileBrowser()
        self.fileBrowser.setObjectName(u"fileBrowser")
        self.tabWidget.addTab(self.fileBrowser, "")
        self.verdictBrowser = VerdictBrowser()
        self.verdictBrowser.setObjectName(u"verdictBrowser")
        self.tabWidget.addTab(self.verdictBrowser, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.stackedWidget.addWidget(self.page)
        self.terminal = TerminalWidget()
        self.terminal.setObjectName(u"terminal")
        self.stackedWidget.addWidget(self.terminal)

        self.verticalLayout_2.addWidget(self.stackedWidget)

        TaskComposerM.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(TaskComposerM)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setSizeGripEnabled(False)
        TaskComposerM.setStatusBar(self.statusbar)

        self.retranslateUi(TaskComposerM)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(TaskComposerM)
    # setupUi

    def retranslateUi(self, TaskComposerM):
        TaskComposerM.setWindowTitle(QCoreApplication.translate("TaskComposerM", u"cchelper", None))
        self.helpButton.setText(QCoreApplication.translate("TaskComposerM", u"H", None))
        self.settingButton.setText(QCoreApplication.translate("TaskComposerM", u"S", None))
        self.solveButton.setText(QCoreApplication.translate("TaskComposerM", u"S", None))
        self.buildButton.setText(QCoreApplication.translate("TaskComposerM", u"4", None))
        self.stopButton.setText(QCoreApplication.translate("TaskComposerM", u"T", None))
        self.runButton.setText(QCoreApplication.translate("TaskComposerM", u"5", None))
        self.submitButton.setText(QCoreApplication.translate("TaskComposerM", u"6", None))
        self.graphButton.setText(QCoreApplication.translate("TaskComposerM", u"G", None))
        self.terminalButton.setText(QCoreApplication.translate("TaskComposerM", u"T", None))
        self.dbButton.setText(QCoreApplication.translate("TaskComposerM", u"D", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.taskBrowser), QCoreApplication.translate("TaskComposerM", u"Task Browser", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.testBrowser), QCoreApplication.translate("TaskComposerM", u"Test Cases", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.fileBrowser), QCoreApplication.translate("TaskComposerM", u"File Browser", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.verdictBrowser), QCoreApplication.translate("TaskComposerM", u"Verdict Table", None))
    # retranslateUi

