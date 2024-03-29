#IMPORT QT_CORE
from library import *


class PyPushButton(QPushButton):
    def __init__(
            self,
            text="",
            heigh = 30,
            width = 50,
            textPadding  =0,
            borderRadius=0,
            textColor = "#FFFFFF",
            iconPath ="",
            iconColor = "#FFFFFF",
            btnColor="#2B2D31",
            btnHover = "#3E4145",
            btnPressed = "#1E2022",
            isActive = False

    ):
        super().__init__()

        #SET DEFAULT PARAMETERS
        self.setText(text)
        self.setMaximumHeight(heigh)
        self.setMinimumHeight(heigh)
        self.setMaximumWidth(width)
        self.setMinimumWidth(width)
        self.setCursor(Qt.PointingHandCursor)

        #CUSTOM PARAMETERS
        self.minimumWidth_ = width
        self.textPadding  = textPadding
        self.borderRadius= borderRadius
        self.textColor = textColor
        self.iconPath = iconPath
        self.iconColor = iconColor
        self.btnColor= btnColor
        self.btnHover = btnHover
        self.btnPressed = btnPressed
        self.isActive = isActive

        self.setStyle(
            textPadding = self.textPadding,
            textColor = self.textColor,
            btnColor = self.btnColor,
            btnHover = self.btnHover,
            btnPressed = self.btnPressed,
            borderRadius = self.borderRadius,
            isActive = self.isActive,
        )

    def setStyle(
            self,
            textPadding=0,
            textColor = "#FFFFFF",
            btnColor = "#2B2D31",
            borderRadius = 0,
            btnHover = "#3E4145",
            btnPressed = "#1E2022",
            isActive = False
    ):
        style = f"""
        QPushButton{{
            color: {textColor};
            background-color:{btnColor};
            border: none;
            border-radius: {borderRadius}px;
        }}
        QPushButton:hover {{
            background-color:{btnHover};

        }}
        QPushButton:pressed{{
            background-color:{btnPressed};

        }}
        """

        activateStyle = f"""
        QPushButton{{
            background-color:{btnHover};
            border-right: 5px solid red;
        
        }}
        """
        if not isActive:
            self.setStyleSheet(style)
            
        else:
            self.setStyleSheet(style + activateStyle)