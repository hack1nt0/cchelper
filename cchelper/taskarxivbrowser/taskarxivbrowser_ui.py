# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'taskarxivbrowser.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QLabel, QSizePolicy, QSpacerItem, QSpinBox,
    QTableView, QToolButton, QVBoxLayout, QWidget)

class Ui_TaskArxivBrowser(object):
    def setupUi(self, TaskArxivBrowser):
        if not TaskArxivBrowser.objectName():
            TaskArxivBrowser.setObjectName(u"TaskArxivBrowser")
        TaskArxivBrowser.resize(465, 373)
        TaskArxivBrowser.setWindowTitle(u"TaskArxivBrowser")
        self.verticalLayout = QVBoxLayout(TaskArxivBrowser)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.view = QTableView(TaskArxivBrowser)
        self.view.setObjectName(u"view")
        self.view.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)
        self.view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.view.setSortingEnabled(True)
        self.view.horizontalHeader().setProperty("showSortIndicator", False)

        self.verticalLayout.addWidget(self.view)

        self.label = QLabel(TaskArxivBrowser)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.stashButton = QToolButton(TaskArxivBrowser)
        self.stashButton.setObjectName(u"stashButton")
        self.stashButton.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout.addWidget(self.stashButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pageSzBox = QSpinBox(TaskArxivBrowser)
        self.pageSzBox.setObjectName(u"pageSzBox")

        self.horizontalLayout.addWidget(self.pageSzBox)

        self.toolButton_3 = QToolButton(TaskArxivBrowser)
        self.toolButton_3.setObjectName(u"toolButton_3")

        self.horizontalLayout.addWidget(self.toolButton_3)

        self.pageNoBox = QSpinBox(TaskArxivBrowser)
        self.pageNoBox.setObjectName(u"pageNoBox")

        self.horizontalLayout.addWidget(self.pageNoBox)

        self.toolButton_2 = QToolButton(TaskArxivBrowser)
        self.toolButton_2.setObjectName(u"toolButton_2")

        self.horizontalLayout.addWidget(self.toolButton_2)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(TaskArxivBrowser)

        QMetaObject.connectSlotsByName(TaskArxivBrowser)
    # setupUi

    def retranslateUi(self, TaskArxivBrowser):
        self.label.setText(QCoreApplication.translate("TaskArxivBrowser", u"** Double click to drill in **Solver**.", None))
        self.stashButton.setText(QCoreApplication.translate("TaskArxivBrowser", u"Stash", None))
        self.toolButton_3.setText(QCoreApplication.translate("TaskArxivBrowser", u"<", None))
        self.toolButton_2.setText(QCoreApplication.translate("TaskArxivBrowser", u">", None))
        pass
    # retranslateUi

