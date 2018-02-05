# encoding: utf-8
"""Converts any video file to a gif
input_file is a full path
Returns input_file with .gif extension"""
import logging
from os.path import splitext, exists, abspath, join

from PySide.QtCore import Signal, QObject
from TasksPool import TasksPool
from config import Config
from emoji import Emoji

logger = logging.getLogger(__name__)


class Handbrake(QObject):
    return_signal = Signal(str)

    def __init__(self, emoji=None):
        """
        This class allows you to add() video files and convert them to gifs.
        Output files are going to be in the same folder as the input files.
        """
        super(Handbrake, self).__init__()
        self.tp = TasksPool()
        self.tp.return_signal.connect(lambda x: self.return_signal.emit(x))

        # If we supply Emoji object, then
        if isinstance(emoji, Emoji):
            video_file = abspath(join(emoji.folder, emoji.name + Config()()['name_delimiter'] + emoji.version + '.mov'))
            if exists(video_file):
                self.add(video_file)
                self.run()
            else:
                self.return_signal.emit(__name__ + 'Warning: {} has no .mov file'.format(emoji.name_no_ext))
                logger.warning('Warning: {} has no .mov file'.format(emoji.name_no_ext))
        elif isinstance(emoji, str):
            video_file = emoji
            if exists(video_file):
                self.add(video_file)
                self.run()

    def add(self, input_file):
        """
        :param input_file: Source video file
        :return: String with resulting gif's path
        """
        output_file = splitext(input_file)[0]+'.mp4'
        cmd = 'bin\\HandBrakeCLI.exe -i {} -o "{}"'.format(input_file, output_file)
        self.tp.add_task(cmd)
        logger.debug(cmd + ' added')

    def run(self):
        """
        Launches FFmpeg conversion process queue filled with add() method
        """
        self.tp.launch_list()
        self.tp = None

if __name__ == '__main__':
    pass
    # hb = Handbrake(Emoji(r'C:\Python\Vault_Of_Gifs\input\Emoji_02_280x280_20FPS.avi'))
