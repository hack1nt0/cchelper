# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'confform.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFormLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QRadioButton, QSizePolicy, QSpinBox, QToolButton,
    QVBoxLayout, QWidget)

class Ui_ConfForm(object):
    def setupUi(self, ConfForm):
        if not ConfForm.objectName():
            ConfForm.setObjectName(u"ConfForm")
        ConfForm.resize(441, 434)
        ConfForm.setWindowTitle(u"Settings")
        self.verticalLayout = QVBoxLayout(ConfForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.stashDirectoryLabel = QLabel(ConfForm)
        self.stashDirectoryLabel.setObjectName(u"stashDirectoryLabel")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.stashDirectoryLabel)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.projectEdit = QLineEdit(ConfForm)
        self.projectEdit.setObjectName(u"projectEdit")
        self.projectEdit.setReadOnly(True)

        self.horizontalLayout_7.addWidget(self.projectEdit)

        self.openButton = QToolButton(ConfForm)
        self.openButton.setObjectName(u"openButton")

        self.horizontalLayout_7.addWidget(self.openButton)


        self.formLayout_2.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_7)

        self.defaultFileNameLabel = QLabel(ConfForm)
        self.defaultFileNameLabel.setObjectName(u"defaultFileNameLabel")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.defaultFileNameLabel)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.SLineEdit = QLineEdit(ConfForm)
        self.SLineEdit.setObjectName(u"SLineEdit")
        self.SLineEdit.setPlaceholderText(u"Solver")

        self.horizontalLayout_5.addWidget(self.SLineEdit)

        self.label_3 = QLabel(ConfForm)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_5.addWidget(self.label_3)

        self.GLineEdit = QLineEdit(ConfForm)
        self.GLineEdit.setObjectName(u"GLineEdit")

        self.horizontalLayout_5.addWidget(self.GLineEdit)

        self.label_2 = QLabel(ConfForm)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_5.addWidget(self.label_2)

        self.JLineEdit = QLineEdit(ConfForm)
        self.JLineEdit.setObjectName(u"JLineEdit")

        self.horizontalLayout_5.addWidget(self.JLineEdit)


        self.formLayout_2.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_5)

        self.editorLabel = QLabel(ConfForm)
        self.editorLabel.setObjectName(u"editorLabel")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.editorLabel)

        self.editorEdit = QLineEdit(ConfForm)
        self.editorEdit.setObjectName(u"editorEdit")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.editorEdit)

        self.maxBitsLabel = QLabel(ConfForm)
        self.maxBitsLabel.setObjectName(u"maxBitsLabel")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.maxBitsLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.bytesPerCellSpinBox = QSpinBox(ConfForm)
        self.bytesPerCellSpinBox.setObjectName(u"bytesPerCellSpinBox")
        self.bytesPerCellSpinBox.setMinimum(1)
        self.bytesPerCellSpinBox.setMaximum(100001)
        self.bytesPerCellSpinBox.setValue(1000)

        self.horizontalLayout.addWidget(self.bytesPerCellSpinBox)

        self.rowsPerPageSpinBox = QSpinBox(ConfForm)
        self.rowsPerPageSpinBox.setObjectName(u"rowsPerPageSpinBox")
        self.rowsPerPageSpinBox.setSuffix(u" rows/page")
        self.rowsPerPageSpinBox.setMinimum(1)
        self.rowsPerPageSpinBox.setMaximum(100001)
        self.rowsPerPageSpinBox.setValue(10)

        self.horizontalLayout.addWidget(self.rowsPerPageSpinBox)


        self.formLayout_2.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout)

        self.initialRowsLabel = QLabel(ConfForm)
        self.initialRowsLabel.setObjectName(u"initialRowsLabel")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.initialRowsLabel)

        self.bytesPerPageSpinBox = QSpinBox(ConfForm)
        self.bytesPerPageSpinBox.setObjectName(u"bytesPerPageSpinBox")
        self.bytesPerPageSpinBox.setSuffix(u" bytes/page")
        self.bytesPerPageSpinBox.setMinimum(1)
        self.bytesPerPageSpinBox.setMaximum(100001)
        self.bytesPerPageSpinBox.setValue(10000)

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.bytesPerPageSpinBox)

        self.pipeLabel = QLabel(ConfForm)
        self.pipeLabel.setObjectName(u"pipeLabel")

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.pipeLabel)

        self.bytesPerReadSpinBox = QSpinBox(ConfForm)
        self.bytesPerReadSpinBox.setObjectName(u"bytesPerReadSpinBox")
        self.bytesPerReadSpinBox.setSuffix(u" bytes/read")
        self.bytesPerReadSpinBox.setMinimum(1)
        self.bytesPerReadSpinBox.setMaximum(1000001)

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.bytesPerReadSpinBox)

        self.buildOptsLabel = QLabel(ConfForm)
        self.buildOptsLabel.setObjectName(u"buildOptsLabel")

        self.formLayout_2.setWidget(6, QFormLayout.LabelRole, self.buildOptsLabel)

        self.buildModeGroupBox = QGroupBox(ConfForm)
        self.buildModeGroupBox.setObjectName(u"buildModeGroupBox")
        self.buildModeGroupBox.setFlat(True)
        self.horizontalLayout_4 = QHBoxLayout(self.buildModeGroupBox)
