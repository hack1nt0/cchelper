# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QSizePolicy, QTabWidget, QVBoxLayout, QWidget)

from cchelper.settings.confform import ConfForm
from cchelper.settings.langbrowser import LangBrowser
from cchelper.settings.logviewer import LogViewer
from cchelper.settings.tagbrowser import TagBrowser

class Ui_Settings(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName(u"Settings")
        Settings.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Settings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(Settings)
        self.tabWidget.setObjectName(u"tabWidget")
        self.confform = ConfForm()
        self.confform.setObjectName(u"confform")
        self.tabWidget.addTab(self.confform, "")
        self.langbrowser = LangBrowser()
        self.langbrowser.setObjectName(u"langbrowser")
        self.tabWidget.addTab(self.langbrowser, "")
        self.tagbrowser = TagBrowser()
        self.tagbrowser.setObjectName(u"tagbrowser")
        self.tabWidget.addTab(self.tagbrowser, "")
        self.logviewer = LogViewer()
        self.logviewer.setObjectName(u"logviewer")
        self.tabWidget.addTab(self.logviewer, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.buttonBox = QDialogButtonBox(Settings)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Settings)
        self.buttonBox.accepted.connect(Settings.accept)
        self.buttonBox.rejected.connect(Settings.reject)

        QMetaObject.connectSlotsByName(Settings)
    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QCoreApplication.translate("Settings", u"Dialog", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.confform), QCoreApplication.translate("Settings", u"General", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.langbrowser), QCoreApplication.translate("Settings", u"Languages", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tagbrowser), QCoreApplication.translate("Settings", u"Tags", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.logviewer), QCoreApplication.translate("Settings", u"Log", None))
    # retranslateUi

