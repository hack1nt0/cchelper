# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainw.ui'
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
    QSpacerItem, QStatusBar, QTabWidget, QToolButton,
    QVBoxLayout, QWidget)

from cchelper.filebrowser import FileBrowser
from cchelper.taskbrowser import TaskBrowser

class Ui_MainW(object):
    def setupUi(self, MainW):
        if not MainW.objectName():
            MainW.setObjectName(u"MainW")
        MainW.resize(484, 517)
        MainW.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QWidget(MainW)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.TBrowser = TaskBrowser()
        self.TBrowser.setObjectName(u"TBrowser")
        self.tabWidget.addTab(self.TBrowser, "")
        self.FBrowser = FileBrowser()
        self.FBrowser.setObjectName(u"FBrowser")
        self.tabWidget.addTab(self.FBrowser, "")

        self.verticalLayout.addWidget(self.tabWidget)

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

        self.logButton = QToolButton(self.centralwidget)
        self.logButton.setObjectName(u"logButton")

        self.horizontalLayout_2.addWidget(self.logButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        MainW.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainW)
        self.statusbar.setObjectName(u"statusbar")
        MainW.setStatusBar(self.statusbar)

        self.retranslateUi(MainW)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainW)
    # setupUi

    def retranslateUi(self, MainW):
        MainW.setWindowTitle(QCoreApplication.translate("MainW", u"cchelper", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TBrowser), QCoreApplication.translate("MainW", u"Tasks", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.FBrowser), QCoreApplication.translate("MainW", u"Files", None))
        self.F1Button.setText(QCoreApplication.translate("MainW", u"?", None))
        self.settingButton.setText(QCoreApplication.translate("MainW", u"S", None))
        self.logButton.setText(QCoreApplication.translate("MainW", u"Log", None))
    # retranslateUi

