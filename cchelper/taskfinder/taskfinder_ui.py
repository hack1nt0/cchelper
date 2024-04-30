# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'taskfinder.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDateEdit,
    QDialogButtonBox, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QPlainTextEdit, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from cchelper import MultiComboBox

class Ui_TaskFinder(object):
    def setupUi(self, TaskFinder):
        if not TaskFinder.objectName():
            TaskFinder.setObjectName(u"TaskFinder")
        TaskFinder.resize(361, 363)
        TaskFinder.setWindowTitle(u"Find Task")
        self.verticalLayout = QVBoxLayout(TaskFinder)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTop|Qt.AlignTrailing)
        self.urlLabel = QLabel(TaskFinder)
        self.urlLabel.setObjectName(u"urlLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.urlLabel)

        self.urlLineEdit = QLineEdit(TaskFinder)
        self.urlLineEdit.setObjectName(u"urlLineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.urlLineEdit)

        self.nameLabel = QLabel(TaskFinder)
        self.nameLabel.setObjectName(u"nameLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.nameLabel)

        self.nameLineEdit = QLineEdit(TaskFinder)
        self.nameLineEdit.setObjectName(u"nameLineEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.nameLineEdit)

        self.tagsLabel = QLabel(TaskFinder)
        self.tagsLabel.setObjectName(u"tagsLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.tagsLabel)

        self.tagsComboBox = MultiComboBox(TaskFinder)
        self.tagsComboBox.setObjectName(u"tagsComboBox")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.tagsComboBox)

        self.creationTimeLabel = QLabel(TaskFinder)
        self.creationTimeLabel.setObjectName(u"creationTimeLabel")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.creationTimeLabel)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.cTimeLEdit = QDateEdit(TaskFinder)
        self.cTimeLEdit.setObjectName(u"cTimeLEdit")

        self.horizontalLayout_2.addWidget(self.cTimeLEdit)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.label = QLabel(TaskFinder)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.cTimeREdit = QDateEdit(TaskFinder)
        self.cTimeREdit.setObjectName(u"cTimeREdit")

        self.horizontalLayout_2.addWidget(self.cTimeREdit)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.solverContainsLabel = QLabel(TaskFinder)
        self.solverContainsLabel.setObjectName(u"solverContainsLabel")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.solverContainsLabel)

        self.solverContainsTextEdit = QPlainTextEdit(TaskFinder)
        self.solverContainsTextEdit.setObjectName(u"solverContainsTextEdit")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.solverContainsTextEdit)

        self.statusLabel = QLabel(TaskFinder)
        self.statusLabel.setObjectName(u"statusLabel")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.statusLabel)

        self.statusComboBox = QComboBox(TaskFinder)
        self.statusComboBox.setObjectName(u"statusComboBox")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.statusComboBox)


        self.verticalLayout.addLayout(self.formLayout)

        self.label_2 = QLabel(TaskFinder)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.label_2.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_2)

        self.buttonBox = QDialogButtonBox(TaskFinder)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.Reset)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(TaskFinder)

        QMetaObject.connectSlotsByName(TaskFinder)
    # setupUi

    def retranslateUi(self, TaskFinder):
        self.urlLabel.setText(QCoreApplication.translate("TaskFinder", u"Url*:", None))
        self.nameLabel.setText(QCoreApplication.translate("TaskFinder", u"Name*:", None))
        self.tagsLabel.setText(QCoreApplication.translate("TaskFinder", u"Tags:", None))
        self.creationTimeLabel.setText(QCoreApplication.translate("TaskFinder", u"Creation Time:", None))
        self.label.setText(QCoreApplication.translate("TaskFinder", u"<", None))
        self.solverContainsLabel.setText(QCoreApplication.translate("TaskFinder", u"Solver Contains*:", None))
        self.statusLabel.setText(QCoreApplication.translate("TaskFinder", u"Status:", None))
        self.label_2.setText(QCoreApplication.translate("TaskFinder", u"*: Substring match, case insensitive.", None))
        pass
    # retranslateUi

