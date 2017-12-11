# encoding: utf-8

from PySide.QtCore import QEventLoop, Signal, QObject, QTimer
from PySide.QtGui import QApplication

# from config import Config
from emoji import Emoji
from ffmpeg import FFmpeg
from gifsicle import GifSicle
from os import path, listdir


# ################################# CONFIG ################################### #
# config = Config()
# fps_delays = config()['fps_delays']
# flag_show_message_bar_timer = config()['flag_show_message_bar_timer']
# act_folder = config()['act_folder']
# damaged_filesize = int(config()['damaged_filesize'])
# ############################### END CONFIG ################################# #

temp_project_folder = r'C:\Python\Vault_Of_Gifs\input'
temp_lossy_factor = 0


class Conversion(QObject):
    conversion1_done = Signal()
    conversion2_done = Signal()
    conversion3_done = Signal()

    def __init__(self, project_folder, lossy_factor, color_map=None):
        super(Conversion, self).__init__()

        self.project_folder = project_folder
        self.lossy_factor = lossy_factor
        # Use the first color map present in the project folder
        if not color_map:
            try:
                self.color_map = self.files_in_folder(self.project_folder, 'act')[0]
            except(IndexError):
                print('Please put one color_palette.act in the folder')

        self.loop = QEventLoop()
        self.conversion1_done.connect(self.loop.quit)
        self.conversion1_done.connect(self.gifs2lossy)
        self.conversion2_done.connect(self.gifs2damaged)
        self.conversion3_done.connect(lambda: QTimer.singleShot(1000, qapp.quit))
        self.avis2gif()
        self.loop.exec_()

    def avis2gif(self):
        emoji_dict = {Emoji(emoji).filename: Emoji(emoji) for emoji in self.files_in_folder(self.project_folder)}
        for item in emoji_dict.keys():
            # print(emoji_dict[item])
            if not emoji_dict[item].has_gif:
                print(emoji_dict[item].name, 'gif file missing, creating one')
                FFmpeg(emoji_dict[item])
        QTimer.singleShot(0, self.conversion1_done)

    def gifs2lossy(self):
        emoji_dict = {Emoji(emoji).filename: Emoji(emoji) for emoji in self.files_in_folder(self.project_folder)}
        for item in emoji_dict.keys():
            if not emoji_dict[item].has_lossy:
                print(emoji_dict[item].name, 'lossy file missing, creating one')
                GifSicle(emoji_dict[item], self.lossy_factor, self.color_map, to_lossy=True)
        QTimer.singleShot(0, self.conversion2_done)

    def gifs2damaged(self):
        emoji_dict = {Emoji(emoji).filename: Emoji(emoji) for emoji in self.files_in_folder(self.project_folder)}
        for item in emoji_dict.keys():
            if not emoji_dict[item].has_damaged:
                print(emoji_dict[item].name, 'damaged file missing, creating')
                GifSicle(emoji_dict[item], self.lossy_factor, self.color_map, to_damaged=True)
        self.conversion3_done.emit()

    def files_in_folder(self, folder='input', ext='avi'):
        return [path.join(path.abspath(folder), file) for file in listdir(folder) if '.'+str(ext) in file]

temp_project_folder = input('\nWhere is your project? (. or input or C:/input)\nDefault folder is "input"\n')
if temp_project_folder == '':
    temp_project_folder = path.join(path.curdir, 'input')

qapp = QApplication([])
conversion = Conversion(temp_project_folder, temp_lossy_factor)
qapp.exec_()
