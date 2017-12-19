# encoding: utf-8
"""Converts any video file to a gif
input_file is a full path
Returns input_file with .gif extension"""

from os.path import splitext, exists
from TasksPool import TasksPool
from emoji import Emoji


class FFmpeg(object):
    def __init__(self, emoji=None):
        """
        This class allows you to add() video files and convert them to gifs.
        Output files are going to be in the same folder as the input files.
        """
        self.tp = TasksPool()

        # If we supply Emoji object, then
        if isinstance(emoji, Emoji):
            if exists(emoji.full_path):
                self.add(emoji.full_path, emoji.fps)
                self.run()
            else:
                print(__name__, 'Warning: {} has no video file'.format(emoji.name_no_ext))

    def add(self, input_file, fps, delete_palette=True):
        """
        :param input_file: Source video file
        :param fps: Video's FPS count
        :param delete_palette: If True, the palette for gif generation gets deleted
        :return: String with resulting gif's path
        """
        palette_file = splitext(input_file)[0]+'.png'
        output_file = splitext(input_file)[0]+'.gif'
        cmd = 'bin\\ffmpeg.exe -v error -i "{}" -vf "fps={},scale=-1:-1:flags=lanczos,palettegen=max_colors=256" -y "{}"'.format(input_file, fps, palette_file)
        self.tp.add_task(cmd)
        cmd = 'bin\\ffmpeg.exe -v error -i "{}" -i "{}" -lavfi "fps={},scale=-1:-1:flags=lanczos [x]; [x][1:v] paletteuse=dither=none" -y "{}"'.format(input_file, palette_file, fps, output_file)
        self.tp.add_task(cmd)
        if delete_palette:
            cmd = 'cmd.exe /c del {}'.format(palette_file)
            self.tp.add_task(cmd)
        return splitext(input_file)[0] + '.gif'

    def run(self):
        """
        Launches FFmpeg conversion process queue filled with add() method
        """
        self.tp.launch_list()
        self.tp = None

if __name__ == '__main__':

    # ff = FFmpeg()
    # ff.add(r'C:\Python\Vault_Of_Gifs\input\Emoji-02-280x280-30FPS.avi', 30)
    # ff.add(r'C:\Python\Vault_Of_Gifs\input\Marshawn_Lynch_Emoji-01-280x280-30FPS.avi', 30)
    # ff.run()
    pass
