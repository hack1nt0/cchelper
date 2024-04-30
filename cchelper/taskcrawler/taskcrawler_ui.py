# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'taskcrawler.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QFormLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTableView,
    QVBoxLayout, QWidget)

class Ui_TaskCrawler(object):
    def setupUi(self, TaskCrawler):
        if not TaskCrawler.objectName():
            TaskCrawler.setObjectName(u"TaskCrawler")
        TaskCrawler.setWindowModality(Qt.NonModal)
        TaskCrawler.resize(451, 395)
        TaskCrawler.setWindowTitle(u"Crawl Task")
        TaskCrawler.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        TaskCrawler.setModal(True)
        self.verticalLayout = QVBoxLayout(TaskCrawler)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.urlLabel = QLabel(TaskCrawler)
        self.urlLabel.setObjectName(u"urlLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.urlLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.urlLineEdit = QLineEdit(TaskCrawler)
        self.urlLineEdit.setObjectName(u"urlLineEdit")
        self.urlLineEdit.setAlignment(Qt.AlignCenter)
        self.urlLineEdit.setPlaceholderText(u"Url")

        self.horizontalLayout.addWidget(self.urlLineEdit)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout)

        self.taskLabel = QLabel(TaskCrawler)
        self.taskLabel.setObjectName(u"taskLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.taskLabel)

        self.taskTable = QTableView(TaskCrawler)
        self.taskTable.setObjectName(u"taskTable")
        self.taskTable.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)
        self.taskTable.setTabKeyNavigation(False)
        self.taskTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.taskTable)

        self.testLabel = QLabel(TaskCrawler)
        self.testLabel.setObjectName(u"testLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.testLabel)

        self.testTable = QTableView(TaskCrawler)
        self.testTable.setObjectName(u"testTable")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.testTable)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.crawlButton = QPushButton(TaskCrawler)
        self.crawlButton.setObjectName(u"crawlButton")

        self.horizontalLayout_2.addWidget(self.crawlButton)

        self.convertButton = QPushButton(TaskCrawler)
        self.convertButton.setObjectName(u"convertButton")

        self.horizontalLayout_2.addWidget(self.convertButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.okButton = QPushButton(TaskCrawler)
        self.okButton.setObjectName(u"okButton")
        self.okButton.setAutoDefault(False)

        self.horizontalLayout_2.addWidget(self.okButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(TaskCrawler)

        self.okButton.setDefault(False)


        QMetaObject.connectSlotsByName(TaskCrawler)
    # setupUi

    def retranslateUi(self, TaskCrawler):
        self.urlLabel.setText(QCoreApplication.translate("TaskCrawler", u"Url:", None))
        self.taskLabel.setText(QCoreApplication.translate("TaskCrawler", u"Tasks:", None))
        self.testLabel.setText(QCoreApplication.translate("TaskCrawler", u"Tests:", None))
        self.crawlButton.setText(QCoreApplication.translate("TaskCrawler", u"Crawl", None))
        self.convertButton.setText(QCoreApplication.translate("TaskCrawler", u"Convert I/A", None))
        self.okButton.setText(QCoreApplication.translate("TaskCrawler", u"OK", None))
        pass
    # retranslateUi

