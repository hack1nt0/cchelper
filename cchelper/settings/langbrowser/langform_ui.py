# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'langform.ui'
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
    QTextEdit, QVBoxLayout, QWidget)

class Ui_LangForm(object):
    def setupUi(self, LangForm):
        if not LangForm.objectName():
            LangForm.setObjectName(u"LangForm")
        LangForm.resize(507, 505)
        LangForm.setWindowTitle(u"Form")
        self.verticalLayout = QVBoxLayout(LangForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.nameLabel = QLabel(LangForm)
        self.nameLabel.setObjectName(u"nameLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.nameLabel)

        self.nameLineEdit = QLineEdit(LangForm)
        self.nameLineEdit.setObjectName(u"nameLineEdit")
        self.nameLineEdit.setPlaceholderText(u"NOT NULL")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.nameLineEdit)

        self.suffixLabel = QLabel(LangForm)
        self.suffixLabel.setObjectName(u"suffixLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.suffixLabel)

        self.suffixLineEdit = QLineEdit(LangForm)
        self.suffixLineEdit.setObjectName(u"suffixLineEdit")
        self.suffixLineEdit.setPlaceholderText(u"NOT NULL")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.suffixLineEdit)

        self.templateLabel = QLabel(LangForm)
        self.templateLabel.setObjectName(u"templateLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.templateLabel)

        self.templateTextEdit = QTextEdit(LangForm)
        self.templateTextEdit.setObjectName(u"templateTextEdit")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.templateTextEdit)


        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(LangForm)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(LangForm)
        self.buttonBox.accepted.connect(LangForm.accept)
        self.buttonBox.rejected.connect(LangForm.reject)

        QMetaObject.connectSlotsByName(LangForm)
    # setupUi

    def retranslateUi(self, LangForm):
        self.nameLabel.setText(QCoreApplication.translate("LangForm", u"Name:", None))
        self.suffixLabel.setText(QCoreApplication.translate("LangForm", u"Suffix:", None))
        self.templateLabel.setText(QCoreApplication.translate("LangForm", u"Template:", None))
        pass
    # retranslateUi

