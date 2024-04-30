# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'filefinder.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QLabel, QLineEdit, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_FileFinder(object):
    def setupUi(self, FileFinder):
        if not FileFinder.objectName():
            FileFinder.setObjectName(u"FileFinder")
        FileFinder.resize(354, 118)
        self.verticalLayout = QVBoxLayout(FileFinder)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setLabelAlignment(Qt.AlignCenter)
        self.pathLabel = QLabel(FileFinder)
        self.pathLabel.setObjectName(u"pathLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.pathLabel)

        self.pathLineEdit = QLineEdit(FileFinder)
        self.pathLineEdit.setObjectName(u"pathLineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.pathLineEdit)

        self.containsLabel = QLabel(FileFinder)
        self.containsLabel.setObjectName(u"containsLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.containsLabel)

        self.containsLineEdit = QLineEdit(FileFinder)
        self.containsLineEdit.setObjectName(u"containsLineEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.containsLineEdit)


        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(FileFinder)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(FileFinder)
        self.buttonBox.accepted.connect(FileFinder.accept)
        self.buttonBox.rejected.connect(FileFinder.reject)

        QMetaObject.connectSlotsByName(FileFinder)
    # setupUi

    def retranslateUi(self, FileFinder):
        FileFinder.setWindowTitle(QCoreApplication.translate("FileFinder", u"Dialog", None))
        self.pathLabel.setText(QCoreApplication.translate("FileFinder", u"Path:", None))
        self.containsLabel.setText(QCoreApplication.translate("FileFinder", u"Contains:", None))
    # retranslateUi

