# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'taskbrowser.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QHeaderView,
    QSizePolicy, QSpacerItem, QSpinBox, QTableView,
    QToolButton, QVBoxLayout, QWidget)

class Ui_TaskBrowser(object):
    def setupUi(self, TaskBrowser):
        if not TaskBrowser.objectName():
            TaskBrowser.setObjectName(u"TaskBrowser")
        TaskBrowser.resize(426, 456)
        self.verticalLayout = QVBoxLayout(TaskBrowser)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)

        self.spinBox = QSpinBox(TaskBrowser)
        self.spinBox.setObjectName(u"spinBox")

        self.horizontalLayout.addWidget(self.spinBox)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.view = QTableView(TaskBrowser)
        self.view.setObjectName(u"view")

        self.verticalLayout.addWidget(self.view)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.findButton = QToolButton(TaskBrowser)
        self.findButton.setObjectName(u"findButton")

        self.horizontalLayout_2.addWidget(self.findButton)

        self.stopButton = QToolButton(TaskBrowser)
        self.stopButton.setObjectName(u"stopButton")

        self.horizontalLayout_2.addWidget(self.stopButton)

        self.newButton = QToolButton(TaskBrowser)
        self.newButton.setObjectName(u"newButton")

        self.horizontalLayout_2.addWidget(self.newButton)

        self.crawlButton = QToolButton(TaskBrowser)
        self.crawlButton.setObjectName(u"crawlButton")

        self.horizontalLayout_2.addWidget(self.crawlButton)

        self.checkBox = QCheckBox(TaskBrowser)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout_2.addWidget(self.checkBox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(TaskBrowser)

        QMetaObject.connectSlotsByName(TaskBrowser)
    # setupUi

    def retranslateUi(self, TaskBrowser):
        TaskBrowser.setWindowTitle(QCoreApplication.translate("TaskBrowser", u"Form", None))
        self.spinBox.setSuffix(QCoreApplication.translate("TaskBrowser", u" tasks", None))
        self.findButton.setText(QCoreApplication.translate("TaskBrowser", u"F", None))
        self.stopButton.setText(QCoreApplication.translate("TaskBrowser", u"T", None))
        self.newButton.setText(QCoreApplication.translate("TaskBrowser", u"N", None))
        self.crawlButton.setText(QCoreApplication.translate("TaskBrowser", u"C", None))
        self.checkBox.setText(QCoreApplication.translate("TaskBrowser", u"Competitive Companion", None))
    # retranslateUi

