from library import *

#Switch Botton
class PyToggle(QCheckBox):
    def __init__(
            self,
            width=40,
            bgColor="#777",
            circleColor="#DDD",
            activeColor="red",
            animationCurve = QEasingCurve.OutBounce
    ):
        QCheckBox.__init__(self)

        self.setFixedSize(width, 18)
        self.setCursor(Qt.PointingHandCursor)

        self._bgColor = bgColor
        self._circleColor = circleColor
        self._activeColor = activeColor

        self._circlePosition = 3
        self.animation = QPropertyAnimation(self, b"circle_position",self)
        self.animation.setEasingCurve(animationCurve)
        self.animation.setDuration(500)

        self.stateChanged.connect(self.start_transition)

    @Property(float)
    def circle_position(self):
        return self._circlePosition
    
    @circle_position.setter
    def circle_position(self, pos):
        self._circlePosition = pos
        self.update()

    def start_transition(self, value):
        self.animation.stop()
        if value:
            self.animation.setEndValue(self.width() - 16) 
        else:
            self.animation.setEndValue(3)  

        self.animation.start()        

    def hitButton (self, pos: QPoint):
        return self.contentsRect().contains(pos)


    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(Qt.NoPen)

        rect = QRect(0, 0, self.width(), self.height())

        if not self.isChecked():

            p.setBrush(QColor(self._bgColor))
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)


            p.setBrush(QColor(self._circleColor))
            p.drawEllipse(self._circlePosition, 3, 12, 12)

        else:

            p.setBrush(QColor(self._activeColor))
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)


            p.setBrush(QColor(self._circleColor))
            p.drawEllipse(self._circlePosition, 3, 12, 12)

        p.end()
