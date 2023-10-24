# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pagesKFkFzx.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qt_core import *
from gui.widgest.py_push_button import PyPushButton
from gui.widgest.py_Slider import PySlider
from gui.widgest.py_check_box import PyToggle

class Ui_StackedWidget(object):
    def setupUi(self, StackedWidget):
        if not StackedWidget.objectName():
            StackedWidget.setObjectName(u"StackedWidget")
        StackedWidget.setMaximumWidth(150)
        StackedWidget.setMinimumWidth(150)

        #CREAT PAGE1
        self.page1 = QWidget()
        self.page1.setObjectName(u"page1")
        self.page1.setMinimumWidth(150)
        self.page1.setMaximumWidth(150)

        #CREATE LAYPUT FOR PAGE 1
        self.verticalLayout = QVBoxLayout(self.page1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0,0,0,0)

        # LEFT MENU SPACING
        self.left_menu_spacinggg = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)


        self.label = QLabel("Brilho")
        self.verticalLayout.addWidget(self.label)
        self.slider = PySlider()
        self.verticalLayout.addWidget(self.slider)

        self.label2 = QLabel("Contraste")
        self.verticalLayout.addWidget(self.label2)
        self.slider2 = PySlider()
        self.verticalLayout.addWidget(self.slider2)

        #cereate a combobox

        self.label3 = QLabel("Escala de super resolução:")
        self.verticalLayout.addWidget(self.label3)

        self.combobox = QComboBox()
        self.combobox.setStyleSheet("""
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
        self.combobox.addItems(['Desativado', 'ESPCN_x2.pb', 'ESPCN_x3.pb', 'ESPCN_x4.pb'])
        self.verticalLayout.addWidget(self.combobox)
        
        #create label: Nitidez
        self.label_hist4 = QLabel("Nitidez")
        #create a switch
        self.switch4 = PyToggle()
        self.verticalLayout.addWidget(self.label_hist4)
        self.verticalLayout.addWidget(self.switch4)

        #create label: equalization for histogram
        self.label_hist = QLabel("Equalização de Histograma")
        #create a switch
        self.switch = PyToggle()
        self.verticalLayout.addWidget(self.label_hist)
        self.verticalLayout.addWidget(self.switch)

        #create label: filtro passa baixa
        self.label_hist2 = QLabel("Filtro Passa-Baixa")
        #create a switch
        self.switch2 = PyToggle()
        self.verticalLayout.addWidget(self.label_hist2)
        self.verticalLayout.addWidget(self.switch2)

        #create label: Filtro de mediana
        self.label_hist3 = QLabel("Filtro Mediana")
        #create a switch
        self.switch3 = PyToggle()
        self.verticalLayout.addWidget(self.label_hist3)
        self.verticalLayout.addWidget(self.switch3)

        self.verticalLayout.addItem(self.left_menu_spacinggg)

        StackedWidget.addWidget(self.page1)
    
        self.retranslateUi(StackedWidget)
        QMetaObject.connectSlotsByName(StackedWidget)

    def retranslateUi(self, StackedWidget):
        StackedWidget.setWindowTitle(QCoreApplication.translate("StackedWidget", u"StackedWidget", None))
    # retranslateUi

