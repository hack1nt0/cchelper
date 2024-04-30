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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QSizePolicy, QSpacerItem,
    QTableView, QToolButton, QTreeView, QVBoxLayout,
    QWidget)

class Ui_FileBrowser(object):
    def setupUi(self, FileBrowser):
        if not FileBrowser.objectName():
            FileBrowser.setObjectName(u"FileBrowser")
        FileBrowser.resize(618, 452)
        self.verticalLayout_3 = QVBoxLayout(FileBrowser)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.lineEdit = QLineEdit(FileBrowser)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout_3.addWidget(self.lineEdit)

        self.foundW = QFrame(FileBrowser)
        self.foundW.setObjectName(u"foundW")
        self.verticalLayout = QVBoxLayout(self.foundW)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tableView = QTableView(self.foundW)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout.addWidget(self.tableView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.foundW)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_3.addWidget(self.foundW)

        self.fsW = QFrame(FileBrowser)
        self.fsW.setObjectName(u"fsW")
        self.verticalLayout_2 = QVBoxLayout(self.fsW)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.view = QTreeView(self.fsW)
        self.view.setObjectName(u"view")

        self.verticalLayout_2.addWidget(self.view)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.newButton = QToolButton(self.fsW)
        self.newButton.setObjectName(u"newButton")

        self.horizontalLayout_2.addWidget(self.newButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout_3.addWidget(self.fsW)


        self.retranslateUi(FileBrowser)

        QMetaObject.connectSlotsByName(FileBrowser)
    # setupUi

    def retranslateUi(self, FileBrowser):
        FileBrowser.setWindowTitle(QCoreApplication.translate("FileBrowser", u"Form", None))
        self.label.setText(QCoreApplication.translate("FileBrowser", u"Found 0 files.", None))
        self.newButton.setText(QCoreApplication.translate("FileBrowser", u"New File", None))
    # retranslateUi

