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


        self.label = QLabel("BRILHO")
        self.verticalLayout.addWidget(self.label)
        self.slider = PySlider()
        self.verticalLayout.addWidget(self.slider)

        self.label2 = QLabel("CONTRASTE")
        self.verticalLayout.addWidget(self.label2)
        self.slider2 = PySlider()
        self.verticalLayout.addWidget(self.slider2)

        self.label3 = QLabel("SELECIONE UMA OPÇÃO:")
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
        self.combobox.addItems(['Escala da super resolução', 'ESPCN_x2.pb', 'ESPCN_x3.pb', 'ESPCN_x4.pb'])
        self.combobox.setItemData(0, Qt.ItemIsEnabled, Qt.UserRole - 1)
        self.verticalLayout.addWidget(self.combobox)
        self.verticalLayout.addItem(self.left_menu_spacinggg)


        #CREATE PAGE 2
        StackedWidget.addWidget(self.page1)
        self.page2 = QWidget()
        self.page2.setObjectName(u"page2")
        self.page2.setMinimumWidth(150)
        self.page2.setMaximumWidth(150)

        #CREATE LAYOUT FOR PAGE2
        self.verticalLayout_2 = QVBoxLayout(self.page2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        StackedWidget.addWidget(self.page2)
        self.retranslateUi(StackedWidget)
        QMetaObject.connectSlotsByName(StackedWidget)


    def retranslateUi(self, StackedWidget):
        StackedWidget.setWindowTitle(QCoreApplication.translate("StackedWidget", u"StackedWidget", None))
    # retranslateUi

