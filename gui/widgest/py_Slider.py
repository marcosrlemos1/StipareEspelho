#IMPORTS
import os

import PySide6.QtGui

#IMPORT QT_CORE
from qt_core import *

class PySlider(QSlider):
    def __init__(
            self,
            height=10,
            width=100,
            minimum_width=1,
            text_padding=0,
            text_color="white",
            icon_path="",
            icon_color="",
            slider_color="000000",
            slider_handle_color="#FFFFFF",
            slider_groove_color="#717674",
            border_radius=1
    ):
        super().__init__(Qt.Horizontal)

        # self default parameters
        self.setMaximumHeight(height)
        self.setMinimumHeight(height)
        self.setMinimumWidth(width)
        self.setCursor(Qt.PointingHandCursor)
        self.setValue(50)

        # custom parameters
        self.minimumWidth = minimum_width
        self.text_padding = text_padding
        self.text_color = text_color
        self.icon_path = icon_path
        self.icon_color = icon_color
        self.slider_color = slider_color
        self.slider_handle_color = slider_handle_color
        self.slider_groove_color = slider_groove_color
        self.width = width
        self.border_radius = border_radius

        self.set_style(
            text_padding=self.text_padding,
            text_color=self.text_color,
            slider_color=self.slider_color,
            slider_handle_color=self.slider_handle_color,
            slider_groove_color=self.slider_groove_color,
            border_radius=self.border_radius
        )
    def set_style(
            self,
            text_padding=0,
            text_color="",
            slider_color="",
            slider_handle_color="",
            slider_groove_color="",
            border_radius=5
    ):
        style = f"""
        QSlider {{
            color: {text_color};
            background-color: {slider_color};
            padding: {text_padding}px {text_padding}px;
            text-align: center;
            border: none;
            border-radius: {border_radius}px; /* Adiciona bordas arredondadas */
        }}
        QSlider::handle {{
            background-color: {slider_handle_color};
            border: none;
            border-radius: 5px;
            width: 15px;
            margin: -3px 0px;
        }}
        QSlider::groove {{
            background-color: {slider_groove_color};
            border-radius: {border_radius}px;
            height: 6px;
            margin: 0px;
        }}
        """

        self.setStyleSheet(style) 