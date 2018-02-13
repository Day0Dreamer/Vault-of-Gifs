from PySide.QtCore import *
from PySide.QtGui import *

sensitivity = 3


class Viewer(QGraphicsView):
    TIME_OFFSET = Signal(int)
    TEMP_PAUSE = Signal(bool)
    PLAYPAUSE = Signal()
    MOUSEWHEEL = Signal(bool)

    def __init__(self, parent):
        super(Viewer, self).__init__(parent)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.time_scroll = False
        self.pan = False
        self.lastX = 0
        self.lastY = 0
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.time_scroll = True
            self.lastX = event.x()
            self.TEMP_PAUSE.emit(True)
        elif event.button() == Qt.RightButton:
            self.PLAYPAUSE.emit()
        elif event.button() == Qt.MiddleButton:
            self.pan = True
            self.lastX = event.x()
            self.lastY = event.y()
        else:
            super(Viewer, self).mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if self.time_scroll:
            offset_x = event.x() - self.lastX
            if not offset_x % sensitivity:
                self.lastX = event.x()
                self.TIME_OFFSET.emit(offset_x)
        elif self.pan:
            offset_x = self.horizontalScrollBar().value() - (event.x() - self.lastX)
            self.horizontalScrollBar().setValue(offset_x)
            self.lastX = event.x()

            offset_y = self.verticalScrollBar().value() - (event.y() - self.lastY)
            self.verticalScrollBar().setValue(offset_y)
            self.lastY = event.y()
        else:
            super(Viewer, self).mouseMoveEvent(event)
            
    def mouseReleaseEvent(self, event):
        if self.time_scroll:
            self.time_scroll = False
            self.TEMP_PAUSE.emit(False)
        elif self.pan:
            self.pan = False
        else:
            super(Viewer, self).mouseReleaseEvent(event)

    def wheelEvent(self, event):
        if True:
            self.MOUSEWHEEL.emit(bool(max(event.delta(), 0)))
        else:
            super(Viewer, self).scroll(event)

