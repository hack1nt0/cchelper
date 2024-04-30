# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'codesubmit.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QSizePolicy, QSpacerItem, QTabWidget, QToolButton,
    QVBoxLayout, QWidget)

from cchelper.fileeditor.fileedit import FileEdit

class Ui_CodeSubmitter(object):
    def setupUi(self, CodeSubmitter):
        if not CodeSubmitter.objectName():
            CodeSubmitter.setObjectName(u"CodeSubmitter")
        CodeSubmitter.resize(471, 416)
        CodeSubmitter.setWindowTitle(u"Submit Code")
        self.verticalLayout = QVBoxLayout(CodeSubmitter)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(CodeSubmitter)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.finalTextEdit = FileEdit(self.tab)
        self.finalTextEdit.setObjectName(u"finalTextEdit")

        self.verticalLayout_2.addWidget(self.finalTextEdit)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.validateButton = QToolButton(self.tab)
        self.validateButton.setObjectName(u"validateButton")

        self.horizontalLayout.addWidget(self.validateButton)

        self.removeMainButton = QToolButton(self.tab)
        self.removeMainButton.setObjectName(u"removeMainButton")

        self.horizontalLayout.addWidget(self.removeMainButton)

        self.copyButton = QToolButton(self.tab)
        self.copyButton.setObjectName(u"copyButton")

        self.horizontalLayout.addWidget(self.copyButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.tabWidget.addTab(self.tab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), u"Final")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.ppTextEdit = FileEdit(self.tab_2)
        self.ppTextEdit.setObjectName(u"ppTextEdit")

        self.verticalLayout_3.addWidget(self.ppTextEdit)

        self.tabWidget.addTab(self.tab_2, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), u"Preprocessed")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_4 = QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.errTextEdit = FileEdit(self.tab_3)
        self.errTextEdit.setObjectName(u"errTextEdit")

        self.verticalLayout_4.addWidget(self.errTextEdit)

        self.tabWidget.addTab(self.tab_3, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.retranslateUi(CodeSubmitter)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(CodeSubmitter)
    # setupUi

    def retranslateUi(self, CodeSubmitter):
        self.validateButton.setText(QCoreApplication.translate("CodeSubmitter", u"Validate", None))
        self.removeMainButton.setText(QCoreApplication.translate("CodeSubmitter", u"Remove main()", None))
        self.copyButton.setText(QCoreApplication.translate("CodeSubmitter", u"Copy to Clipboard", None))
        self.label.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("CodeSubmitter", u"SyntaxErr", None))
        pass
    # retranslateUi

