# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialogButtonBox, QFormLayout,
    QLabel, QLineEdit, QSizePolicy, QVBoxLayout,
    QWidget)

from cchelper import MultiComboBox

class Ui_TaskEditor(object):
    def setupUi(self, TaskEditor):
        if not TaskEditor.objectName():
            TaskEditor.setObjectName(u"TaskEditor")
        TaskEditor.resize(381, 154)
        font = QFont()
        font.setFamilies([u".AppleSystemUIFont"])
        TaskEditor.setFont(font)
        TaskEditor.setWindowTitle(u"Archive Task")
        self.verticalLayout = QVBoxLayout(TaskEditor)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.tagsLabel = QLabel(TaskEditor)
        self.tagsLabel.setObjectName(u"tagsLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.tagsLabel)

        self.tagsComboBox = MultiComboBox(TaskEditor)
        self.tagsComboBox.setObjectName(u"tagsComboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tagsComboBox.sizePolicy().hasHeightForWidth())
        self.tagsComboBox.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.tagsComboBox)

        self.urlLabel = QLabel(TaskEditor)
        self.urlLabel.setObjectName(u"urlLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.urlLabel)

        self.urlLineEdit = QLineEdit(TaskEditor)
        self.urlLineEdit.setObjectName(u"urlLineEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.urlLineEdit)

        self.docLabel = QLabel(TaskEditor)
        self.docLabel.setObjectName(u"docLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.docLabel)

        self.docLineEdit = QLineEdit(TaskEditor)
        self.docLineEdit.setObjectName(u"docLineEdit")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.docLineEdit)


        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(TaskEditor)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(TaskEditor)

        QMetaObject.connectSlotsByName(TaskEditor)
    # setupUi

    def retranslateUi(self, TaskEditor):
        self.tagsLabel.setText(QCoreApplication.translate("TaskEditor", u"Tags:", None))
        self.urlLabel.setText(QCoreApplication.translate("TaskEditor", u"Url:", None))
        self.docLabel.setText(QCoreApplication.translate("TaskEditor", u"Doc:", None))
        pass
    # retranslateUi