#ifndef Q_OS_MAC
        self.horizontalLayout_4.setSpacing(-1)
#endif
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.buildDebugRadioButton = QRadioButton(self.buildModeGroupBox)
        self.buildDebugRadioButton.setObjectName(u"buildDebugRadioButton")
        self.buildDebugRadioButton.setChecked(True)

        self.horizontalLayout_4.addWidget(self.buildDebugRadioButton)

        self.buildReleaseRadioButton = QRadioButton(self.buildModeGroupBox)
        self.buildReleaseRadioButton.setObjectName(u"buildReleaseRadioButton")

        self.horizontalLayout_4.addWidget(self.buildReleaseRadioButton)


        self.formLayout_2.setWidget(6, QFormLayout.FieldRole, self.buildModeGroupBox)

        self.buildAsNeedCheckBox = QCheckBox(ConfForm)
        self.buildAsNeedCheckBox.setObjectName(u"buildAsNeedCheckBox")

        self.formLayout_2.setWidget(7, QFormLayout.FieldRole, self.buildAsNeedCheckBox)

        self.runinshellCheckBox = QCheckBox(ConfForm)
        self.runinshellCheckBox.setObjectName(u"runinshellCheckBox")

        self.formLayout_2.setWidget(8, QFormLayout.FieldRole, self.runinshellCheckBox)

        self.dumpWarmUpLabel = QLabel(ConfForm)
        self.dumpWarmUpLabel.setObjectName(u"dumpWarmUpLabel")

        self.formLayout_2.setWidget(9, QFormLayout.LabelRole, self.dumpWarmUpLabel)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.exeDumpSpinBox = QSpinBox(ConfForm)
        self.exeDumpSpinBox.setObjectName(u"exeDumpSpinBox")
        self.exeDumpSpinBox.setSuffix(u" seconds")
        self.exeDumpSpinBox.setMinimum(1)

        self.horizontalLayout_2.addWidget(self.exeDumpSpinBox)

        self.exeWarmSpinBox = QSpinBox(ConfForm)
        self.exeWarmSpinBox.setObjectName(u"exeWarmSpinBox")
        self.exeWarmSpinBox.setSuffix(u" seconds")
        self.exeWarmSpinBox.setMinimum(2)

        self.horizontalLayout_2.addWidget(self.exeWarmSpinBox)


        self.formLayout_2.setLayout(9, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.parallelLabel = QLabel(ConfForm)
        self.parallelLabel.setObjectName(u"parallelLabel")

        self.formLayout_2.setWidget(10, QFormLayout.LabelRole, self.parallelLabel)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.parallelSpinBox = QSpinBox(ConfForm)
        self.parallelSpinBox.setObjectName(u"parallelSpinBox")
        self.parallelSpinBox.setSuffix(u" threads")
        self.parallelSpinBox.setMinimum(1)
        self.parallelSpinBox.setMaximum(32)

        self.horizontalLayout_6.addWidget(self.parallelSpinBox)

        self.refreshRateSpinBox = QSpinBox(ConfForm)
        self.refreshRateSpinBox.setObjectName(u"refreshRateSpinBox")
        self.refreshRateSpinBox.setSuffix(u" Hz")
        self.refreshRateSpinBox.setMinimum(1)
        self.refreshRateSpinBox.setMaximum(60)

        self.horizontalLayout_6.addWidget(self.refreshRateSpinBox)


        self.formLayout_2.setLayout(10, QFormLayout.FieldRole, self.horizontalLayout_6)

        self.fontLabel = QLabel(ConfForm)
        self.fontLabel.setObjectName(u"fontLabel")

        self.formLayout_2.setWidget(11, QFormLayout.LabelRole, self.fontLabel)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.fontLineEdit = QLineEdit(ConfForm)
        self.fontLineEdit.setObjectName(u"fontLineEdit")

        self.horizontalLayout_3.addWidget(self.fontLineEdit)

        self.fontButton = QToolButton(ConfForm)
        self.fontButton.setObjectName(u"fontButton")

        self.horizontalLayout_3.addWidget(self.fontButton)


        self.formLayout_2.setLayout(11, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.graphvizLabel = QLabel(ConfForm)
        self.graphvizLabel.setObjectName(u"graphvizLabel")

        self.formLayout_2.setWidget(12, QFormLayout.LabelRole, self.graphvizLabel)

        self.graphvizLineEdit = QLineEdit(ConfForm)
        self.graphvizLineEdit.setObjectName(u"graphvizLineEdit")

        self.formLayout_2.setWidget(12, QFormLayout.FieldRole, self.graphvizLineEdit)


        self.verticalLayout.addLayout(self.formLayout_2)


        self.retranslateUi(ConfForm)

        QMetaObject.connectSlotsByName(ConfForm)
    # setupUi

    def retranslateUi(self, ConfForm):
        self.stashDirectoryLabel.setText(QCoreApplication.translate("ConfForm", u"Project Dir:", None))
        self.openButton.setText(QCoreApplication.translate("ConfForm", u"...", None))
        self.defaultFileNameLabel.setText(QCoreApplication.translate("ConfForm", u"Default Files:", None))
        self.SLineEdit.setText(QCoreApplication.translate("ConfForm", u"Solver.cpp", None))
        self.label_3.setText(QCoreApplication.translate("ConfForm", u" + ", None))
        self.GLineEdit.setText(QCoreApplication.translate("ConfForm", u"Generator.py", None))
        self.GLineEdit.setPlaceholderText(QCoreApplication.translate("ConfForm", u"Generator", None))
        self.label_2.setText(QCoreApplication.translate("ConfForm", u" + ", None))
        self.JLineEdit.setText(QCoreApplication.translate("ConfForm", u"Jurger.cpp", None))
        self.JLineEdit.setPlaceholderText(QCoreApplication.translate("ConfForm", u"Jurger", None))
        self.editorLabel.setText(QCoreApplication.translate("ConfForm", u"Ext. Editor:", None))
        self.maxBitsLabel.setText(QCoreApplication.translate("ConfForm", u"Table:", None))
        self.bytesPerCellSpinBox.setSuffix(QCoreApplication.translate("ConfForm", u" bytes/cell", None))
        self.initialRowsLabel.setText(QCoreApplication.translate("ConfForm", u"File Viewer:", None))
        self.pipeLabel.setText(QCoreApplication.translate("ConfForm", u"Pipe:", None))
        self.buildOptsLabel.setText(QCoreApplication.translate("ConfForm", u"Build Mode:", None))
        self.buildDebugRadioButton.setText(QCoreApplication.translate("ConfForm", u"Debug", None))
        self.buildReleaseRadioButton.setText(QCoreApplication.translate("ConfForm", u"Release", None))
        self.buildAsNeedCheckBox.setText(QCoreApplication.translate("ConfForm", u"Build as need", None))
        self.runinshellCheckBox.setText(QCoreApplication.translate("ConfForm", u"Run in shell mode", None))
        self.dumpWarmUpLabel.setText(QCoreApplication.translate("ConfForm", u"Dump/Warm:", None))
        self.parallelLabel.setText(QCoreApplication.translate("ConfForm", u"Parallels:", None))
        self.fontLabel.setText(QCoreApplication.translate("ConfForm", u"Font:", None))
        self.fontButton.setText(QCoreApplication.translate("ConfForm", u"...", None))
        self.graphvizLabel.setText(QCoreApplication.translate("ConfForm", u"Graphviz:", None))
        pass
    # retranslateUi

