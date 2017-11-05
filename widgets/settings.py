from PySide.QtCore import *
from PySide.QtGui import *
from widgets import Settings_UI as ui


class QtSettings(QDialog, ui.Ui_dialog_settings):
    def __init__(self):
        super(QtSettings, self).__init__()
        self.setupUi(self)
