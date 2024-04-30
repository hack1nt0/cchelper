# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'textfinder.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLineEdit,
    QSizePolicy, QSpacerItem, QSpinBox, QToolButton,
    QVBoxLayout, QWidget)

class Ui_TextFinder(object):
    def setupUi(self, TextFinder):
        if not TextFinder.objectName():
            TextFinder.setObjectName(u"TextFinder")
        TextFinder.resize(251, 79)
        self.verticalLayout = QVBoxLayout(TextFinder)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lineEdit = QLineEdit(TextFinder)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setPlaceholderText(u"NOT NULL")

        self.verticalLayout.addWidget(self.lineEdit)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.stopButton = QToolButton(TextFinder)
        self.stopButton.setObjectName(u"stopButton")

        self.horizontalLayout.addWidget(self.stopButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.spinBox = QSpinBox(TextFinder)
        self.spinBox.setObjectName(u"spinBox")

        self.horizontalLayout.addWidget(self.spinBox)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(TextFinder)

        QMetaObject.connectSlotsByName(TextFinder)
    # setupUi

    def retranslateUi(self, TextFinder):
        TextFinder.setWindowTitle(QCoreApplication.translate("TextFinder", u"Find Text", None))
        self.stopButton.setText(QCoreApplication.translate("TextFinder", u"Stop", None))
    # retranslateUi

