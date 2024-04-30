# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'filebrowser.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QListView, QSizePolicy,
    QSpacerItem, QToolButton, QVBoxLayout, QWidget)

class Ui_TaskBrowser(object):
    def setupUi(self, TaskBrowser):
        if not TaskBrowser.objectName():
            TaskBrowser.setObjectName(u"TaskBrowser")
        TaskBrowser.resize(501, 500)
        self.verticalLayout = QVBoxLayout(TaskBrowser)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.findButton = QToolButton(TaskBrowser)
        self.findButton.setObjectName(u"findButton")

        self.horizontalLayout_2.addWidget(self.findButton)

        self.newButton = QToolButton(TaskBrowser)
        self.newButton.setObjectName(u"newButton")

        self.horizontalLayout_2.addWidget(self.newButton)

        self.delButton = QToolButton(TaskBrowser)
        self.delButton.setObjectName(u"delButton")

        self.horizontalLayout_2.addWidget(self.delButton)

        self.editButton = QToolButton(TaskBrowser)
        self.editButton.setObjectName(u"editButton")

        self.horizontalLayout_2.addWidget(self.editButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.view = QListView(TaskBrowser)
        self.view.setObjectName(u"view")
        self.view.setAlternatingRowColors(True)
        self.view.setProperty("isWrapping", True)
        self.view.setWordWrap(True)

        self.verticalLayout.addWidget(self.view)


        self.retranslateUi(TaskBrowser)

        QMetaObject.connectSlotsByName(TaskBrowser)
    # setupUi

    def retranslateUi(self, TaskBrowser):
        TaskBrowser.setWindowTitle(QCoreApplication.translate("TaskBrowser", u"Form", None))
        self.findButton.setText(QCoreApplication.translate("TaskBrowser", u"F", None))
        self.newButton.setText(QCoreApplication.translate("TaskBrowser", u"N", None))
        self.delButton.setText(QCoreApplication.translate("TaskBrowser", u"D", None))
        self.editButton.setText(QCoreApplication.translate("TaskBrowser", u"E", None))
    # retranslateUi

