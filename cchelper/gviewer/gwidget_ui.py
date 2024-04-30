# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gwidget.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QDialog, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QSizePolicy,
    QSpacerItem, QSpinBox, QToolButton, QVBoxLayout,
    QWidget)

from cchelper.gviewer.gview import GView

class Ui_GWidget(object):
    def setupUi(self, GWidget):
        if not GWidget.objectName():
            GWidget.setObjectName(u"GWidget")
        GWidget.resize(589, 496)
        GWidget.setWindowTitle(u"Graph")
        self.verticalLayout = QVBoxLayout(GWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.view = GView(GWidget)
        self.view.setObjectName(u"view")

        self.verticalLayout.addWidget(self.view)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.FButton = QToolButton(GWidget)
        self.FButton.setObjectName(u"FButton")

        self.horizontalLayout.addWidget(self.FButton)

        self.findWidget = QFrame(GWidget)
        self.findWidget.setObjectName(u"findWidget")
        self.findLayout = QHBoxLayout(self.findWidget)
        self.findLayout.setSpacing(0)
        self.findLayout.setObjectName(u"findLayout")
        self.findLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit = QLineEdit(self.findWidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.findLayout.addWidget(self.lineEdit)

        self.CFButton = QToolButton(self.findWidget)
        self.CFButton.setObjectName(u"CFButton")

        self.findLayout.addWidget(self.CFButton)


        self.horizontalLayout.addWidget(self.findWidget)

        self.LButton = QToolButton(GWidget)
        self.LButton.setObjectName(u"LButton")
        self.LButton.setPopupMode(QToolButton.InstantPopup)

        self.horizontalLayout.addWidget(self.LButton)

        self.saveButton = QToolButton(GWidget)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalLayout.addWidget(self.saveButton)

        self.editButton = QToolButton(GWidget)
        self.editButton.setObjectName(u"editButton")

        self.horizontalLayout.addWidget(self.editButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label = QLabel(GWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.spinBox = QSpinBox(GWidget)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setWrapping(False)
        self.spinBox.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox.setProperty("showGroupSeparator", False)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(10000001)

        self.horizontalLayout.addWidget(self.spinBox)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(GWidget)

        QMetaObject.connectSlotsByName(GWidget)
    # setupUi

    def retranslateUi(self, GWidget):
        self.FButton.setText(QCoreApplication.translate("GWidget", u"Find", None))
        self.CFButton.setText(QCoreApplication.translate("GWidget", u"X", None))
        self.LButton.setText(QCoreApplication.translate("GWidget", u"Layouts", None))
        self.saveButton.setText(QCoreApplication.translate("GWidget", u"Save", None))
        self.editButton.setText(QCoreApplication.translate("GWidget", u"Edit", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("GWidget", u"Nodes/Edges", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("GWidget", u"0/0", None))
        self.spinBox.setSuffix(QCoreApplication.translate("GWidget", u" pages", None))
        pass
    # retranslateUi

