from PySide.QtGui import QDialog
from widgets import about_ui as ui, stylesheet


class QtAbout(QDialog, ui.Ui_Dialog):
    def __init__(self):
        super(QtAbout, self).__init__()
        self.setupUi(self)
        self.setStyleSheet(stylesheet.houdini)
        self.setWindowTitle('About')
