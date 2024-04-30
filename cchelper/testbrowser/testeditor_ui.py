# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'testeditor.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFormLayout, QLabel, QSizePolicy,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_TestEditor(object):
    def setupUi(self, TestEditor):
        if not TestEditor.objectName():
            TestEditor.setObjectName(u"TestEditor")
        TestEditor.resize(312, 171)
        self.verticalLayout = QVBoxLayout(TestEditor)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.countLabel = QLabel(TestEditor)
        self.countLabel.setObjectName(u"countLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.countLabel)

        self.countSpinBox = QSpinBox(TestEditor)
        self.countSpinBox.setObjectName(u"countSpinBox")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.countSpinBox)

        self.inputTypeLabel = QLabel(TestEditor)
        self.inputTypeLabel.setObjectName(u"inputTypeLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.inputTypeLabel)

        self.inputTypeComboBox = QComboBox(TestEditor)
        self.inputTypeComboBox.setObjectName(u"inputTypeComboBox")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.inputTypeComboBox)

        self.answerTypeLabel = QLabel(TestEditor)
        self.answerTypeLabel.setObjectName(u"answerTypeLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.answerTypeLabel)

        self.answerTypeComboBox = QComboBox(TestEditor)
        self.answerTypeComboBox.setObjectName(u"answerTypeComboBox")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.answerTypeComboBox)


        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(TestEditor)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(TestEditor)
        self.buttonBox.accepted.connect(TestEditor.accept)
        self.buttonBox.rejected.connect(TestEditor.reject)

        QMetaObject.connectSlotsByName(TestEditor)
    # setupUi

    def retranslateUi(self, TestEditor):
        TestEditor.setWindowTitle(QCoreApplication.translate("TestEditor", u"Dialog", None))
        self.countLabel.setText(QCoreApplication.translate("TestEditor", u"Count:", None))
        self.inputTypeLabel.setText(QCoreApplication.translate("TestEditor", u"Input Type:", None))
        self.answerTypeLabel.setText(QCoreApplication.translate("TestEditor", u"Answer Type:", None))
    # retranslateUi

