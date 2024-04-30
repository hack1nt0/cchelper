# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tasktestparamseditor.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QFormLayout, QHBoxLayout,
    QLabel, QSizePolicy, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_TaskTestParamsEditor(object):
    def setupUi(self, TaskTestParamsEditor):
        if not TaskTestParamsEditor.objectName():
            TaskTestParamsEditor.setObjectName(u"TaskTestParamsEditor")
        TaskTestParamsEditor.resize(339, 192)
        TaskTestParamsEditor.setWindowTitle(u"Edit Task")
        self.verticalLayout = QVBoxLayout(TaskTestParamsEditor)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(Qt.AlignRight|Qt.AlignTop|Qt.AlignTrailing)
        self.comparatorLabel = QLabel(TaskTestParamsEditor)
        self.comparatorLabel.setObjectName(u"comparatorLabel")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.comparatorLabel)

        self.comparatorComboBox = QComboBox(TaskTestParamsEditor)
        self.comparatorComboBox.setObjectName(u"comparatorComboBox")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.comparatorComboBox)

        self.cpuLabel = QLabel(TaskTestParamsEditor)
        self.cpuLabel.setObjectName(u"cpuLabel")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.cpuLabel)

        self.cpuBox = QSpinBox(TaskTestParamsEditor)
        self.cpuBox.setObjectName(u"cpuBox")
        self.cpuBox.setSuffix(u" milliseconds")
        self.cpuBox.setMaximum(1000000)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.cpuBox)

        self.memLabel = QLabel(TaskTestParamsEditor)
        self.memLabel.setObjectName(u"memLabel")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.memLabel)

        self.memBox = QSpinBox(TaskTestParamsEditor)
        self.memBox.setObjectName(u"memBox")
        self.memBox.setSuffix(u" megabytes")
        self.memBox.setMaximum(1025)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.memBox)

        self.qryLabel = QLabel(TaskTestParamsEditor)
        self.qryLabel.setObjectName(u"qryLabel")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.qryLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.qryBox = QSpinBox(TaskTestParamsEditor)
        self.qryBox.setObjectName(u"qryBox")
        self.qryBox.setSuffix(u"")
        self.qryBox.setMaximum(101)

        self.horizontalLayout.addWidget(self.qryBox)

        self.interactiveCheckBox = QCheckBox(TaskTestParamsEditor)
        self.interactiveCheckBox.setObjectName(u"interactiveCheckBox")

        self.horizontalLayout.addWidget(self.interactiveCheckBox)


        self.formLayout_2.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout)


        self.verticalLayout.addLayout(self.formLayout_2)

        self.buttonBox = QDialogButtonBox(TaskTestParamsEditor)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(TaskTestParamsEditor)

        QMetaObject.connectSlotsByName(TaskTestParamsEditor)
    # setupUi

    def retranslateUi(self, TaskTestParamsEditor):
        self.comparatorLabel.setText(QCoreApplication.translate("TaskTestParamsEditor", u"Compare Type:", None))
        self.cpuLabel.setText(QCoreApplication.translate("TaskTestParamsEditor", u"Cpu:", None))
        self.memLabel.setText(QCoreApplication.translate("TaskTestParamsEditor", u"Mem:", None))
        self.qryLabel.setText(QCoreApplication.translate("TaskTestParamsEditor", u"Qry:", None))
        self.interactiveCheckBox.setText(QCoreApplication.translate("TaskTestParamsEditor", u"Interactive ?", None))
        pass
    # retranslateUi

