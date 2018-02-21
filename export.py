# encoding: utf-8
# Добавить обработку ненахождения карты цветов в папке инпут
from PySide import QtGui

from PySide.QtCore import QEventLoop, Signal, QObject, QTimer
from PySide.QtGui import QApplication, QMessageBox

import sys
import logging
import argparse
from emoji import Emoji
from ffmpeg import FFmpeg
from gifsicle import GifSicle
from os import path, listdir, remove
from widgets import settings
from handbrake import Handbrake
from widgets import stylesheet

logger = logging.getLogger(__name__)


# noinspection PyCallByClass
class Conversion(QObject):
    conversion1 = Signal(int, int)
    conversion2 = Signal(int, int)
    conversion3 = Signal(int, int)
    conversion4 = Signal(int, int)
    conversion5 = Signal(int, int)
    conversion1_done = Signal()
    conversion2_done = Signal()
    conversion3_done = Signal()
    conversion4_done = Signal()
    conversion5_done = Signal()
    error = Signal(str)

    def __init__(self):
        super(Conversion, self).__init__()
        # self.true_init(project_folder, lossy_factor, color_map=None)

    def true_init(self, project_folder, lossy_factor, color_map=None):
        self.project_folder = project_folder
        self.lossy_factor = lossy_factor
        # Use the first color map present in the project folder
        if not color_map:
            try:
                self.color_map = self.files_in_folder(self.project_folder, 'act')[0]
            except IndexError:
                error_message = 'Please put one color_palette.act in the folder'
                logger.warning(error_message)
                error_box = QMessageBox()
                # error_box.setStyleSheet(self.styleSheet())
                error_box.setWindowTitle('File error')
                error_box.setText('There is .act file missing')
                error_box.setInformativeText(error_message)
                error_box.exec_()
                return
        else:
            self.color_map = color_map

        self.loop = QEventLoop()
        self.conversion1_done.connect(self.loop.quit)
        self.conversion1_done.connect(self.gifs2lossy)
        self.conversion2_done.connect(self.gifs2damaged)
        self.conversion3_done.connect(self.handbrake)
        self.conversion4_done.connect(self.cleanup)
        if __name__ == '__main__':
            self.conversion5_done.connect(lambda: QTimer.singleShot(1000, qapp.quit))
        self.conversion1_done.connect(lambda: print('c1done'))
        self.conversion2_done.connect(lambda: print('c2done'))
        self.conversion3_done.connect(lambda: print('c3done'))
        self.conversion4_done.connect(lambda: print('c4done'))
        self.conversion5_done.connect(lambda: print('c5done'))
        self.avis2gif()
        self.loop.exec_()

    def avis2gif(self):
        emoji_dict = {Emoji(emoji).filename: Emoji(emoji) for emoji in self.files_in_folder(self.project_folder) if Emoji(emoji)}
        for index, item in enumerate(emoji_dict.keys()):
            # print(emoji_dict[item])
            if not emoji_dict[item].has_gif or settings.overwrite_gifs:
                print(emoji_dict[item].name, 'gif file missing, creating one')
                FFmpeg(emoji_dict[item])
                self.conversion1.emit(index+1, len(emoji_dict)-1)
        QTimer.singleShot(1, self.conversion1_done)

    def gifs2lossy(self):
        emoji_dict = {Emoji(emoji).filename: Emoji(emoji) for emoji in self.files_in_folder(self.project_folder) if Emoji(emoji)}
        for index, item in enumerate(emoji_dict.keys()):
            if not emoji_dict[item].has_lossy or settings.overwrite_gifs:
                print(emoji_dict[item].name, 'lossy file missing, creating one')
                # Get the proper lossy value for the gifsicle
                if '136' in emoji_dict[item].resolution:
                    lossy_factor = self.lossy_factor['136']
                elif '280' in emoji_dict[item].resolution:
                    lossy_factor = self.lossy_factor['280']
                GifSicle(emoji_dict[item], lossy_factor, self.color_map, to_lossy=True)
                self.conversion2.emit(index+1, len(emoji_dict)-1)
            else:
                print('Lossy file for {} already exists, skipping lossy creation'.format(emoji_dict[item].name))
        QTimer.singleShot(1, self.conversion2_done)

    def gifs2damaged(self):
        emoji_dict = {Emoji(emoji).filename: Emoji(emoji) for emoji in self.files_in_folder(self.project_folder) if Emoji(emoji)}
        for index, item in enumerate(emoji_dict.keys()):
            if not emoji_dict[item].has_damaged or settings.overwrite_gifs:
                print(emoji_dict[item].name, 'damaged file missing, creating')
                # Get the proper lossy value for the gifsicle
                if '136' in emoji_dict[item].resolution:
                    lossy_factor = self.lossy_factor['136']
                elif '280' in emoji_dict[item].resolution:
                    lossy_factor = self.lossy_factor['280']
                GifSicle(emoji_dict[item], lossy_factor, self.color_map, to_damaged=True)
                self.conversion3.emit(index+1, len(emoji_dict)-1)
        QTimer.singleShot(1, self.conversion3_done)

    def handbrake(self):
        emoji_list = [Emoji(emoji) for emoji in self.files_in_folder(self.project_folder) if Emoji(emoji)]
        Handbrake(emoji_list[0])
        self.conversion4.emit(1, 1)
        QTimer.singleShot(1, self.conversion4_done)


    def cleanup(self):
        all_temps = [temps for temps in self.files_in_folder(self.project_folder, 'tmp')]
        for temp_file in all_temps:
            remove(temp_file)
        all_gifs = [gifs for gifs in self.files_in_folder(self.project_folder, 'gif')]
        for temp_gif in all_gifs:
            if "LOSSY" not in temp_gif:
                try:
                    remove(temp_gif)
                except PermissionError as e:
                    logging.warning(e)
                    error_message = str(e)
                    error_box = QtGui.QMessageBox()
                    error_box.setStyleSheet(stylesheet.houdini)
                    error_box.setWindowTitle('File error')
                    error_box.setText(error_message)
                    error_box.exec_()
        self.conversion5.emit(1, 1)
        QTimer.singleShot(1, self.conversion5_done)


    def files_in_folder(self, folder='input', ext='avi'):
        return [path.join(path.abspath(folder), file) for file in listdir(folder) if '.'+str(ext) == path.splitext(file)[1]]

