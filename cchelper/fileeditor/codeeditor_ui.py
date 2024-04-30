# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'codeeditor.ui'
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
    QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout,
    QWidget)

from cchelper.fileeditor.fileedit import FileEdit

class Ui_CodeEditor(object):
    def setupUi(self, CodeEditor):
        if not CodeEditor.objectName():
            CodeEditor.setObjectName(u"CodeEditor")
        CodeEditor.resize(476, 369)
        self.verticalLayout = QVBoxLayout(CodeEditor)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.textEdit = FileEdit(CodeEditor)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout.addWidget(self.textEdit)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.findButton = QToolButton(CodeEditor)
        self.findButton.setObjectName(u"findButton")

        self.horizontalLayout.addWidget(self.findButton)

        self.saveButton = QToolButton(CodeEditor)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalLayout.addWidget(self.saveButton)

        self.langButton = QToolButton(CodeEditor)
        self.langButton.setObjectName(u"langButton")
        self.langButton.setPopupMode(QToolButton.InstantPopup)

        self.horizontalLayout.addWidget(self.langButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.statLabel = QLabel(CodeEditor)
        self.statLabel.setObjectName(u"statLabel")

        self.horizontalLayout.addWidget(self.statLabel)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(CodeEditor)

        QMetaObject.connectSlotsByName(CodeEditor)
    # setupUi

    def retranslateUi(self, CodeEditor):
        CodeEditor.setWindowTitle(QCoreApplication.translate("CodeEditor", u"Edit File", None))
        self.findButton.setText(QCoreApplication.translate("CodeEditor", u"Find", None))
        self.saveButton.setText(QCoreApplication.translate("CodeEditor", u"Save/Reload", None))
        self.langButton.setText(QCoreApplication.translate("CodeEditor", u"Change Language", None))
        self.statLabel.setText(QCoreApplication.translate("CodeEditor", u"Lines", None))
    # retranslateUi

