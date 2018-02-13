from PySide.QtCore import Qt
from PySide.QtGui import *
# from widgets import palette_editor_ui as ui
from widgets import palette_editor_viewer as peviewer
from widgets import stylesheet


class PaletteEditor(QWidget):
    def __init__(self):
        super(PaletteEditor, self).__init__()
        self.setStyleSheet(stylesheet.houdini)

        self.setObjectName("palette_editor")
        self.resize(700, 300)
        self.horizontalLayout = QHBoxLayout(self)
        self.pe_viewer = peviewer.PEViewer()
        self.horizontalLayout.addWidget(self.pe_viewer)

# class PaletteEditor(QGraphicsView):
#     def __init__(self):
#         super(PaletteEditor, self).__init__()
#         self.setStyleSheet(stylesheet.houdini)
#
#         self.scene = QGraphicsScene()
#         self.setScene(self.scene)

        # self.rect1 = self.scene.addRect(0, 0, 30, 30, QPen(Qt.black), QBrush(Qt.cyan))

if __name__ == '__main__':
    app = QApplication([])
    w = PaletteEditor()
    w.show()
    app.exec_()
