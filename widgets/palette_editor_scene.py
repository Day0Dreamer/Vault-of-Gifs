from PySide.QtCore import *
from PySide.QtGui import *
from widgets import palette_editor_item


class PEScene(QGraphicsScene):
    def __init__(self):
        super(PEScene, self).__init__()
        self.setSceneRect(-1000, -1000, 2000, 2000)
        self.grid = 30
        self.add_node()

    def drawBackground(self, painter, rect):
        if False:
            painter = QPainter()
            rect = QRect()
        painter.fillRect(rect, QColor('#121212'))

        left = rect.left() - (rect.left() % self.grid)
        top = rect.top() - (rect.top() % self.grid)
        right = rect.right()
        bottom = rect.bottom()
        lines = []
        for x in range(int(left), int(right), self.grid):
            lines.append(QLine(x, top, x, bottom))
        for y in range(int(top), int(bottom), self.grid):
            lines.append(QLine(left, y, right, y))
        painter.drawLines(lines)

    def add_node(self, pos=False):
        if not pos:
            pos = QPoint(0, 0)
        item = palette_editor_item.PEItem(self.grid, len(self.items())+1)
        self.addItem(item)
        item.setPos(pos)

    def mouseDoubleClickEvent(self, event):
        self.add_node(event.scenePos())
        super(PEScene, self).mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event):
        for i in self.items():
            i.adjust_pos()
        super(PEScene, self).mouseReleaseEvent(event)