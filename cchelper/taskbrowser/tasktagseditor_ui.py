# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tasktagseditor.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialogButtonBox,
    QFormLayout, QLabel, QLineEdit, QSizePolicy,
    QVBoxLayout, QWidget)

from cchelper import MultiComboBox

class Ui_TaskTagsEditor(object):
    def setupUi(self, TaskTagsEditor):
        if not TaskTagsEditor.objectName():
            TaskTagsEditor.setObjectName(u"TaskTagsEditor")
        TaskTagsEditor.resize(417, 221)
        font = QFont()
        font.setFamilies([u".AppleSystemUIFont"])
        TaskTagsEditor.setFont(font)
        TaskTagsEditor.setWindowTitle(u"Edit Task")
        self.verticalLayout = QVBoxLayout(TaskTagsEditor)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.tagsLabel = QLabel(TaskTagsEditor)
        self.tagsLabel.setObjectName(u"tagsLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.tagsLabel)

        self.tagsComboBox = MultiComboBox(TaskTagsEditor)
        self.tagsComboBox.setObjectName(u"tagsComboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tagsComboBox.sizePolicy().hasHeightForWidth())
        self.tagsComboBox.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.tagsComboBox)

        self.urlLabel = QLabel(TaskTagsEditor)
        self.urlLabel.setObjectName(u"urlLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.urlLabel)

        self.urlLineEdit = QLineEdit(TaskTagsEditor)
        self.urlLineEdit.setObjectName(u"urlLineEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.urlLineEdit)

        self.docLabel = QLabel(TaskTagsEditor)
        self.docLabel.setObjectName(u"docLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.docLabel)

        self.docLineEdit = QLineEdit(TaskTagsEditor)
        self.docLineEdit.setObjectName(u"docLineEdit")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.docLineEdit)

        self.statusLabel = QLabel(TaskTagsEditor)
        self.statusLabel.setObjectName(u"statusLabel")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.statusLabel)

        self.statusComboBox = QComboBox(TaskTagsEditor)
        self.statusComboBox.setObjectName(u"statusComboBox")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.statusComboBox)

        self.nameLabel = QLabel(TaskTagsEditor)
        self.nameLabel.setObjectName(u"nameLabel")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.nameLabel)

        self.nameLineEdit = QLineEdit(TaskTagsEditor)
        self.nameLineEdit.setObjectName(u"nameLineEdit")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.nameLineEdit)


        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(TaskTagsEditor)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(TaskTagsEditor)

        QMetaObject.connectSlotsByName(TaskTagsEditor)
    # setupUi

    def retranslateUi(self, TaskTagsEditor):
        self.tagsLabel.setText(QCoreApplication.translate("TaskTagsEditor", u"Tags:", None))
        self.urlLabel.setText(QCoreApplication.translate("TaskTagsEditor", u"Url:", None))
        self.docLabel.setText(QCoreApplication.translate("TaskTagsEditor", u"Doc:", None))
        self.statusLabel.setText(QCoreApplication.translate("TaskTagsEditor", u"Status:", None))
        self.nameLabel.setText(QCoreApplication.translate("TaskTagsEditor", u"Name:", None))
        pass
    # retranslateUi

