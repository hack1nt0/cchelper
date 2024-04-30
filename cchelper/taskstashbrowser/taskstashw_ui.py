# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'taskstashw.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QMainWindow,
    QSizePolicy, QSpacerItem, QStackedWidget, QStatusBar,
    QToolButton, QVBoxLayout, QWidget)

from cchelper.fileeditor.codeeditor import CodeEditor

class Ui_TaskStashW(object):
    def setupUi(self, TaskStashW):
        if not TaskStashW.objectName():
            TaskStashW.setObjectName(u"TaskStashW")
        TaskStashW.resize(633, 587)
        TaskStashW.setWindowTitle(u"cchelper")
        self.centralwidget = QWidget(TaskStashW)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.F1Button = QToolButton(self.centralwidget)
        self.F1Button.setObjectName(u"F1Button")

        self.horizontalLayout_2.addWidget(self.F1Button)

        self.settingButton = QToolButton(self.centralwidget)
        self.settingButton.setObjectName(u"settingButton")

        self.horizontalLayout_2.addWidget(self.settingButton)

        self.findButton = QToolButton(self.centralwidget)
        self.findButton.setObjectName(u"findButton")

        self.horizontalLayout_2.addWidget(self.findButton)

        self.newButton = QToolButton(self.centralwidget)
        self.newButton.setObjectName(u"newButton")

        self.horizontalLayout_2.addWidget(self.newButton)

        self.delButton = QToolButton(self.centralwidget)
        self.delButton.setObjectName(u"delButton")

        self.horizontalLayout_2.addWidget(self.delButton)

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_2.addWidget(self.comboBox)

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

        self.arxivButton = QToolButton(self.centralwidget)
        self.arxivButton.setObjectName(u"arxivButton")
        sizePolicy.setHeightForWidth(self.arxivButton.sizePolicy().hasHeightForWidth())
        self.arxivButton.setSizePolicy(sizePolicy)
        self.arxivButton.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.horizontalLayout_2.addWidget(self.arxivButton)

        self.logButton = QToolButton(self.centralwidget)
        self.logButton.setObjectName(u"logButton")

        self.horizontalLayout_2.addWidget(self.logButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.TCButton = QToolButton(self.centralwidget)
        self.TCButton.setObjectName(u"TCButton")

        self.horizontalLayout.addWidget(self.TCButton)

        self.VButton = QToolButton(self.centralwidget)
        self.VButton.setObjectName(u"VButton")

        self.horizontalLayout.addWidget(self.VButton)

        self.SButton = QToolButton(self.centralwidget)
        self.SButton.setObjectName(u"SButton")
        self.SButton.setCheckable(True)
        self.SButton.setChecked(True)
        self.SButton.setAutoExclusive(True)

        self.horizontalLayout.addWidget(self.SButton)

        self.GButton = QToolButton(self.centralwidget)
        self.GButton.setObjectName(u"GButton")
        self.GButton.setCheckable(True)
        self.GButton.setAutoExclusive(True)

        self.horizontalLayout.addWidget(self.GButton)

        self.JButton = QToolButton(self.centralwidget)
        self.JButton.setObjectName(u"JButton")
        self.JButton.setCheckable(True)
        self.JButton.setAutoExclusive(True)

        self.horizontalLayout.addWidget(self.JButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.SEditor = CodeEditor()
        self.SEditor.setObjectName(u"SEditor")
        self.stackedWidget.addWidget(self.SEditor)
        self.GEditor = CodeEditor()
        self.GEditor.setObjectName(u"GEditor")
        self.stackedWidget.addWidget(self.GEditor)
        self.JEditor = CodeEditor()
        self.JEditor.setObjectName(u"JEditor")
        self.stackedWidget.addWidget(self.JEditor)

        self.verticalLayout.addWidget(self.stackedWidget)

        TaskStashW.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(TaskStashW)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setSizeGripEnabled(False)
        TaskStashW.setStatusBar(self.statusbar)

        self.retranslateUi(TaskStashW)

        QMetaObject.connectSlotsByName(TaskStashW)
    # setupUi

    def retranslateUi(self, TaskStashW):
        self.F1Button.setText(QCoreApplication.translate("TaskStashW", u"?", None))
        self.settingButton.setText(QCoreApplication.translate("TaskStashW", u"S", None))
        self.findButton.setText(QCoreApplication.translate("TaskStashW", u"F", None))
        self.newButton.setText(QCoreApplication.translate("TaskStashW", u"N", None))
        self.delButton.setText(QCoreApplication.translate("TaskStashW", u"D", None))
        self.buildButton.setText(QCoreApplication.translate("TaskStashW", u"4", None))
        self.runButton.setText(QCoreApplication.translate("TaskStashW", u"5", None))
        self.stopButton.setText(QCoreApplication.translate("TaskStashW", u"T", None))
        self.submitButton.setText(QCoreApplication.translate("TaskStashW", u"6", None))
        self.arxivButton.setText(QCoreApplication.translate("TaskStashW", u"7", None))
        self.logButton.setText(QCoreApplication.translate("TaskStashW", u"Log", None))
        self.TCButton.setText(QCoreApplication.translate("TaskStashW", u"Test Cases", None))
        self.VButton.setText(QCoreApplication.translate("TaskStashW", u"Verdicts", None))
        self.SButton.setText(QCoreApplication.translate("TaskStashW", u"Solver", None))
        self.GButton.setText(QCoreApplication.translate("TaskStashW", u"Generator", None))
        self.JButton.setText(QCoreApplication.translate("TaskStashW", u"Jurger", None))
        pass
    # retranslateUi

