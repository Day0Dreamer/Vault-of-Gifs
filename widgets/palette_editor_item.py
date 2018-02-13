from PySide.QtGui import *
from PySide.QtCore import *


class PEItem(QGraphicsItem):
    def __init__(self, height, num):
        super(PEItem, self).__init__()
        self.x = 0
        self.y = 0
        self.width = 150
        self.height = height
        self.num = num
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

    def boundingRect(self):
        return QRectF(self.x, self.y, self.width, self.height)

    def paint(self, painter, opt, widget):
        rec = self.boundingRect()
        if False:
            painter = QPainter()
        painter.fillRect(rec, Qt.black)
        painter.fillRect(rec.adjusted(1, 1, -1, -1), Qt.white)
        painter.fillRect(rec.adjusted(3, 3, -3, -3), Qt.gray)

        painter.setFont(QFont('Courier New', 9))
        painter.setPen(QPen(Qt.black))
        painter.drawText(rec, Qt.AlignCenter, 'Node {}'.format(self.num))

    def adjust_pos(self):
        y = self.pos().y()
        delta = y % self.height
        if delta > self.height/2:
            delta = self.height - delta
            self.setPos(self.pos()+QPoint(0, delta))
        else:
            self.setPos(self.pos()-QPoint(0, delta))
