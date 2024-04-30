# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'fileviewer.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QPlainTextEdit, QSizePolicy,
    QSpacerItem, QSpinBox, QToolButton, QVBoxLayout,
    QWidget)

class Ui_FileViewer(object):
    def setupUi(self, FileViewer):
        if not FileViewer.objectName():
            FileViewer.setObjectName(u"FileViewer")
        FileViewer.resize(559, 507)
        FileViewer.setWindowTitle(u"View File")
        self.verticalLayout = QVBoxLayout(FileViewer)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.textEdit = QPlainTextEdit(FileViewer)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout.addWidget(self.textEdit)

        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.setSpacing(0)
        self.bottomLayout.setObjectName(u"bottomLayout")
        self.findButton = QToolButton(FileViewer)
        self.findButton.setObjectName(u"findButton")

        self.bottomLayout.addWidget(self.findButton)

        self.headButton = QToolButton(FileViewer)
        self.headButton.setObjectName(u"headButton")
        self.headButton.setCheckable(False)
        self.headButton.setAutoExclusive(False)

        self.bottomLayout.addWidget(self.headButton)

        self.tailButton = QToolButton(FileViewer)
        self.tailButton.setObjectName(u"tailButton")
        self.tailButton.setCheckable(True)
        self.tailButton.setChecked(False)
        self.tailButton.setAutoExclusive(False)

        self.bottomLayout.addWidget(self.tailButton)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottomLayout.addItem(self.horizontalSpacer_3)

        self.pageSzSpinBox = QSpinBox(FileViewer)
        self.pageSzSpinBox.setObjectName(u"pageSzSpinBox")
        self.pageSzSpinBox.setFocusPolicy(Qt.TabFocus)
        self.pageSzSpinBox.setSuffix(u" bytes")

        self.bottomLayout.addWidget(self.pageSzSpinBox)

        self.prevButton = QToolButton(FileViewer)
        self.prevButton.setObjectName(u"prevButton")

        self.bottomLayout.addWidget(self.prevButton)

        self.pageNoSpinBox = QSpinBox(FileViewer)
        self.pageNoSpinBox.setObjectName(u"pageNoSpinBox")
        self.pageNoSpinBox.setFocusPolicy(Qt.TabFocus)
        self.pageNoSpinBox.setSuffix(u" pages")
        self.pageNoSpinBox.setPrefix(u"")

        self.bottomLayout.addWidget(self.pageNoSpinBox)

        self.nextButton = QToolButton(FileViewer)
        self.nextButton.setObjectName(u"nextButton")

        self.bottomLayout.addWidget(self.nextButton)


        self.verticalLayout.addLayout(self.bottomLayout)


        self.retranslateUi(FileViewer)

        QMetaObject.connectSlotsByName(FileViewer)
    # setupUi

    def retranslateUi(self, FileViewer):
        self.findButton.setText(QCoreApplication.translate("FileViewer", u"Find", None))
        self.headButton.setText(QCoreApplication.translate("FileViewer", u"Head", None))
        self.tailButton.setText(QCoreApplication.translate("FileViewer", u"Tail -f", None))
        self.prevButton.setText(QCoreApplication.translate("FileViewer", u"<", None))
        self.nextButton.setText(QCoreApplication.translate("FileViewer", u">", None))
        pass
    # retranslateUi

