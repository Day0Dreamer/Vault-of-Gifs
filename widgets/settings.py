from PySide.QtGui import *
from widgets import Settings_UI as ui
from widgets import stylesheet
from config import Config

# ################################# CONFIG ################################### #
config = Config()
fps_delays = config()['fps_delays']
damaged_filesize = int(config()['damaged_filesize'])
logging_level = config()['logging_level']
logging_level_comment = config()['logging_level_comment'].split(', ')
console_flag = config()['console_enabled']
default_project_folder = config()['default_folder']
preload_files = config()['preload_files']
name_delimiter = config()['name_delimiter']
overwrite_gifs = config()['overwrite_gifs']
icons_folder_name = 'icons'


class QtSettings(QDialog, ui.Ui_dialog_settings):
    def __init__(self):
        super(QtSettings, self).__init__()
        self.setupUi(self)
        self.setStyleSheet(stylesheet.houdini)

        self.damaged_filesize.setValue(damaged_filesize)
        self.preload_files.setChecked(preload_files)
        self.default_folder.setText(default_project_folder)
        # self.default_folder_browse.connect(self.select_default_folder)
        self.name_delimiter.setText(name_delimiter)
        self.logging_level.addItems(logging_level_comment)
        # self.logging_level.setCurrentIndex(0)
        self.console_enabled.setChecked(console_flag)
        self.overwrite_gifs.setChecked(overwrite_gifs)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.restore_defaults)

        self.buttonBox.button(QDialogButtonBox.Save).setEnabled(False)

    def restore_defaults(self):
        self.damaged_filesize.setValue(int(config.default['damaged_filesize']))
        self.preload_files.setChecked(config.default['preload_files'])
        self.default_folder.setText(config.default['default_folder'])
        self.name_delimiter.setText(config.default['name_delimiter'])
        self.logging_level.addItems(config.default['logging_level_comment'])
        # self.logging_level.setCurrentIndex(0)
        self.console_enabled.setChecked(config.default['console_enabled'])

    def select_default_folder(self):
        pass


