# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'taskcomposer.ui'
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
    QSpacerItem, QSplitter, QStatusBar, QTabWidget,
    QToolButton, QVBoxLayout, QWidget)

from cchelper.chartviewer.chartviewer import ChartViewer
from cchelper.fileeditor.codeeditor import CodeEditor
from cchelper.fileviewer.fileviewer import FileViewer
from cchelper.gviewer.gviewer import GViewer
from cchelper.verdictbrowser.verdictbrowser import VerdictBrowser

class Ui_TaskComposer(object):
    def setupUi(self, TaskComposer):
        if not TaskComposer.objectName():
            TaskComposer.setObjectName(u"TaskComposer")
        TaskComposer.resize(633, 587)
        TaskComposer.setWindowTitle(u"cchelper")
        self.centralwidget = QWidget(TaskComposer)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.TCButton = QToolButton(self.centralwidget)
        self.TCButton.setObjectName(u"TCButton")

        self.horizontalLayout_2.addWidget(self.TCButton)

        self.buildButton = QToolButton(self.centralwidget)
        self.buildButton.setObjectName(u"buildButton")
        self.buildButton.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.horizontalLayout_2.addWidget(self.buildButton)

        self.runButton = QToolButton(self.centralwidget)
        self.runButton.setObjectName(u"runButton")
        self.runButton.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.horizontalLayout_2.addWidget(self.runButton)

        self.stopButton = QToolButton(self.centralwidget)
        self.stopButton.setObjectName(u"stopButton")

        self.horizontalLayout_2.addWidget(self.stopButton)

        self.submitButton = QToolButton(self.centralwidget)
        self.submitButton.setObjectName(u"submitButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.submitButton.sizePolicy().hasHeightForWidth())
        self.submitButton.setSizePolicy(sizePolicy)
        self.submitButton.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.horizontalLayout_2.addWidget(self.submitButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.tabWidget = QTabWidget(self.splitter)
        self.tabWidget.setObjectName(u"tabWidget")
        self.SEditor = CodeEditor()
        self.SEditor.setObjectName(u"SEditor")
        self.tabWidget.addTab(self.SEditor, "")
        self.GEditor = CodeEditor()
        self.GEditor.setObjectName(u"GEditor")
        self.tabWidget.addTab(self.GEditor, "")
        self.JEditor = CodeEditor()
        self.JEditor.setObjectName(u"JEditor")
        self.tabWidget.addTab(self.JEditor, "")
        self.splitter.addWidget(self.tabWidget)
        self.tabWidget_2 = QTabWidget(self.splitter)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.CViewer = ChartViewer()
        self.CViewer.setObjectName(u"CViewer")
        self.tabWidget_2.addTab(self.CViewer, "")
        self.VBrowser = VerdictBrowser()
        self.VBrowser.setObjectName(u"VBrowser")
        self.tabWidget_2.addTab(self.VBrowser, "")
        self.FViewer = FileViewer()
        self.FViewer.setObjectName(u"FViewer")
        self.tabWidget_2.addTab(self.FViewer, "")
        self.GViewer = GViewer()
        self.GViewer.setObjectName(u"GViewer")
        self.tabWidget_2.addTab(self.GViewer, "")
        self.splitter.addWidget(self.tabWidget_2)

        self.verticalLayout.addWidget(self.splitter)

        TaskComposer.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(TaskComposer)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setSizeGripEnabled(False)
        TaskComposer.setStatusBar(self.statusbar)

        self.retranslateUi(TaskComposer)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(TaskComposer)
    # setupUi

    def retranslateUi(self, TaskComposer):
        self.TCButton.setText(QCoreApplication.translate("TaskComposer", u"Test Cases", None))
        self.buildButton.setText(QCoreApplication.translate("TaskComposer", u"4", None))
        self.runButton.setText(QCoreApplication.translate("TaskComposer", u"5", None))
        self.stopButton.setText(QCoreApplication.translate("TaskComposer", u"T", None))
        self.submitButton.setText(QCoreApplication.translate("TaskComposer", u"6", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.SEditor), QCoreApplication.translate("TaskComposer", u"Solver", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.GEditor), QCoreApplication.translate("TaskComposer", u"Generator", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.JEditor), QCoreApplication.translate("TaskComposer", u"Jurger", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.CViewer), QCoreApplication.translate("TaskComposer", u"CViewer", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.VBrowser), QCoreApplication.translate("TaskComposer", u"Verdict Table", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.FViewer), QCoreApplication.translate("TaskComposer", u"FViewer", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.GViewer), QCoreApplication.translate("TaskComposer", u"GViewer", None))
        pass
    # retranslateUi

