#IMPORTS
import os

import PySide6.QtGui

#IMPORT QT_CORE
from qt_core import *


class PyPushButton(QPushButton):
    def __init__(
            self,
            text="",
            heigh = 30,
            width = 50,
            text_padding  =0,
            border_radius=0,
            text_color = "#FFFFFF",
            icon_path ="",
            icon_color = "#FFFFFF",
            btn_color="#2B2D31",
            btn_hover = "#3E4145",
            btn_pressed = "#1E2022",
            is_active = False

    ):
        super().__init__()

        #set default parameters

        self.setText(text)
        self.setMaximumHeight(heigh)
        self.setMinimumHeight(heigh)
        self.setMaximumWidth(width)
        self.setMinimumWidth(width)
        self.setCursor(Qt.PointingHandCursor)

        #custom parameters
        self.minimum_width = width
        self.text_padding  = text_padding
        self.border_radius= border_radius
        self.text_color = text_color
        self.icon_path = icon_path
        self.icon_color = icon_color
        self.btn_color= btn_color
        self.btn_hover = btn_hover
        self.btn_pressed = btn_pressed
        self.is_active = is_active

        self.set_style(
            text_padding = self.text_padding,
            text_color = self.text_color,
            btn_color = self.btn_color,
            btn_hover = self.btn_hover,
            btn_pressed = self.btn_pressed,
            border_radius = self.border_radius,
            is_active = self.is_active,
        )

    def set_style(
            self,
            text_padding=0,
            text_color = "#FFFFFF",
            btn_color = "#2B2D31",
            border_radius = 0,
            btn_hover = "#3E4145",
            btn_pressed = "#1E2022",
            is_active = False
    ):
        style = f"""
        QPushButton{{
            color: {text_color};
            background-color:{btn_color};
            border: none;
            border-radius: {border_radius}px;
        }}
        QPushButton:hover {{
            background-color:{btn_hover};

        }}
        QPushButton:pressed{{
            background-color:{btn_pressed};

        }}
        """

        activate_style = f"""
        QPushButton{{
            background-color:{btn_hover};
            border-right: 5px solid red;
        
        }}
        """
        if not is_active:
            self.setStyleSheet(style)
            
        else:
            self.setStyleSheet(style + activate_style)

    