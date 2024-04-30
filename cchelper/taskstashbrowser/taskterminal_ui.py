# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'taskterminal.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLineEdit, QMainWindow,
    QSizePolicy, QSpacerItem, QStackedWidget, QStatusBar,
    QToolButton, QWidget)

class Ui_TaskStashW(object):
    def setupUi(self, TaskStashW):
        if not TaskStashW.objectName():
            TaskStashW.setObjectName(u"TaskStashW")
        TaskStashW.resize(615, 533)
        TaskStashW.setWindowTitle(u"cchelper")
        self.centralwidget = QWidget(TaskStashW)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(12, 12, 442, 24))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.toolButton = QToolButton(self.horizontalLayoutWidget)
        self.toolButton.setObjectName(u"toolButton")

        self.horizontalLayout.addWidget(self.toolButton)

        self.TCButton = QToolButton(self.horizontalLayoutWidget)
        self.TCButton.setObjectName(u"TCButton")

        self.horizontalLayout.addWidget(self.TCButton)

        self.TPButton = QToolButton(self.horizontalLayoutWidget)
        self.TPButton.setObjectName(u"TPButton")

        self.horizontalLayout.addWidget(self.TPButton)

        self.SButton = QToolButton(self.horizontalLayoutWidget)
        self.SButton.setObjectName(u"SButton")

        self.horizontalLayout.addWidget(self.SButton)

        self.VButton = QToolButton(self.horizontalLayoutWidget)
        self.VButton.setObjectName(u"VButton")

        self.horizontalLayout.addWidget(self.VButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(12, 373, 346, 24))
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.F1Button = QToolButton(self.widget)
        self.F1Button.setObjectName(u"F1Button")

        self.horizontalLayout_2.addWidget(self.F1Button)

        self.settingButton = QToolButton(self.widget)
        self.settingButton.setObjectName(u"settingButton")

        self.horizontalLayout_2.addWidget(self.settingButton)

        self.findButton = QToolButton(self.widget)
        self.findButton.setObjectName(u"findButton")

        self.horizontalLayout_2.addWidget(self.findButton)

        self.newButton = QToolButton(self.widget)
        self.newButton.setObjectName(u"newButton")

        self.horizontalLayout_2.addWidget(self.newButton)

        self.delButton = QToolButton(self.widget)
        self.delButton.setObjectName(u"delButton")

        self.horizontalLayout_2.addWidget(self.delButton)

        self.buildButton = QToolButton(self.widget)
        self.buildButton.setObjectName(u"buildButton")
        self.buildButton.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.horizontalLayout_2.addWidget(self.buildButton)

        self.runButton = QToolButton(self.widget)
        self.runButton.setObjectName(u"runButton")
        self.runButton.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.horizontalLayout_2.addWidget(self.runButton)

        self.stopButton = QToolButton(self.widget)
        self.stopButton.setObjectName(u"stopButton")

        self.horizontalLayout_2.addWidget(self.stopButton)

        self.submitButton = QToolButton(self.widget)
        self.submitButton.setObjectName(u"submitButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.submitButton.sizePolicy().hasHeightForWidth())
        self.submitButton.setSizePolicy(sizePolicy)
        self.submitButton.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.horizontalLayout_2.addWidget(self.submitButton)

        self.arxivButton = QToolButton(self.widget)
        self.arxivButton.setObjectName(u"arxivButton")
        sizePolicy.setHeightForWidth(self.arxivButton.sizePolicy().hasHeightForWidth())
        self.arxivButton.setSizePolicy(sizePolicy)
        self.arxivButton.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.horizontalLayout_2.addWidget(self.arxivButton)

        self.logButton = QToolButton(self.widget)
        self.logButton.setObjectName(u"logButton")

        self.horizontalLayout_2.addWidget(self.logButton)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(210, 310, 113, 21))
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(140, 70, 351, 211))
        self.editor = QWidget()
        self.editor.setObjectName(u"editor")
        self.stackedWidget.addWidget(self.editor)
        self.terminal = QWidget()
        self.terminal.setObjectName(u"terminal")
        self.stackedWidget.addWidget(self.terminal)
        TaskStashW.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(TaskStashW)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setSizeGripEnabled(False)
        TaskStashW.setStatusBar(self.statusbar)

        self.retranslateUi(TaskStashW)

        QMetaObject.connectSlotsByName(TaskStashW)
    # setupUi

    def retranslateUi(self, TaskStashW):
        self.toolButton.setText(QCoreApplication.translate("TaskStashW", u"Task List", None))
        self.TCButton.setText(QCoreApplication.translate("TaskStashW", u"Test Cases", None))
        self.TPButton.setText(QCoreApplication.translate("TaskStashW", u"Test Pamameters", None))
        self.SButton.setText(QCoreApplication.translate("TaskStashW", u"Screen List", None))
        self.VButton.setText(QCoreApplication.translate("TaskStashW", u"Verdicts", None))
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
        pass
    # retranslateUi