################################# ARGPARSE ################################# #
parser = argparse.ArgumentParser(description='This program converts video files to compressed gifs.',
                                 usage=r'"C:\files" "C:\color.act" 140 230')
parser.add_argument("folder", help="project folder", type=str, metavar='input')
parser.add_argument("color", help="color palette (act or txt)", type=str)
parser.add_argument("l280", help="LZW compression factor for 280px pictures", type=int, metavar="lossy 280px")
parser.add_argument("l136", help="LZW compression factor for 136px pictures", type=int, metavar="lossy 136px")
parser.add_argument("-ext", help="Video files extension (default is AVI)", type=str, default='avi')


############################## END ARGPARSE ################################ #

if __name__ == '__main__':

    if len(sys.argv) == 1:
        parser.print_help()
        # sys.exit(1)
    try:
        # args = parser.parse_args(['C:\Python\Vault_Of_Gifs\input', r'C:\Python\Vault_Of_Gifs\temp\perc.txt', '200', '200'])
        args = parser.parse_args()
    except:
        args = None

    temp_project_folder = input('\nWhere is your project? (. or input or C:/input)\nDefault folder is "input"\n')
    if temp_project_folder == '':
        temp_project_folder = path.join(path.curdir, 'input')

    qapp = QApplication([])
    temp_lossy_factor = 0
    conversion = Conversion(temp_project_folder, temp_lossy_factor)
    qapp.exec_()
