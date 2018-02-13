from PySide.QtGui import QGraphicsView
from widgets import palette_editor_scene


class PEViewer(QGraphicsView):
    def __init__(self):
        super(PEViewer, self).__init__()
        self.pe_scene = palette_editor_scene.PEScene()
        self.setScene(self.pe_scene)
