# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'verdictbrowser.ui'
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

class Ui_VerdictBrowser(object):
    def setupUi(self, VerdictBrowser):
        if not VerdictBrowser.objectName():
            VerdictBrowser.setObjectName(u"VerdictBrowser")
        VerdictBrowser.resize(621, 384)
        VerdictBrowser.setWindowTitle(u"Vedict Browser")
        self.verticalLayout = QVBoxLayout(VerdictBrowser)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(VerdictBrowser)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.view = QTableView(VerdictBrowser)
        self.view.setObjectName(u"view")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.view.sizePolicy().hasHeightForWidth())
        self.view.setSizePolicy(sizePolicy)
        self.view.setTabKeyNavigation(False)
        self.view.setAlternatingRowColors(True)
        self.view.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.view.horizontalHeader().setHighlightSections(False)
        self.view.verticalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.view)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.addButton = QToolButton(VerdictBrowser)
        self.addButton.setObjectName(u"addButton")

        self.horizontalLayout_4.addWidget(self.addButton)

        self.chartButton = QToolButton(VerdictBrowser)
        self.chartButton.setObjectName(u"chartButton")

        self.horizontalLayout_4.addWidget(self.chartButton)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_7)

        self.tailsSpinBox = QSpinBox(VerdictBrowser)
        self.tailsSpinBox.setObjectName(u"tailsSpinBox")
        self.tailsSpinBox.setSuffix(u" bytes/cell")

        self.horizontalLayout_4.addWidget(self.tailsSpinBox)

        self.prevButton = QToolButton(VerdictBrowser)
        self.prevButton.setObjectName(u"prevButton")

        self.horizontalLayout_4.addWidget(self.prevButton)

        self.pageNoBox = QSpinBox(VerdictBrowser)
        self.pageNoBox.setObjectName(u"pageNoBox")
        self.pageNoBox.setFocusPolicy(Qt.WheelFocus)
        self.pageNoBox.setSuffix(u" verdicts")
        self.pageNoBox.setPrefix(u"")
        self.pageNoBox.setMinimum(1)

        self.horizontalLayout_4.addWidget(self.pageNoBox)

        self.nextButton = QToolButton(VerdictBrowser)
        self.nextButton.setObjectName(u"nextButton")

        self.horizontalLayout_4.addWidget(self.nextButton)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.retranslateUi(VerdictBrowser)

        QMetaObject.connectSlotsByName(VerdictBrowser)
    # setupUi

    def retranslateUi(self, VerdictBrowser):
        self.label.setText(QCoreApplication.translate("VerdictBrowser", u"Verdict done.", None))
        self.addButton.setText(QCoreApplication.translate("VerdictBrowser", u"Add as tests", None))
        self.chartButton.setText(QCoreApplication.translate("VerdictBrowser", u"Chart", None))
        self.prevButton.setText(QCoreApplication.translate("VerdictBrowser", u"<", None))
        self.nextButton.setText(QCoreApplication.translate("VerdictBrowser", u">", None))
        pass
    # retranslateUi

