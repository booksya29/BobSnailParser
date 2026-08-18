# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QProgressBar, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(1920, 1080)
        self.gridLayout = QGridLayout(Widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.centralContainer = QWidget(Widget)
        self.centralContainer.setObjectName(u"centralContainer")
        self.centralContainer.setMinimumSize(QSize(600, 0))
        self.centralContainer.setMaximumSize(QSize(700, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.centralContainer)
        self.verticalLayout_2.setSpacing(12)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.AshanLabel = QLabel(self.centralContainer)
        self.AshanLabel.setObjectName(u"AshanLabel")
        self.AshanLabel.setMinimumSize(QSize(70, 0))

        self.horizontalLayout.addWidget(self.AshanLabel)

        self.AshanProgressBar = QProgressBar(self.centralContainer)
        self.AshanProgressBar.setObjectName(u"AshanProgressBar")
        self.AshanProgressBar.setValue(0)
        self.AshanProgressBar.setTextVisible(True)

        self.horizontalLayout.addWidget(self.AshanProgressBar)

        self.AshanButton = QPushButton(self.centralContainer)
        self.AshanButton.setObjectName(u"AshanButton")

        self.horizontalLayout.addWidget(self.AshanButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.SilpoLabel = QLabel(self.centralContainer)
        self.SilpoLabel.setObjectName(u"SilpoLabel")
        self.SilpoLabel.setMinimumSize(QSize(70, 0))

        self.horizontalLayout_3.addWidget(self.SilpoLabel)

        self.SilpoProgressBar = QProgressBar(self.centralContainer)
        self.SilpoProgressBar.setObjectName(u"SilpoProgressBar")
        self.SilpoProgressBar.setValue(0)
        self.SilpoProgressBar.setTextVisible(True)

        self.horizontalLayout_3.addWidget(self.SilpoProgressBar)

        self.SilpoButton = QPushButton(self.centralContainer)
        self.SilpoButton.setObjectName(u"SilpoButton")

        self.horizontalLayout_3.addWidget(self.SilpoButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.ATBLabel = QLabel(self.centralContainer)
        self.ATBLabel.setObjectName(u"ATBLabel")
        self.ATBLabel.setMinimumSize(QSize(70, 0))

        self.horizontalLayout_4.addWidget(self.ATBLabel)

        self.ATBProgressBar = QProgressBar(self.centralContainer)
        self.ATBProgressBar.setObjectName(u"ATBProgressBar")
        self.ATBProgressBar.setValue(0)
        self.ATBProgressBar.setTextVisible(True)

        self.horizontalLayout_4.addWidget(self.ATBProgressBar)

        self.ATBButton = QPushButton(self.centralContainer)
        self.ATBButton.setObjectName(u"ATBButton")

        self.horizontalLayout_4.addWidget(self.ATBButton)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.FozzyLabel = QLabel(self.centralContainer)
        self.FozzyLabel.setObjectName(u"FozzyLabel")
        self.FozzyLabel.setMinimumSize(QSize(70, 0))

        self.horizontalLayout_5.addWidget(self.FozzyLabel)

        self.FozzyProgressBar = QProgressBar(self.centralContainer)
        self.FozzyProgressBar.setObjectName(u"FozzyProgressBar")
        self.FozzyProgressBar.setValue(0)
        self.FozzyProgressBar.setTextVisible(True)

        self.horizontalLayout_5.addWidget(self.FozzyProgressBar)

        self.FozzyButton = QPushButton(self.centralContainer)
        self.FozzyButton.setObjectName(u"FozzyButton")

        self.horizontalLayout_5.addWidget(self.FozzyButton)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.NovusLabel = QLabel(self.centralContainer)
        self.NovusLabel.setObjectName(u"NovusLabel")
        self.NovusLabel.setMinimumSize(QSize(70, 0))

        self.horizontalLayout_6.addWidget(self.NovusLabel)

        self.NovusProgressBar = QProgressBar(self.centralContainer)
        self.NovusProgressBar.setObjectName(u"NovusProgressBar")
        self.NovusProgressBar.setValue(0)
        self.NovusProgressBar.setTextVisible(True)

        self.horizontalLayout_6.addWidget(self.NovusProgressBar)

        self.NovusButton = QPushButton(self.centralContainer)
        self.NovusButton.setObjectName(u"NovusButton")

        self.horizontalLayout_6.addWidget(self.NovusButton)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.ForaLabel = QLabel(self.centralContainer)
        self.ForaLabel.setObjectName(u"ForaLabel")
        self.ForaLabel.setMinimumSize(QSize(70, 0))

        self.horizontalLayout_7.addWidget(self.ForaLabel)

        self.ForaProgressBar = QProgressBar(self.centralContainer)
        self.ForaProgressBar.setObjectName(u"ForaProgressBar")
        self.ForaProgressBar.setValue(0)
        self.ForaProgressBar.setTextVisible(True)

        self.horizontalLayout_7.addWidget(self.ForaProgressBar)

        self.ForaButton = QPushButton(self.centralContainer)
        self.ForaButton.setObjectName(u"ForaButton")

        self.horizontalLayout_7.addWidget(self.ForaButton)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.VarusLabel = QLabel(self.centralContainer)
        self.VarusLabel.setObjectName(u"VarusLabel")
        self.VarusLabel.setMinimumSize(QSize(70, 0))

        self.horizontalLayout_8.addWidget(self.VarusLabel)

        self.VarusProgressBar = QProgressBar(self.centralContainer)
        self.VarusProgressBar.setObjectName(u"VarusProgressBar")
        self.VarusProgressBar.setValue(0)
        self.VarusProgressBar.setTextVisible(True)

        self.horizontalLayout_8.addWidget(self.VarusProgressBar)

        self.VarusButton = QPushButton(self.centralContainer)
        self.VarusButton.setObjectName(u"VarusButton")

        self.horizontalLayout_8.addWidget(self.VarusButton)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.MetroLabel = QLabel(self.centralContainer)
        self.MetroLabel.setObjectName(u"MetroLabel")
        self.MetroLabel.setMinimumSize(QSize(70, 0))

        self.horizontalLayout_9.addWidget(self.MetroLabel)

        self.MetroProgressBar = QProgressBar(self.centralContainer)
        self.MetroProgressBar.setObjectName(u"MetroProgressBar")
        self.MetroProgressBar.setValue(0)
        self.MetroProgressBar.setTextVisible(True)

        self.horizontalLayout_9.addWidget(self.MetroProgressBar)

        self.MetroButton = QPushButton(self.centralContainer)
        self.MetroButton.setObjectName(u"MetroButton")

        self.horizontalLayout_9.addWidget(self.MetroButton)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.TavriaLabel = QLabel(self.centralContainer)
        self.TavriaLabel.setObjectName(u"TavriaLabel")
        self.TavriaLabel.setMinimumSize(QSize(70, 0))

        self.horizontalLayout_10.addWidget(self.TavriaLabel)

        self.TavriaProgressBar = QProgressBar(self.centralContainer)
        self.TavriaProgressBar.setObjectName(u"TavriaProgressBar")
        self.TavriaProgressBar.setValue(0)
        self.TavriaProgressBar.setTextVisible(True)

        self.horizontalLayout_10.addWidget(self.TavriaProgressBar)

        self.TavriaButton = QPushButton(self.centralContainer)
        self.TavriaButton.setObjectName(u"TavriaButton")

        self.horizontalLayout_10.addWidget(self.TavriaButton)


        self.verticalLayout.addLayout(self.horizontalLayout_10)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.StartButton = QPushButton(self.centralContainer)
        self.StartButton.setObjectName(u"StartButton")
        self.StartButton.setMinimumSize(QSize(0, 36))

        self.verticalLayout_2.addWidget(self.StartButton)


        self.gridLayout.addWidget(self.centralContainer, 0, 0, 1, 1, Qt.AlignCenter)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Bob Snail", None))
        self.AshanLabel.setText(QCoreApplication.translate("Widget", u"\u0410\u0448\u0430\u043d", None))
        self.AshanButton.setText(QCoreApplication.translate("Widget", u"Edit Config", None))
        self.SilpoLabel.setText(QCoreApplication.translate("Widget", u"\u0421\u0456\u043b\u044c\u043f\u043e", None))
        self.SilpoButton.setText(QCoreApplication.translate("Widget", u"Edit Config", None))
        self.ATBLabel.setText(QCoreApplication.translate("Widget", u"\u0410\u0422\u0411", None))
        self.ATBButton.setText(QCoreApplication.translate("Widget", u"Edit Config", None))
        self.FozzyLabel.setText(QCoreApplication.translate("Widget", u"\u0424\u043e\u0437\u0437\u0456", None))
        self.FozzyButton.setText(QCoreApplication.translate("Widget", u"Edit Config", None))
        self.NovusLabel.setText(QCoreApplication.translate("Widget", u"\u041d\u043e\u0432\u0443\u0441", None))
        self.NovusButton.setText(QCoreApplication.translate("Widget", u"Edit Config", None))
        self.ForaLabel.setText(QCoreApplication.translate("Widget", u"\u0424\u043e\u0440\u0430", None))
        self.ForaButton.setText(QCoreApplication.translate("Widget", u"Edit Config", None))
        self.VarusLabel.setText(QCoreApplication.translate("Widget", u"\u0412\u0430\u0440\u0443\u0441", None))
        self.VarusButton.setText(QCoreApplication.translate("Widget", u"Edit Config", None))
        self.MetroLabel.setText(QCoreApplication.translate("Widget", u"\u041c\u0435\u0442\u0440\u043e", None))
        self.MetroButton.setText(QCoreApplication.translate("Widget", u"Edit Config", None))
        self.TavriaLabel.setText(QCoreApplication.translate("Widget", u"\u0422\u0430\u0432\u0440\u0456\u044f", None))
        self.TavriaButton.setText(QCoreApplication.translate("Widget", u"Edit Config", None))
        self.StartButton.setText(QCoreApplication.translate("Widget", u"Start", None))
    # retranslateUi

