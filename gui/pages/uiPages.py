# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pagesKFkFzx.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from library import *
from gui.Widgest.sliderValue import PySlider
from gui.Widgest.checkBox import PyToggle

class Ui_StackedWidget(object):
    def setupUi(self, StackedWidget):
        if not StackedWidget.objectName():
            StackedWidget.setObjectName(u"StackedWidget")
        StackedWidget.setMaximumWidth(150)
        StackedWidget.setMinimumWidth(150)

        #CREAT PAGE ONE
        self.pageOne = QWidget()
        self.pageOne.setObjectName(u"page1")
        self.pageOne.setMinimumWidth(150)
        self.pageOne.setMaximumWidth(150)

        #CREATE LAYOUT FOR PAGE ONE
        self.verticalLayout = QVBoxLayout(self.pageOne)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0,0,0,0)

        #LEFT MENU SPACING
        self.leftMenuSpacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        #INSERT LABEL DETECTION MODE
        self.labelMode = QLabel("Modo de detecção:")
        self.verticalLayout.addWidget(self.labelMode)

        #INSERT MENU COMBOBOX MODE
        self.comboboxMode = QComboBox()
        self.comboboxMode.setStyleSheet("""
                    QComboBox {
                        background-color: #2B2D31;
                        color: white;
                        border: 1px solid #505050;
                        border-radius: 4px;
                        padding: 3px;
                        font-size: 12px;
                    }

                    QComboBox QAbstractItemView {
                        background-color: #2B2D31;
                        border: 1px solid #505050;
                        selection-background-color: #505050;
                        color: white;
                    }
                """)
        self.comboboxMode.addItems(['Desativado','Caixa aberta'])
        self.verticalLayout.addWidget(self.comboboxMode)

        #INSERT LABEL BRIGHTNESS
        self.labelBrightness = QLabel("Brilho")
        self.verticalLayout.addWidget(self.labelBrightness)
        self.sliderBrightness = PySlider()
        self.verticalLayout.addWidget(self.sliderBrightness)

        #INSERT LABEL CONTRAST
        self.labelContrast = QLabel("Contraste")
        self.verticalLayout.addWidget(self.labelContrast)
        self.sliderContrast = PySlider()
        self.verticalLayout.addWidget(self.sliderContrast)

        #INSERT LABEL SUPER RESOLUTION SCALE
        self.labelThree = QLabel("Escala de super resolução:")
        self.verticalLayout.addWidget(self.labelThree)

        #INSERT COMBOBOX SUPER RESOLUTION
        self.comboboxSR = QComboBox()
        self.comboboxSR.setStyleSheet("""
                    QComboBox {
                        background-color: #2B2D31;
                        color: white;
                        border: 1px solid #505050;
                        border-radius: 4px;
                        padding: 3px;
                        font-size: 12px;
                    }

                    QComboBox QAbstractItemView {
                        background-color: #2B2D31;
                        border: 1px solid #505050;
                        selection-background-color: #505050;
                        color: white;
                    }
                """)
        self.comboboxSR.addItems(['Desativado', 'ESPCN_x2.pb', 'ESPCN_x3.pb', 'ESPCN_x4.pb'])
        self.verticalLayout.addWidget(self.comboboxSR)
        
        #INSERT LABEL SHARPNESS
        self.labelSharpness = QLabel("Nitidez")
        self.verticalLayout.addWidget(self.labelSharpness)

        #INSERT SWITCH SHARPNESS
        self.switchSharpness = PyToggle()
        self.verticalLayout.addWidget(self.switchSharpness)

        #INSERT LABEL HISTOGRAM EQUALIZATION
        self.labelHistogram = QLabel("Equalização de Histograma")
        self.verticalLayout.addWidget(self.labelHistogram)

        #INSERT SWITCH HISTOGRAM EQUALIZATION
        self.switchHistogram = PyToggle()
        self.verticalLayout.addWidget(self.switchHistogram)

        #INSERT LABEL LOW PASS FILTER
        self.labelLowPass = QLabel("Filtro Passa-Baixa")
        self.verticalLayout.addWidget(self.labelLowPass)

        #INSERT SWITCH LOW PASS FILTER
        self.switchLowPass = PyToggle()
        self.verticalLayout.addWidget(self.switchLowPass)

        #INSERT LABEL MEDIAN FILTER
        self.labelMedian = QLabel("Filtro Mediana")
        self.verticalLayout.addWidget(self.labelMedian)

        #INSERT SWITCH MEDIAN FILTER
        self.switchMedian = PyToggle()
        self.verticalLayout.addWidget(self.switchMedian)

        self.verticalLayout.addItem(self.leftMenuSpacing)
        StackedWidget.addWidget(self.pageOne)
        self.retranslateUi(StackedWidget)
        QMetaObject.connectSlotsByName(StackedWidget)

    def retranslateUi(self, StackedWidget):
        StackedWidget.setWindowTitle(QCoreApplication.translate("StackedWidget", u"StackedWidget", None))