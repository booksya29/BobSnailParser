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
    QProgressBar, QPushButton, QScrollArea, QSizePolicy, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(1920, 1080)
        self.gridLayout = QGridLayout(Widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(Widget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.main = QWidget()
        self.main.setObjectName(u"main")
        self.verticalLayout_2 = QVBoxLayout(self.main)
        self.verticalLayout_2.setSpacing(12)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.AshanLabel = QLabel(Widget)
        self.AshanLabel.setObjectName(u"AshanLabel")
        self.AshanLabel.setMinimumSize(QSize(70, 0))

        self.horizontalLayout.addWidget(self.AshanLabel)

        self.AshanProgressBar = QProgressBar(Widget)
        self.AshanProgressBar.setObjectName(u"AshanProgressBar")
        self.AshanProgressBar.setValue(0)
        self.AshanProgressBar.setTextVisible(True)

        self.horizontalLayout.addWidget(self.AshanProgressBar)

        self.AshanParsingButton = QPushButton(Widget)
        self.AshanParsingButton.setObjectName(u"AshanParsingButton")

        self.horizontalLayout.addWidget(self.AshanParsingButton)

        self.AshanButton = QPushButton(Widget)
        self.AshanButton.setObjectName(u"AshanButton")

        self.horizontalLayout.addWidget(self.AshanButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.SilpoLabel = QLabel(Widget)
        self.SilpoLabel.setObjectName(u"SilpoLabel")
        self.SilpoLabel.setMinimumSize(QSize(70, 0))

        self.horizontalLayout_3.addWidget(self.SilpoLabel)

        self.SilpoProgressBar = QProgressBar(Widget)
        self.SilpoProgressBar.setObjectName(u"SilpoProgressBar")
        self.SilpoProgressBar.setValue(0)
        self.SilpoProgressBar.setTextVisible(True)

        self.horizontalLayout_3.addWidget(self.SilpoProgressBar)

        self.SilpoParsing = QPushButton(Widget)
        self.SilpoParsing.setObjectName(u"SilpoParsing")

        self.horizontalLayout_3.addWidget(self.SilpoParsing)

        self.SilpoButton = QPushButton(Widget)
        self.SilpoButton.setObjectName(u"SilpoButton")

        self.horizontalLayout_3.addWidget(self.SilpoButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.ATBLabel = QLabel(Widget)
        self.ATBLabel.setObjectName(u"ATBLabel")
        self.ATBLabel.setMinimumSize(QSize(70, 0))

        self.horizontalLayout_4.addWidget(self.ATBLabel)

        self.ATBProgressBar = QProgressBar(Widget)
        self.ATBProgressBar.setObjectName(u"ATBProgressBar")
        self.ATBProgressBar.setValue(0)
        self.ATBProgressBar.setTextVisible(True)

        self.horizontalLayout_4.addWidget(self.ATBProgressBar)

        self.ATBParsing = QPushButton(Widget)
        self.ATBParsing.setObjectName(u"ATBParsing")

        self.horizontalLayout_4.addWidget(self.ATBParsing)

        self.ATBButton = QPushButton(Widget)
        self.ATBButton.setObjectName(u"ATBButton")

        self.horizontalLayout_4.addWidget(self.ATBButton)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.FozzyLabel = QLabel(Widget)
        self.FozzyLabel.setObjectName(u"FozzyLabel")
        self.FozzyLabel.setMinimumSize(QSize(70, 0))

        self.horizontalLayout_5.addWidget(self.FozzyLabel)

        self.FozzyProgressBar = QProgressBar(Widget)
        self.FozzyProgressBar.setObjectName(u"FozzyProgressBar")
        self.FozzyProgressBar.setValue(0)
        self.FozzyProgressBar.setTextVisible(True)

        self.horizontalLayout_5.addWidget(self.FozzyProgressBar)

        self.FozzyParsing = QPushButton(Widget)
        self.FozzyParsing.setObjectName(u"FozzyParsing")

        self.horizontalLayout_5.addWidget(self.FozzyParsing)

        self.FozzyButton = QPushButton(Widget)
        self.FozzyButton.setObjectName(u"FozzyButton")

        self.horizontalLayout_5.addWidget(self.FozzyButton)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.NovusLabel = QLabel(Widget)
        self.NovusLabel.setObjectName(u"NovusLabel")
        self.NovusLabel.setMinimumSize(QSize(70, 0))

        self.horizontalLayout_6.addWidget(self.NovusLabel)

        self.NovusProgressBar = QProgressBar(Widget)
        self.NovusProgressBar.setObjectName(u"NovusProgressBar")
        self.NovusProgressBar.setValue(0)
        self.NovusProgressBar.setTextVisible(True)

        self.horizontalLayout_6.addWidget(self.NovusProgressBar)

        self.ParsingNovus = QPushButton(Widget)
        self.ParsingNovus.setObjectName(u"ParsingNovus")

        self.horizontalLayout_6.addWidget(self.ParsingNovus)

        self.NovusButton = QPushButton(Widget)
        self.NovusButton.setObjectName(u"NovusButton")

        self.horizontalLayout_6.addWidget(self.NovusButton)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.ForaLabel = QLabel(Widget)
        self.ForaLabel.setObjectName(u"ForaLabel")
        self.ForaLabel.setMinimumSize(QSize(70, 0))

        self.horizontalLayout_7.addWidget(self.ForaLabel)

        self.ForaProgressBar = QProgressBar(Widget)
        self.ForaProgressBar.setObjectName(u"ForaProgressBar")
        self.ForaProgressBar.setValue(0)
        self.ForaProgressBar.setTextVisible(True)

        self.horizontalLayout_7.addWidget(self.ForaProgressBar)

        self.ForaParsing = QPushButton(Widget)
        self.ForaParsing.setObjectName(u"ForaParsing")

        self.horizontalLayout_7.addWidget(self.ForaParsing)

        self.ForaButton = QPushButton(Widget)
        self.ForaButton.setObjectName(u"ForaButton")

        self.horizontalLayout_7.addWidget(self.ForaButton)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.VarusLabel = QLabel(Widget)
        self.VarusLabel.setObjectName(u"VarusLabel")
        self.VarusLabel.setMinimumSize(QSize(70, 0))

        self.horizontalLayout_8.addWidget(self.VarusLabel)

        self.VarusProgressBar = QProgressBar(Widget)
        self.VarusProgressBar.setObjectName(u"VarusProgressBar")
        self.VarusProgressBar.setValue(0)
        self.VarusProgressBar.setTextVisible(True)

        self.horizontalLayout_8.addWidget(self.VarusProgressBar)

        self.VarusParsing = QPushButton(Widget)
        self.VarusParsing.setObjectName(u"VarusParsing")

        self.horizontalLayout_8.addWidget(self.VarusParsing)

        self.VarusButton = QPushButton(Widget)
        self.VarusButton.setObjectName(u"VarusButton")

        self.horizontalLayout_8.addWidget(self.VarusButton)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.MetroLabel = QLabel(Widget)
        self.MetroLabel.setObjectName(u"MetroLabel")
        self.MetroLabel.setMinimumSize(QSize(70, 0))

        self.horizontalLayout_9.addWidget(self.MetroLabel)

        self.MetroProgressBar = QProgressBar(Widget)
        self.MetroProgressBar.setObjectName(u"MetroProgressBar")
        self.MetroProgressBar.setValue(0)
        self.MetroProgressBar.setTextVisible(True)

        self.horizontalLayout_9.addWidget(self.MetroProgressBar)

        self.MatroParsing = QPushButton(Widget)
        self.MatroParsing.setObjectName(u"MatroParsing")

        self.horizontalLayout_9.addWidget(self.MatroParsing)

        self.MetroButton = QPushButton(Widget)
        self.MetroButton.setObjectName(u"MetroButton")

        self.horizontalLayout_9.addWidget(self.MetroButton)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.TavriaLabel = QLabel(Widget)
        self.TavriaLabel.setObjectName(u"TavriaLabel")
        self.TavriaLabel.setMinimumSize(QSize(70, 0))

        self.horizontalLayout_10.addWidget(self.TavriaLabel)

        self.TavriaProgressBar = QProgressBar(Widget)
        self.TavriaProgressBar.setObjectName(u"TavriaProgressBar")
        self.TavriaProgressBar.setValue(0)
        self.TavriaProgressBar.setTextVisible(True)

        self.horizontalLayout_10.addWidget(self.TavriaProgressBar)

        self.TavriaParsing = QPushButton(Widget)
        self.TavriaParsing.setObjectName(u"TavriaParsing")

        self.horizontalLayout_10.addWidget(self.TavriaParsing)

        self.TavriaButton = QPushButton(Widget)
        self.TavriaButton.setObjectName(u"TavriaButton")

        self.horizontalLayout_10.addWidget(self.TavriaButton)


        self.verticalLayout.addLayout(self.horizontalLayout_10)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.actionsLayout = QHBoxLayout()
        self.actionsLayout.setObjectName(u"actionsLayout")
        self.StartButton = QPushButton(Widget)
        self.StartButton.setObjectName(u"StartButton")
        self.StartButton.setMinimumSize(QSize(0, 36))

        self.actionsLayout.addWidget(self.StartButton)

        self.StopButton = QPushButton(Widget)
        self.StopButton.setObjectName(u"StopButton")
        self.StopButton.setEnabled(False)
        self.StopButton.setMinimumSize(QSize(0, 36))

        self.actionsLayout.addWidget(self.StopButton)


        self.verticalLayout_2.addLayout(self.actionsLayout)

        self.tabWidget.addTab(self.main, "")
        self.new = QWidget()
        self.new.setObjectName(u"new")
        self.verticalLayout_new = QVBoxLayout(self.new)
        self.verticalLayout_new.setSpacing(12)
        self.verticalLayout_new.setObjectName(u"verticalLayout_new")
        self.newScrollArea = QScrollArea(self.new)
        self.newScrollArea.setObjectName(u"newScrollArea")
        self.newScrollArea.setWidgetResizable(True)
        self.newScrollAreaWidgetContents = QWidget()
        self.newScrollAreaWidgetContents.setObjectName(u"newScrollAreaWidgetContents")
        self.verticalLayout_scroll = QVBoxLayout(self.newScrollAreaWidgetContents)
        self.verticalLayout_scroll.setSpacing(8)
        self.verticalLayout_scroll.setObjectName(u"verticalLayout_scroll")
        self.horizontalLayout_dnipro_fozzy = QHBoxLayout()
        self.horizontalLayout_dnipro_fozzy.setObjectName(u"horizontalLayout_dnipro_fozzy")
        self.NewDniproFozzyLabel = QLabel(self.newScrollAreaWidgetContents)
        self.NewDniproFozzyLabel.setObjectName(u"NewDniproFozzyLabel")
        self.NewDniproFozzyLabel.setMinimumSize(QSize(400, 0))
        self.horizontalLayout_dnipro_fozzy.addWidget(self.NewDniproFozzyLabel)

        self.NewDniproFozzyProgressBar = QProgressBar(self.newScrollAreaWidgetContents)
        self.NewDniproFozzyProgressBar.setObjectName(u"NewDniproFozzyProgressBar")
        self.NewDniproFozzyProgressBar.setValue(0)
        self.NewDniproFozzyProgressBar.setTextVisible(True)
        self.horizontalLayout_dnipro_fozzy.addWidget(self.NewDniproFozzyProgressBar)

        self.NewDniproFozzyParsingButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewDniproFozzyParsingButton.setObjectName(u"NewDniproFozzyParsingButton")
        self.horizontalLayout_dnipro_fozzy.addWidget(self.NewDniproFozzyParsingButton)

        self.NewDniproFozzyButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewDniproFozzyButton.setObjectName(u"NewDniproFozzyButton")
        self.horizontalLayout_dnipro_fozzy.addWidget(self.NewDniproFozzyButton)

        self.verticalLayout_scroll.addLayout(self.horizontalLayout_dnipro_fozzy)

        self.horizontalLayout_kyiv_fozzy_zabolotnogo = QHBoxLayout()
        self.horizontalLayout_kyiv_fozzy_zabolotnogo.setObjectName(u"horizontalLayout_kyiv_fozzy_zabolotnogo")
        self.NewKyivFozzyZabolotnogoLabel = QLabel(self.newScrollAreaWidgetContents)
        self.NewKyivFozzyZabolotnogoLabel.setObjectName(u"NewKyivFozzyZabolotnogoLabel")
        self.NewKyivFozzyZabolotnogoLabel.setMinimumSize(QSize(400, 0))
        self.horizontalLayout_kyiv_fozzy_zabolotnogo.addWidget(self.NewKyivFozzyZabolotnogoLabel)

        self.NewKyivFozzyZabolotnogoProgressBar = QProgressBar(self.newScrollAreaWidgetContents)
        self.NewKyivFozzyZabolotnogoProgressBar.setObjectName(u"NewKyivFozzyZabolotnogoProgressBar")
        self.NewKyivFozzyZabolotnogoProgressBar.setValue(0)
        self.NewKyivFozzyZabolotnogoProgressBar.setTextVisible(True)
        self.horizontalLayout_kyiv_fozzy_zabolotnogo.addWidget(self.NewKyivFozzyZabolotnogoProgressBar)

        self.NewKyivFozzyZabolotnogoParsingButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewKyivFozzyZabolotnogoParsingButton.setObjectName(u"NewKyivFozzyZabolotnogoParsingButton")
        self.horizontalLayout_kyiv_fozzy_zabolotnogo.addWidget(self.NewKyivFozzyZabolotnogoParsingButton)

        self.NewKyivFozzyZabolotnogoButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewKyivFozzyZabolotnogoButton.setObjectName(u"NewKyivFozzyZabolotnogoButton")
        self.horizontalLayout_kyiv_fozzy_zabolotnogo.addWidget(self.NewKyivFozzyZabolotnogoButton)

        self.verticalLayout_scroll.addLayout(self.horizontalLayout_kyiv_fozzy_zabolotnogo)

        self.horizontalLayout_ashan_banderu = QHBoxLayout()
        self.horizontalLayout_ashan_banderu.setObjectName(u"horizontalLayout_ashan_banderu")
        self.NewAshanBanderuLabel = QLabel(self.newScrollAreaWidgetContents)
        self.NewAshanBanderuLabel.setObjectName(u"NewAshanBanderuLabel")
        self.NewAshanBanderuLabel.setMinimumSize(QSize(400, 0))
        self.horizontalLayout_ashan_banderu.addWidget(self.NewAshanBanderuLabel)

        self.NewAshanBanderuProgressBar = QProgressBar(self.newScrollAreaWidgetContents)
        self.NewAshanBanderuProgressBar.setObjectName(u"NewAshanBanderuProgressBar")
        self.NewAshanBanderuProgressBar.setValue(0)
        self.NewAshanBanderuProgressBar.setTextVisible(True)
        self.horizontalLayout_ashan_banderu.addWidget(self.NewAshanBanderuProgressBar)

        self.NewAshanBanderuParsingButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewAshanBanderuParsingButton.setObjectName(u"NewAshanBanderuParsingButton")
        self.horizontalLayout_ashan_banderu.addWidget(self.NewAshanBanderuParsingButton)

        self.NewAshanBanderuButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewAshanBanderuButton.setObjectName(u"NewAshanBanderuButton")
        self.horizontalLayout_ashan_banderu.addWidget(self.NewAshanBanderuButton)

        self.verticalLayout_scroll.addLayout(self.horizontalLayout_ashan_banderu)

        self.horizontalLayout_ashan_dnipro = QHBoxLayout()
        self.horizontalLayout_ashan_dnipro.setObjectName(u"horizontalLayout_ashan_dnipro")
        self.NewAshanDniproLabel = QLabel(self.newScrollAreaWidgetContents)
        self.NewAshanDniproLabel.setObjectName(u"NewAshanDniproLabel")
        self.NewAshanDniproLabel.setMinimumSize(QSize(400, 0))
        self.horizontalLayout_ashan_dnipro.addWidget(self.NewAshanDniproLabel)

        self.NewAshanDniproProgressBar = QProgressBar(self.newScrollAreaWidgetContents)
        self.NewAshanDniproProgressBar.setObjectName(u"NewAshanDniproProgressBar")
        self.NewAshanDniproProgressBar.setValue(0)
        self.NewAshanDniproProgressBar.setTextVisible(True)
        self.horizontalLayout_ashan_dnipro.addWidget(self.NewAshanDniproProgressBar)

        self.NewAshanDniproParsingButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewAshanDniproParsingButton.setObjectName(u"NewAshanDniproParsingButton")
        self.horizontalLayout_ashan_dnipro.addWidget(self.NewAshanDniproParsingButton)

        self.NewAshanDniproButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewAshanDniproButton.setObjectName(u"NewAshanDniproButton")
        self.horizontalLayout_ashan_dnipro.addWidget(self.NewAshanDniproButton)

        self.verticalLayout_scroll.addLayout(self.horizontalLayout_ashan_dnipro)

        self.horizontalLayout_lviv_ashan = QHBoxLayout()
        self.horizontalLayout_lviv_ashan.setObjectName(u"horizontalLayout_lviv_ashan")
        self.NewLvivAshanLabel = QLabel(self.newScrollAreaWidgetContents)
        self.NewLvivAshanLabel.setObjectName(u"NewLvivAshanLabel")
        self.NewLvivAshanLabel.setMinimumSize(QSize(400, 0))
        self.horizontalLayout_lviv_ashan.addWidget(self.NewLvivAshanLabel)

        self.NewLvivAshanProgressBar = QProgressBar(self.newScrollAreaWidgetContents)
        self.NewLvivAshanProgressBar.setObjectName(u"NewLvivAshanProgressBar")
        self.NewLvivAshanProgressBar.setValue(0)
        self.NewLvivAshanProgressBar.setTextVisible(True)
        self.horizontalLayout_lviv_ashan.addWidget(self.NewLvivAshanProgressBar)

        self.NewLvivAshanParsingButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewLvivAshanParsingButton.setObjectName(u"NewLvivAshanParsingButton")
        self.horizontalLayout_lviv_ashan.addWidget(self.NewLvivAshanParsingButton)

        self.NewLvivAshanButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewLvivAshanButton.setObjectName(u"NewLvivAshanButton")
        self.horizontalLayout_lviv_ashan.addWidget(self.NewLvivAshanButton)

        self.verticalLayout_scroll.addLayout(self.horizontalLayout_lviv_ashan)

        self.horizontalLayout_odesa_ashan = QHBoxLayout()
        self.horizontalLayout_odesa_ashan.setObjectName(u"horizontalLayout_odesa_ashan")
        self.NewOdesaAshanLabel = QLabel(self.newScrollAreaWidgetContents)
        self.NewOdesaAshanLabel.setObjectName(u"NewOdesaAshanLabel")
        self.NewOdesaAshanLabel.setMinimumSize(QSize(400, 0))
        self.horizontalLayout_odesa_ashan.addWidget(self.NewOdesaAshanLabel)

        self.NewOdesaAshanProgressBar = QProgressBar(self.newScrollAreaWidgetContents)
        self.NewOdesaAshanProgressBar.setObjectName(u"NewOdesaAshanProgressBar")
        self.NewOdesaAshanProgressBar.setValue(0)
        self.NewOdesaAshanProgressBar.setTextVisible(True)
        self.horizontalLayout_odesa_ashan.addWidget(self.NewOdesaAshanProgressBar)

        self.NewOdesaAshanParsingButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewOdesaAshanParsingButton.setObjectName(u"NewOdesaAshanParsingButton")
        self.horizontalLayout_odesa_ashan.addWidget(self.NewOdesaAshanParsingButton)

        self.NewOdesaAshanButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewOdesaAshanButton.setObjectName(u"NewOdesaAshanButton")
        self.horizontalLayout_odesa_ashan.addWidget(self.NewOdesaAshanButton)

        self.verticalLayout_scroll.addLayout(self.horizontalLayout_odesa_ashan)

        self.horizontalLayout_dripro_metro = QHBoxLayout()
        self.horizontalLayout_dripro_metro.setObjectName(u"horizontalLayout_dripro_metro")
        self.NewDniproMetroLabel = QLabel(self.newScrollAreaWidgetContents)
        self.NewDniproMetroLabel.setObjectName(u"NewDniproMetroLabel")
        self.NewDniproMetroLabel.setMinimumSize(QSize(400, 0))
        self.horizontalLayout_dripro_metro.addWidget(self.NewDniproMetroLabel)

        self.NewDniproMetroProgressBar = QProgressBar(self.newScrollAreaWidgetContents)
        self.NewDniproMetroProgressBar.setObjectName(u"NewDniproMetroProgressBar")
        self.NewDniproMetroProgressBar.setValue(0)
        self.NewDniproMetroProgressBar.setTextVisible(True)
        self.horizontalLayout_dripro_metro.addWidget(self.NewDniproMetroProgressBar)

        self.NewDniproMetroParsingButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewDniproMetroParsingButton.setObjectName(u"NewDniproMetroParsingButton")
        self.horizontalLayout_dripro_metro.addWidget(self.NewDniproMetroParsingButton)

        self.NewDniproMetroButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewDniproMetroButton.setObjectName(u"NewDniproMetroButton")
        self.horizontalLayout_dripro_metro.addWidget(self.NewDniproMetroButton)

        self.verticalLayout_scroll.addLayout(self.horizontalLayout_dripro_metro)

        self.horizontalLayout_lviv_metro = QHBoxLayout()
        self.horizontalLayout_lviv_metro.setObjectName(u"horizontalLayout_lviv_metro")
        self.NewLvivMetroLabel = QLabel(self.newScrollAreaWidgetContents)
        self.NewLvivMetroLabel.setObjectName(u"NewLvivMetroLabel")
        self.NewLvivMetroLabel.setMinimumSize(QSize(400, 0))
        self.horizontalLayout_lviv_metro.addWidget(self.NewLvivMetroLabel)

        self.NewLvivMetroProgressBar = QProgressBar(self.newScrollAreaWidgetContents)
        self.NewLvivMetroProgressBar.setObjectName(u"NewLvivMetroProgressBar")
        self.NewLvivMetroProgressBar.setValue(0)
        self.NewLvivMetroProgressBar.setTextVisible(True)
        self.horizontalLayout_lviv_metro.addWidget(self.NewLvivMetroProgressBar)

        self.NewLvivMetroParsingButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewLvivMetroParsingButton.setObjectName(u"NewLvivMetroParsingButton")
        self.horizontalLayout_lviv_metro.addWidget(self.NewLvivMetroParsingButton)

        self.NewLvivMetroButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewLvivMetroButton.setObjectName(u"NewLvivMetroButton")
        self.horizontalLayout_lviv_metro.addWidget(self.NewLvivMetroButton)

        self.verticalLayout_scroll.addLayout(self.horizontalLayout_lviv_metro)

        self.horizontalLayout_odesa_metro = QHBoxLayout()
        self.horizontalLayout_odesa_metro.setObjectName(u"horizontalLayout_odesa_metro")
        self.NewOdesaMetroLabel = QLabel(self.newScrollAreaWidgetContents)
        self.NewOdesaMetroLabel.setObjectName(u"NewOdesaMetroLabel")
        self.NewOdesaMetroLabel.setMinimumSize(QSize(400, 0))
        self.horizontalLayout_odesa_metro.addWidget(self.NewOdesaMetroLabel)

        self.NewOdesaMetroProgressBar = QProgressBar(self.newScrollAreaWidgetContents)
        self.NewOdesaMetroProgressBar.setObjectName(u"NewOdesaMetroProgressBar")
        self.NewOdesaMetroProgressBar.setValue(0)
        self.NewOdesaMetroProgressBar.setTextVisible(True)
        self.horizontalLayout_odesa_metro.addWidget(self.NewOdesaMetroProgressBar)

        self.NewOdesaMetroParsingButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewOdesaMetroParsingButton.setObjectName(u"NewOdesaMetroParsingButton")
        self.horizontalLayout_odesa_metro.addWidget(self.NewOdesaMetroParsingButton)

        self.NewOdesaMetroButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewOdesaMetroButton.setObjectName(u"NewOdesaMetroButton")
        self.horizontalLayout_odesa_metro.addWidget(self.NewOdesaMetroButton)

        self.verticalLayout_scroll.addLayout(self.horizontalLayout_odesa_metro)

        self.horizontalLayout_kyiv_metro = QHBoxLayout()
        self.horizontalLayout_kyiv_metro.setObjectName(u"horizontalLayout_kyiv_metro")
        self.NewKyivMetroLabel = QLabel(self.newScrollAreaWidgetContents)
        self.NewKyivMetroLabel.setObjectName(u"NewKyivMetroLabel")
        self.NewKyivMetroLabel.setMinimumSize(QSize(400, 0))
        self.horizontalLayout_kyiv_metro.addWidget(self.NewKyivMetroLabel)

        self.NewKyivMetroProgressBar = QProgressBar(self.newScrollAreaWidgetContents)
        self.NewKyivMetroProgressBar.setObjectName(u"NewKyivMetroProgressBar")
        self.NewKyivMetroProgressBar.setValue(0)
        self.NewKyivMetroProgressBar.setTextVisible(True)
        self.horizontalLayout_kyiv_metro.addWidget(self.NewKyivMetroProgressBar)

        self.NewKyivMetroParsingButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewKyivMetroParsingButton.setObjectName(u"NewKyivMetroParsingButton")
        self.horizontalLayout_kyiv_metro.addWidget(self.NewKyivMetroParsingButton)

        self.NewKyivMetroButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewKyivMetroButton.setObjectName(u"NewKyivMetroButton")
        self.horizontalLayout_kyiv_metro.addWidget(self.NewKyivMetroButton)

        self.verticalLayout_scroll.addLayout(self.horizontalLayout_kyiv_metro)

        self.horizontalLayout_kharkiv_metro = QHBoxLayout()
        self.horizontalLayout_kharkiv_metro.setObjectName(u"horizontalLayout_kharkiv_metro")
        self.NewKharkivMetroLabel = QLabel(self.newScrollAreaWidgetContents)
        self.NewKharkivMetroLabel.setObjectName(u"NewKharkivMetroLabel")
        self.NewKharkivMetroLabel.setMinimumSize(QSize(400, 0))
        self.horizontalLayout_kharkiv_metro.addWidget(self.NewKharkivMetroLabel)

        self.NewKharkivMetroProgressBar = QProgressBar(self.newScrollAreaWidgetContents)
        self.NewKharkivMetroProgressBar.setObjectName(u"NewKharkivMetroProgressBar")
        self.NewKharkivMetroProgressBar.setValue(0)
        self.NewKharkivMetroProgressBar.setTextVisible(True)
        self.horizontalLayout_kharkiv_metro.addWidget(self.NewKharkivMetroProgressBar)

        self.NewKharkivMetroParsingButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewKharkivMetroParsingButton.setObjectName(u"NewKharkivMetroParsingButton")
        self.horizontalLayout_kharkiv_metro.addWidget(self.NewKharkivMetroParsingButton)

        self.NewKharkivMetroButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewKharkivMetroButton.setObjectName(u"NewKharkivMetroButton")
        self.horizontalLayout_kharkiv_metro.addWidget(self.NewKharkivMetroButton)

        self.verticalLayout_scroll.addLayout(self.horizontalLayout_kharkiv_metro)

        self.horizontalLayout_kyiv_novus_zdolbunivska = QHBoxLayout()
        self.horizontalLayout_kyiv_novus_zdolbunivska.setObjectName(u"horizontalLayout_kyiv_novus_zdolbunivska")
        self.NewKyivNovusZdolbunivskaLabel = QLabel(self.newScrollAreaWidgetContents)
        self.NewKyivNovusZdolbunivskaLabel.setObjectName(u"NewKyivNovusZdolbunivskaLabel")
        self.NewKyivNovusZdolbunivskaLabel.setMinimumSize(QSize(400, 0))
        self.horizontalLayout_kyiv_novus_zdolbunivska.addWidget(self.NewKyivNovusZdolbunivskaLabel)

        self.NewKyivNovusZdolbunivskaProgressBar = QProgressBar(self.newScrollAreaWidgetContents)
        self.NewKyivNovusZdolbunivskaProgressBar.setObjectName(u"NewKyivNovusZdolbunivskaProgressBar")
        self.NewKyivNovusZdolbunivskaProgressBar.setValue(0)
        self.NewKyivNovusZdolbunivskaProgressBar.setTextVisible(True)
        self.horizontalLayout_kyiv_novus_zdolbunivska.addWidget(self.NewKyivNovusZdolbunivskaProgressBar)

        self.NewKyivNovusZdolbunivskaParsingButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewKyivNovusZdolbunivskaParsingButton.setObjectName(u"NewKyivNovusZdolbunivskaParsingButton")
        self.horizontalLayout_kyiv_novus_zdolbunivska.addWidget(self.NewKyivNovusZdolbunivskaParsingButton)

        self.NewKyivNovusZdolbunivskaButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewKyivNovusZdolbunivskaButton.setObjectName(u"NewKyivNovusZdolbunivskaButton")
        self.horizontalLayout_kyiv_novus_zdolbunivska.addWidget(self.NewKyivNovusZdolbunivskaButton)

        self.verticalLayout_scroll.addLayout(self.horizontalLayout_kyiv_novus_zdolbunivska)

        self.horizontalLayout_kyiv_varus_malushka = QHBoxLayout()
        self.horizontalLayout_kyiv_varus_malushka.setObjectName(u"horizontalLayout_kyiv_varus_malushka")
        self.NewKyivVarusMalushkaLabel = QLabel(self.newScrollAreaWidgetContents)
        self.NewKyivVarusMalushkaLabel.setObjectName(u"NewKyivVarusMalushkaLabel")
        self.NewKyivVarusMalushkaLabel.setMinimumSize(QSize(400, 0))
        self.horizontalLayout_kyiv_varus_malushka.addWidget(self.NewKyivVarusMalushkaLabel)

        self.NewKyivVarusMalushkaProgressBar = QProgressBar(self.newScrollAreaWidgetContents)
        self.NewKyivVarusMalushkaProgressBar.setObjectName(u"NewKyivVarusMalushkaProgressBar")
        self.NewKyivVarusMalushkaProgressBar.setValue(0)
        self.NewKyivVarusMalushkaProgressBar.setTextVisible(True)
        self.horizontalLayout_kyiv_varus_malushka.addWidget(self.NewKyivVarusMalushkaProgressBar)

        self.NewKyivVarusMalushkaParsingButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewKyivVarusMalushkaParsingButton.setObjectName(u"NewKyivVarusMalushkaParsingButton")
        self.horizontalLayout_kyiv_varus_malushka.addWidget(self.NewKyivVarusMalushkaParsingButton)

        self.NewKyivVarusMalushkaButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewKyivVarusMalushkaButton.setObjectName(u"NewKyivVarusMalushkaButton")
        self.horizontalLayout_kyiv_varus_malushka.addWidget(self.NewKyivVarusMalushkaButton)

        self.verticalLayout_scroll.addLayout(self.horizontalLayout_kyiv_varus_malushka)

        self.horizontalLayout_dnipro_varus_panikahi = QHBoxLayout()
        self.horizontalLayout_dnipro_varus_panikahi.setObjectName(u"horizontalLayout_dnipro_varus_panikahi")
        self.NewDniproVarusPanikahiLabel = QLabel(self.newScrollAreaWidgetContents)
        self.NewDniproVarusPanikahiLabel.setObjectName(u"NewDniproVarusPanikahiLabel")
        self.NewDniproVarusPanikahiLabel.setMinimumSize(QSize(400, 0))
        self.horizontalLayout_dnipro_varus_panikahi.addWidget(self.NewDniproVarusPanikahiLabel)

        self.NewDniproVarusPanikahiProgressBar = QProgressBar(self.newScrollAreaWidgetContents)
        self.NewDniproVarusPanikahiProgressBar.setObjectName(u"NewDniproVarusPanikahiProgressBar")
        self.NewDniproVarusPanikahiProgressBar.setValue(0)
        self.NewDniproVarusPanikahiProgressBar.setTextVisible(True)
        self.horizontalLayout_dnipro_varus_panikahi.addWidget(self.NewDniproVarusPanikahiProgressBar)

        self.NewDniproVarusPanikahiParsingButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewDniproVarusPanikahiParsingButton.setObjectName(u"NewDniproVarusPanikahiParsingButton")
        self.horizontalLayout_dnipro_varus_panikahi.addWidget(self.NewDniproVarusPanikahiParsingButton)

        self.NewDniproVarusPanikahiButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewDniproVarusPanikahiButton.setObjectName(u"NewDniproVarusPanikahiButton")
        self.horizontalLayout_dnipro_varus_panikahi.addWidget(self.NewDniproVarusPanikahiButton)

        self.verticalLayout_scroll.addLayout(self.horizontalLayout_dnipro_varus_panikahi)

        self.horizontalLayout_dnipro_atb_zoryanuy = QHBoxLayout()
        self.horizontalLayout_dnipro_atb_zoryanuy.setObjectName(u"horizontalLayout_dnipro_atb_zoryanuy")
        self.NewDniproAtbZoryanuyLabel = QLabel(self.newScrollAreaWidgetContents)
        self.NewDniproAtbZoryanuyLabel.setObjectName(u"NewDniproAtbZoryanuyLabel")
        self.NewDniproAtbZoryanuyLabel.setMinimumSize(QSize(400, 0))
        self.horizontalLayout_dnipro_atb_zoryanuy.addWidget(self.NewDniproAtbZoryanuyLabel)

        self.NewDniproAtbZoryanuyProgressBar = QProgressBar(self.newScrollAreaWidgetContents)
        self.NewDniproAtbZoryanuyProgressBar.setObjectName(u"NewDniproAtbZoryanuyProgressBar")
        self.NewDniproAtbZoryanuyProgressBar.setValue(0)
        self.NewDniproAtbZoryanuyProgressBar.setTextVisible(True)
        self.horizontalLayout_dnipro_atb_zoryanuy.addWidget(self.NewDniproAtbZoryanuyProgressBar)

        self.NewDniproAtbZoryanuyParsingButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewDniproAtbZoryanuyParsingButton.setObjectName(u"NewDniproAtbZoryanuyParsingButton")
        self.horizontalLayout_dnipro_atb_zoryanuy.addWidget(self.NewDniproAtbZoryanuyParsingButton)

        self.NewDniproAtbZoryanuyButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewDniproAtbZoryanuyButton.setObjectName(u"NewDniproAtbZoryanuyButton")
        self.horizontalLayout_dnipro_atb_zoryanuy.addWidget(self.NewDniproAtbZoryanuyButton)

        self.verticalLayout_scroll.addLayout(self.horizontalLayout_dnipro_atb_zoryanuy)

        self.horizontalLayout_kyiv_atb_rudnutskogo = QHBoxLayout()
        self.horizontalLayout_kyiv_atb_rudnutskogo.setObjectName(u"horizontalLayout_kyiv_atb_rudnutskogo")
        self.NewKyivAtbRudnutskogoLabel = QLabel(self.newScrollAreaWidgetContents)
        self.NewKyivAtbRudnutskogoLabel.setObjectName(u"NewKyivAtbRudnutskogoLabel")
        self.NewKyivAtbRudnutskogoLabel.setMinimumSize(QSize(400, 0))
        self.horizontalLayout_kyiv_atb_rudnutskogo.addWidget(self.NewKyivAtbRudnutskogoLabel)

        self.NewKyivAtbRudnutskogoProgressBar = QProgressBar(self.newScrollAreaWidgetContents)
        self.NewKyivAtbRudnutskogoProgressBar.setObjectName(u"NewKyivAtbRudnutskogoProgressBar")
        self.NewKyivAtbRudnutskogoProgressBar.setValue(0)
        self.NewKyivAtbRudnutskogoProgressBar.setTextVisible(True)
        self.horizontalLayout_kyiv_atb_rudnutskogo.addWidget(self.NewKyivAtbRudnutskogoProgressBar)

        self.NewKyivAtbRudnutskogoParsingButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewKyivAtbRudnutskogoParsingButton.setObjectName(u"NewKyivAtbRudnutskogoParsingButton")
        self.horizontalLayout_kyiv_atb_rudnutskogo.addWidget(self.NewKyivAtbRudnutskogoParsingButton)

        self.NewKyivAtbRudnutskogoButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewKyivAtbRudnutskogoButton.setObjectName(u"NewKyivAtbRudnutskogoButton")
        self.horizontalLayout_kyiv_atb_rudnutskogo.addWidget(self.NewKyivAtbRudnutskogoButton)

        self.verticalLayout_scroll.addLayout(self.horizontalLayout_kyiv_atb_rudnutskogo)

        self.horizontalLayout_kyiv_silpo_beresteyski = QHBoxLayout()
        self.horizontalLayout_kyiv_silpo_beresteyski.setObjectName(u"horizontalLayout_kyiv_silpo_beresteyski")
        self.NewKyivSilpoBeresteyskiLabel = QLabel(self.newScrollAreaWidgetContents)
        self.NewKyivSilpoBeresteyskiLabel.setObjectName(u"NewKyivSilpoBeresteyskiLabel")
        self.NewKyivSilpoBeresteyskiLabel.setMinimumSize(QSize(400, 0))
        self.horizontalLayout_kyiv_silpo_beresteyski.addWidget(self.NewKyivSilpoBeresteyskiLabel)

        self.NewKyivSilpoBeresteyskiProgressBar = QProgressBar(self.newScrollAreaWidgetContents)
        self.NewKyivSilpoBeresteyskiProgressBar.setObjectName(u"NewKyivSilpoBeresteyskiProgressBar")
        self.NewKyivSilpoBeresteyskiProgressBar.setValue(0)
        self.NewKyivSilpoBeresteyskiProgressBar.setTextVisible(True)
        self.horizontalLayout_kyiv_silpo_beresteyski.addWidget(self.NewKyivSilpoBeresteyskiProgressBar)

        self.NewKyivSilpoBeresteyskiParsingButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewKyivSilpoBeresteyskiParsingButton.setObjectName(u"NewKyivSilpoBeresteyskiParsingButton")
        self.horizontalLayout_kyiv_silpo_beresteyski.addWidget(self.NewKyivSilpoBeresteyskiParsingButton)

        self.NewKyivSilpoBeresteyskiButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewKyivSilpoBeresteyskiButton.setObjectName(u"NewKyivSilpoBeresteyskiButton")
        self.horizontalLayout_kyiv_silpo_beresteyski.addWidget(self.NewKyivSilpoBeresteyskiButton)

        self.verticalLayout_scroll.addLayout(self.horizontalLayout_kyiv_silpo_beresteyski)

        self.horizontalLayout_dnipro_silpo_novokrumskiy = QHBoxLayout()
        self.horizontalLayout_dnipro_silpo_novokrumskiy.setObjectName(u"horizontalLayout_dnipro_silpo_novokrumskiy")
        self.NewDniproSilpoNovokrumskiyLabel = QLabel(self.newScrollAreaWidgetContents)
        self.NewDniproSilpoNovokrumskiyLabel.setObjectName(u"NewDniproSilpoNovokrumskiyLabel")
        self.NewDniproSilpoNovokrumskiyLabel.setMinimumSize(QSize(400, 0))
        self.horizontalLayout_dnipro_silpo_novokrumskiy.addWidget(self.NewDniproSilpoNovokrumskiyLabel)

        self.NewDniproSilpoNovokrumskiyProgressBar = QProgressBar(self.newScrollAreaWidgetContents)
        self.NewDniproSilpoNovokrumskiyProgressBar.setObjectName(u"NewDniproSilpoNovokrumskiyProgressBar")
        self.NewDniproSilpoNovokrumskiyProgressBar.setValue(0)
        self.NewDniproSilpoNovokrumskiyProgressBar.setTextVisible(True)
        self.horizontalLayout_dnipro_silpo_novokrumskiy.addWidget(self.NewDniproSilpoNovokrumskiyProgressBar)

        self.NewDniproSilpoNovokrumskiyParsingButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewDniproSilpoNovokrumskiyParsingButton.setObjectName(u"NewDniproSilpoNovokrumskiyParsingButton")
        self.horizontalLayout_dnipro_silpo_novokrumskiy.addWidget(self.NewDniproSilpoNovokrumskiyParsingButton)

        self.NewDniproSilpoNovokrumskiyButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewDniproSilpoNovokrumskiyButton.setObjectName(u"NewDniproSilpoNovokrumskiyButton")
        self.horizontalLayout_dnipro_silpo_novokrumskiy.addWidget(self.NewDniproSilpoNovokrumskiyButton)

        self.verticalLayout_scroll.addLayout(self.horizontalLayout_dnipro_silpo_novokrumskiy)

        self.horizontalLayout_lviv_silpo_kulparivska = QHBoxLayout()
        self.horizontalLayout_lviv_silpo_kulparivska.setObjectName(u"horizontalLayout_lviv_silpo_kulparivska")
        self.NewLvivSilpoKulparivskaLabel = QLabel(self.newScrollAreaWidgetContents)
        self.NewLvivSilpoKulparivskaLabel.setObjectName(u"NewLvivSilpoKulparivskaLabel")
        self.NewLvivSilpoKulparivskaLabel.setMinimumSize(QSize(400, 0))
        self.horizontalLayout_lviv_silpo_kulparivska.addWidget(self.NewLvivSilpoKulparivskaLabel)

        self.NewLvivSilpoKulparivskaProgressBar = QProgressBar(self.newScrollAreaWidgetContents)
        self.NewLvivSilpoKulparivskaProgressBar.setObjectName(u"NewLvivSilpoKulparivskaProgressBar")
        self.NewLvivSilpoKulparivskaProgressBar.setValue(0)
        self.NewLvivSilpoKulparivskaProgressBar.setTextVisible(True)
        self.horizontalLayout_lviv_silpo_kulparivska.addWidget(self.NewLvivSilpoKulparivskaProgressBar)

        self.NewLvivSilpoKulparivskaParsingButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewLvivSilpoKulparivskaParsingButton.setObjectName(u"NewLvivSilpoKulparivskaParsingButton")
        self.horizontalLayout_lviv_silpo_kulparivska.addWidget(self.NewLvivSilpoKulparivskaParsingButton)

        self.NewLvivSilpoKulparivskaButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewLvivSilpoKulparivskaButton.setObjectName(u"NewLvivSilpoKulparivskaButton")
        self.horizontalLayout_lviv_silpo_kulparivska.addWidget(self.NewLvivSilpoKulparivskaButton)

        self.verticalLayout_scroll.addLayout(self.horizontalLayout_lviv_silpo_kulparivska)

        self.horizontalLayout_kyiv_fora_berest = QHBoxLayout()
        self.horizontalLayout_kyiv_fora_berest.setObjectName(u"horizontalLayout_kyiv_fora_berest")
        self.NewKyivForaBerestLabel = QLabel(self.newScrollAreaWidgetContents)
        self.NewKyivForaBerestLabel.setObjectName(u"NewKyivForaBerestLabel")
        self.NewKyivForaBerestLabel.setMinimumSize(QSize(400, 0))
        self.horizontalLayout_kyiv_fora_berest.addWidget(self.NewKyivForaBerestLabel)

        self.NewKyivForaBerestProgressBar = QProgressBar(self.newScrollAreaWidgetContents)
        self.NewKyivForaBerestProgressBar.setObjectName(u"NewKyivForaBerestProgressBar")
        self.NewKyivForaBerestProgressBar.setValue(0)
        self.NewKyivForaBerestProgressBar.setTextVisible(True)
        self.horizontalLayout_kyiv_fora_berest.addWidget(self.NewKyivForaBerestProgressBar)

        self.NewKyivForaBerestParsingButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewKyivForaBerestParsingButton.setObjectName(u"NewKyivForaBerestParsingButton")
        self.horizontalLayout_kyiv_fora_berest.addWidget(self.NewKyivForaBerestParsingButton)

        self.NewKyivForaBerestButton = QPushButton(self.newScrollAreaWidgetContents)
        self.NewKyivForaBerestButton.setObjectName(u"NewKyivForaBerestButton")
        self.horizontalLayout_kyiv_fora_berest.addWidget(self.NewKyivForaBerestButton)

        self.verticalLayout_scroll.addLayout(self.horizontalLayout_kyiv_fora_berest)

        self.newScrollArea.setWidget(self.newScrollAreaWidgetContents)
        self.verticalLayout_new.addWidget(self.newScrollArea)

        self.newActionsLayout = QHBoxLayout()
        self.newActionsLayout.setObjectName(u"newActionsLayout")
        self.NewStartButton = QPushButton(self.new)
        self.NewStartButton.setObjectName(u"NewStartButton")
        self.NewStartButton.setMinimumSize(QSize(0, 36))
        self.newActionsLayout.addWidget(self.NewStartButton)

        self.NewStopButton = QPushButton(self.new)
        self.NewStopButton.setObjectName(u"NewStopButton")
        self.NewStopButton.setEnabled(False)
        self.NewStopButton.setMinimumSize(QSize(0, 36))
        self.newActionsLayout.addWidget(self.NewStopButton)

        self.verticalLayout_new.addLayout(self.newActionsLayout)

        self.tabWidget.addTab(self.new, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        # Aliases
        self.tab_main = self.main
        self.main_tab = self.main
        self.tab_new = self.new
        self.new_tab = self.new

        self.retranslateUi(Widget)

        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Bob Snail", None))
        self.AshanLabel.setText(QCoreApplication.translate("Widget", u"\u0410\u0448\u0430\u043d", None))
        self.AshanParsingButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.AshanButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.SilpoLabel.setText(QCoreApplication.translate("Widget", u"\u0421\u0456\u043b\u044c\u043f\u043e", None))
        self.SilpoParsing.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.SilpoButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.ATBLabel.setText(QCoreApplication.translate("Widget", u"\u0410\u0422\u0411", None))
        self.ATBParsing.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.ATBButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.FozzyLabel.setText(QCoreApplication.translate("Widget", u"\u0424\u043e\u0437\u0437\u0456", None))
        self.FozzyParsing.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.FozzyButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.NovusLabel.setText(QCoreApplication.translate("Widget", u"\u041d\u043e\u0432\u0443\u0441", None))
        self.ParsingNovus.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.NovusButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.ForaLabel.setText(QCoreApplication.translate("Widget", u"\u0424\u043e\u0440\u0430", None))
        self.ForaParsing.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.ForaButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.VarusLabel.setText(QCoreApplication.translate("Widget", u"\u0412\u0430\u0440\u0443\u0441", None))
        self.VarusParsing.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.VarusButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.MetroLabel.setText(QCoreApplication.translate("Widget", u"\u041c\u0435\u0442\u0440\u043e", None))
        self.MatroParsing.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.MetroButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.TavriaLabel.setText(QCoreApplication.translate("Widget", u"\u0422\u0430\u0432\u0440\u0456\u044f", None))
        self.TavriaParsing.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.TavriaButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.StartButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.StopButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u043e\u043f", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.main), QCoreApplication.translate("Widget", u"main", None))
        self.NewDniproFozzyLabel.setText(QCoreApplication.translate("Widget", u"Fozzy Дніпро", None))
        self.NewDniproFozzyParsingButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.NewDniproFozzyButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.NewKyivFozzyZabolotnogoLabel.setText(QCoreApplication.translate("Widget", u"Fozzy Київ", None))
        self.NewKyivFozzyZabolotnogoParsingButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.NewKyivFozzyZabolotnogoButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.NewAshanBanderuLabel.setText(QCoreApplication.translate("Widget", u"Auchan Київ", None))
        self.NewAshanBanderuParsingButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.NewAshanBanderuButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.NewAshanDniproLabel.setText(QCoreApplication.translate("Widget", u"Auchan Дніпро", None))
        self.NewAshanDniproParsingButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.NewAshanDniproButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.NewLvivAshanLabel.setText(QCoreApplication.translate("Widget", u"Auchan Львів", None))
        self.NewLvivAshanParsingButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.NewLvivAshanButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.NewOdesaAshanLabel.setText(QCoreApplication.translate("Widget", u"Auchan Одеса", None))
        self.NewOdesaAshanParsingButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.NewOdesaAshanButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.NewDniproMetroLabel.setText(QCoreApplication.translate("Widget", u"Metro Дніпро", None))
        self.NewDniproMetroParsingButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.NewDniproMetroButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.NewLvivMetroLabel.setText(QCoreApplication.translate("Widget", u"Metro Львів", None))
        self.NewLvivMetroParsingButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.NewLvivMetroButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.NewOdesaMetroLabel.setText(QCoreApplication.translate("Widget", u"Metro Одеса", None))
        self.NewOdesaMetroParsingButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.NewOdesaMetroButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.NewKyivMetroLabel.setText(QCoreApplication.translate("Widget", u"Metro Київ", None))
        self.NewKyivMetroParsingButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.NewKyivMetroButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.NewKharkivMetroLabel.setText(QCoreApplication.translate("Widget", u"Metro Харків", None))
        self.NewKharkivMetroParsingButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.NewKharkivMetroButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.NewKyivNovusZdolbunivskaLabel.setText(QCoreApplication.translate("Widget", u"Novus Київ", None))
        self.NewKyivNovusZdolbunivskaParsingButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.NewKyivNovusZdolbunivskaButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.NewKyivVarusMalushkaLabel.setText(QCoreApplication.translate("Widget", u"Varus Київ", None))
        self.NewKyivVarusMalushkaParsingButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.NewKyivVarusMalushkaButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.NewDniproVarusPanikahiLabel.setText(QCoreApplication.translate("Widget", u"Varus Дніпро", None))
        self.NewDniproVarusPanikahiParsingButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.NewDniproVarusPanikahiButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.NewDniproAtbZoryanuyLabel.setText(QCoreApplication.translate("Widget", u"АТБ Дніпро", None))
        self.NewDniproAtbZoryanuyParsingButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.NewDniproAtbZoryanuyButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.NewKyivAtbRudnutskogoLabel.setText(QCoreApplication.translate("Widget", u"АТБ Київ", None))
        self.NewKyivAtbRudnutskogoParsingButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.NewKyivAtbRudnutskogoButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.NewKyivSilpoBeresteyskiLabel.setText(QCoreApplication.translate("Widget", u"Сільпо Київ", None))
        self.NewKyivSilpoBeresteyskiParsingButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.NewKyivSilpoBeresteyskiButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.NewDniproSilpoNovokrumskiyLabel.setText(QCoreApplication.translate("Widget", u"Сільпо Дніпро", None))
        self.NewDniproSilpoNovokrumskiyParsingButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.NewDniproSilpoNovokrumskiyButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.NewLvivSilpoKulparivskaLabel.setText(QCoreApplication.translate("Widget", u"Сільпо Львів", None))
        self.NewLvivSilpoKulparivskaParsingButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.NewLvivSilpoKulparivskaButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.NewKyivForaBerestLabel.setText(QCoreApplication.translate("Widget", u"Фора Київ", None))
        self.NewKyivForaBerestParsingButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.NewKyivForaBerestButton.setText(QCoreApplication.translate("Widget", u"\u0412\u0456\u0434\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0444\u0456\u0433", None))
        self.NewStartButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.NewStopButton.setText(QCoreApplication.translate("Widget", u"\u0421\u0442\u043e\u043f", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.new), QCoreApplication.translate("Widget", u"new", None))
    # retranslateUi

