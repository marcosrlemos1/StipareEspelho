#IMPORT QT_CORE
from library import *

class PySlider(QSlider):
    def __init__(
            self,
            height=10,
            width=100,
            minimumWidth_=1,
            textPadding=0,
            textColor="white",
            iconPath="",
            iconColor="",
            sliderColor="000000",
            sliderHandleColor="#FFFFFF",
            sliderGrooveColor="#717674",
            borderRadius=1
    ):
        super().__init__(Qt.Horizontal)

        #SET DEFAULT PARAMETERS
        self.setMaximumHeight(height)
        self.setMinimumHeight(height)
        self.setMinimumWidth(width)
        self.setCursor(Qt.PointingHandCursor)
        self.setValue(50)

        #CUSTOM PARAMETERS
        self.minimumWidth_ = minimumWidth_
        self.textPadding = textPadding
        self.textColor = textColor
        self.iconPath = iconPath
        self.iconColor = iconColor
        self.sliderColor = sliderColor
        self.sliderHandleColor = sliderHandleColor
        self.sliderGrooveColor = sliderGrooveColor
        self.width_ = width
        self.borderRadius = borderRadius

        self.setStyle(
            textPadding=self.textPadding,
            textColor=self.textColor,
            sliderColor=self.sliderColor,
            sliderHandleColor=self.sliderHandleColor,
            sliderGrooveColor=self.sliderGrooveColor,
            borderRadius=self.borderRadius
        )

    def setStyle(
            self,
            textPadding=0,
            textColor="",
            sliderColor="",
            sliderHandleColor="",
            sliderGrooveColor="",
            borderRadius=5
    ):
        style = f"""
        QSlider {{
            color: {textColor};
            background-color: {sliderColor};
            padding: {textPadding}px {textPadding}px;
            text-align: center;
            border: none;
            border-radius: {borderRadius}px; /* Adiciona bordas arredondadas */
        }}
        QSlider::handle {{
            background-color: {sliderHandleColor};
            border: none;
            border-radius: 5px;
            width: 15px;
            margin: -3px 0px;
        }}
        QSlider::groove {{
            background-color: {sliderGrooveColor};
            border-radius: {borderRadius}px;
            height: 6px;
            margin: 0px;
        }}
        """

        self.setStyleSheet(style) 