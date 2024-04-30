# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'taskcomposerd.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QSizePolicy,
    QSpacerItem, QSplitter, QTabWidget, QToolButton,
    QVBoxLayout, QWidget)

from cchelper.chartviewer.chartviewer import ChartViewer
from cchelper.fileviewer import FileViewer
from cchelper.gviewer.gviewer import GViewer
from cchelper.testbrowser.testeditor import TestEditor
from cchelper.verdictbrowser.verdictbrowser import VerdictBrowser

class Ui_TaskComposerD(object):
    def setupUi(self, TaskComposerD):
        if not TaskComposerD.objectName():
            TaskComposerD.setObjectName(u"TaskComposerD")
        TaskComposerD.resize(717, 679)
        self.verticalLayout = QVBoxLayout(TaskComposerD)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.buildButton = QToolButton(TaskComposerD)
        self.buildButton.setObjectName(u"buildButton")
        self.buildButton.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.horizontalLayout_2.addWidget(self.buildButton)

        self.runButton = QToolButton(TaskComposerD)
        self.runButton.setObjectName(u"runButton")
        self.runButton.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.horizontalLayout_2.addWidget(self.runButton)

        self.stopButton = QToolButton(TaskComposerD)
        self.stopButton.setObjectName(u"stopButton")

        self.horizontalLayout_2.addWidget(self.stopButton)

        self.submitButton = QToolButton(TaskComposerD)
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

        self.splitter = QSplitter(TaskComposerD)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.tabWidget = QTabWidget(self.splitter)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.TEditor = TestEditor()
        self.TEditor.setObjectName(u"TEditor")
        self.tabWidget.addTab(self.TEditor, "")
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


        self.retranslateUi(TaskComposerD)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(TaskComposerD)
    # setupUi

    def retranslateUi(self, TaskComposerD):
        TaskComposerD.setWindowTitle(QCoreApplication.translate("TaskComposerD", u"Dialog", None))
        self.buildButton.setText(QCoreApplication.translate("TaskComposerD", u"4", None))
        self.runButton.setText(QCoreApplication.translate("TaskComposerD", u"5", None))
        self.stopButton.setText(QCoreApplication.translate("TaskComposerD", u"T", None))
        self.submitButton.setText(QCoreApplication.translate("TaskComposerD", u"6", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TEditor), QCoreApplication.translate("TaskComposerD", u"Test Cases", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.CViewer), QCoreApplication.translate("TaskComposerD", u"CViewer", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.VBrowser), QCoreApplication.translate("TaskComposerD", u"Verdict Table", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.FViewer), QCoreApplication.translate("TaskComposerD", u"FViewer", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.GViewer), QCoreApplication.translate("TaskComposerD", u"GViewer", None))
    # retranslateUi

