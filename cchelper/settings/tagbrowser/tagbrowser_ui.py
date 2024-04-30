# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tagbrowser.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QListView,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_TagBrowser(object):
    def setupUi(self, TagBrowser):
        if not TagBrowser.objectName():
            TagBrowser.setObjectName(u"TagBrowser")
        TagBrowser.resize(279, 333)
        TagBrowser.setWindowTitle(u"Tags")
        self.verticalLayout = QVBoxLayout(TagBrowser)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.view = QListView(TagBrowser)
        self.view.setObjectName(u"view")

        self.verticalLayout.addWidget(self.view)

        self.label = QLabel(TagBrowser)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)


        self.retranslateUi(TagBrowser)

        QMetaObject.connectSlotsByName(TagBrowser)
    # setupUi

    def retranslateUi(self, TagBrowser):
        self.label.setText(QCoreApplication.translate("TagBrowser", u"** First 2 tags are unchangable, and max. cnt. of tags should <= 64.", None))
        pass
    # retranslateUi

