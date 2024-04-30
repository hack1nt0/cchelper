# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'texteditor.ui'
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
    QPlainTextEdit, QSizePolicy, QSpacerItem, QToolButton,
    QVBoxLayout, QWidget)

class Ui_TextEditor(object):
    def setupUi(self, TextEditor):
        if not TextEditor.objectName():
            TextEditor.setObjectName(u"TextEditor")
        TextEditor.resize(476, 369)
        self.verticalLayout = QVBoxLayout(TextEditor)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.textEdit = QPlainTextEdit(TextEditor)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout.addWidget(self.textEdit)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.saveButton = QToolButton(TextEditor)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalLayout.addWidget(self.saveButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.statLabel = QLabel(TextEditor)
        self.statLabel.setObjectName(u"statLabel")

        self.horizontalLayout.addWidget(self.statLabel)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(TextEditor)

        QMetaObject.connectSlotsByName(TextEditor)
    # setupUi

    def retranslateUi(self, TextEditor):
        TextEditor.setWindowTitle(QCoreApplication.translate("TextEditor", u"Edit File", None))
        self.saveButton.setText(QCoreApplication.translate("TextEditor", u"Save", None))
        self.statLabel.setText(QCoreApplication.translate("TextEditor", u"Lines", None))
    # retranslateUi

