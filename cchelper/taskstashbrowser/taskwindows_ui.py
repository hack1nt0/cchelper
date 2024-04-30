# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'taskwindows.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QListView, QMainWindow,
    QSizePolicy, QSpacerItem, QStatusBar, QToolButton,
    QVBoxLayout, QWidget)

class Ui_TaskWindow(object):
    def setupUi(self, TaskWindow):
        if not TaskWindow.objectName():
            TaskWindow.setObjectName(u"TaskWindow")
        TaskWindow.resize(314, 427)
        TaskWindow.setWindowTitle(u"cchelper")
        self.centralwidget = QWidget(TaskWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

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

        self.logButton = QToolButton(self.centralwidget)
        self.logButton.setObjectName(u"logButton")

        self.horizontalLayout_2.addWidget(self.logButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.view = QListView(self.centralwidget)
        self.view.setObjectName(u"view")
        self.view.setAlternatingRowColors(True)
        self.view.setProperty("isWrapping", True)
        self.view.setWordWrap(True)

        self.verticalLayout.addWidget(self.view)

        TaskWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(TaskWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setSizeGripEnabled(False)
        TaskWindow.setStatusBar(self.statusbar)

        self.retranslateUi(TaskWindow)

        QMetaObject.connectSlotsByName(TaskWindow)
    # setupUi

    def retranslateUi(self, TaskWindow):
        self.F1Button.setText(QCoreApplication.translate("TaskWindow", u"?", None))
        self.settingButton.setText(QCoreApplication.translate("TaskWindow", u"S", None))
        self.findButton.setText(QCoreApplication.translate("TaskWindow", u"F", None))
        self.newButton.setText(QCoreApplication.translate("TaskWindow", u"N", None))
        self.delButton.setText(QCoreApplication.translate("TaskWindow", u"D", None))
        self.logButton.setText(QCoreApplication.translate("TaskWindow", u"Log", None))
        pass
    # retranslateUi

