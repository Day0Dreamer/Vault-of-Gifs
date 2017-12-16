# encoding: utf-8
from PySide.QtCore import QEventLoop, Signal, QObject, QTimer
from PySide.QtGui import QApplication

import sys
import argparse
from emoji import Emoji
from ffmpeg import FFmpeg
from gifsicle import GifSicle
from os import path, listdir


# noinspection PyCallByClass
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
        # self.conversion3_done.connect(lambda: QTimer.singleShot(1000, qapp.quit))
        self.conversion1_done.connect(lambda: print('c1done'))
        self.conversion2_done.connect(lambda: print('c2done'))
        self.conversion3_done.connect(lambda: print('c3done'))
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
        QTimer.singleShot(0, self.conversion3_done)

    def files_in_folder(self, folder='input', ext='avi'):
        return [path.join(path.abspath(folder), file) for file in listdir(folder) if '.'+str(ext) in file]

# ################################# ARGPARSE ################################# #
# parser = argparse.ArgumentParser(description='This program converts video files to compressed gifs.',
#                                  usage=r'"C:\files" "C:\color.act" 140 230')
# parser.add_argument("folder", help="project folder", type=str, metavar='input')
# parser.add_argument("color", help="color palette (act or txt)", type=str)
# parser.add_argument("l280", help="LZW compression factor for 280px pictures", type=int, metavar="lossy 280px")
# parser.add_argument("l136", help="LZW compression factor for 136px pictures", type=int, metavar="lossy 136px")
# parser.add_argument("-ext", help="Video files extension (default is AVI)", type=str, default='avi')
# if len(sys.argv) == 1:
#     parser.print_help()
#     # sys.exit(1)
# try:
#     # args = parser.parse_args(['C:\Python\Vault_Of_Gifs\input', r'C:\Python\Vault_Of_Gifs\temp\perc.txt', '200', '200'])
#     args = parser.parse_args()
# except:
#     args = None

# ############################## END ARGPARSE ################################ #

if __name__ == '__main__':
    temp_project_folder = input('\nWhere is your project? (. or input or C:/input)\nDefault folder is "input"\n')
    if temp_project_folder == '':
        temp_project_folder = path.join(path.curdir, 'input')

    qapp = QApplication([])
    temp_lossy_factor = 0
    conversion = Conversion(temp_project_folder, temp_lossy_factor)
    qapp.exec_()
