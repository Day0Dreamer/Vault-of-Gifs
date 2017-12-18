# encoding: utf-8
"""

"""
from PySide.QtCore import Signal, QEventLoop, QTimer, QObject

from TasksPool import TasksPool
from emoji import Emoji
from act_reader import create_gifsicle_colormap
from os.path import splitext, getsize, exists
from config import Config

config = Config()
conf_damaged_filesize = int(config()['damaged_filesize'])*1024


class GifSicle(QObject):
    loop_done = Signal()

    def __init__(self, emoji=None, lossy_factor=None, color_map=None, to_lossy=None, to_damaged=None):
        """
        This class allows you to add() gif files and compress them using LZW compression.
        Output files are going to be in the same folder as the input files.
        """
        super(GifSicle, self).__init__()
        self.tp = TasksPool()
        # If we supply Emoji object, then
        if isinstance(emoji, Emoji):
            if emoji.has_gif:
                if to_lossy:
                    self.to_lossy(emoji, lossy_factor, color_map)
                elif to_damaged:
                    self.to_damaged(emoji, lossy_factor, color_map)
                else:
                    self.updated(emoji, lossy_factor, color_map)
            else:
                print(__name__, 'Warning: {} has no gif made'.format(emoji.name_no_ext))

    def updated(self, emoji, lossy_factor, color_map):
        self.add(input_file=emoji.gif_path,
                 lossy_factor=lossy_factor,
                 color_map=color_map,
                 delay=emoji.delay,
                 output_file=emoji.temp_path)
        self.run()

    def to_lossy(self, emoji, lossy_factor, color_map):
        self.add(input_file=emoji.gif_path,
                 lossy_factor=lossy_factor,
                 color_map=color_map,
                 delay=emoji.delay,
                 output_file=emoji.lossy_path)
        self.run()

    def to_damaged(self, emoji, lossy_factor, color_map):
        # Create filesize dict
        filesizes = {}
        l_filesizes = []
        # If there is a lossy gif, then:
        if exists(emoji.lossy_path):
            # If lossy gif is over the damaged_filesize limit, then:
            lossy_filesize = getsize(emoji.lossy_path)
            if lossy_filesize > conf_damaged_filesize:
                # Make first damaged
                lossy_factor = 400
                self.add(input_file=emoji.gif_path,
                         lossy_factor=lossy_factor,
                         color_map=color_map,
                         delay=emoji.delay,
                         output_file=emoji.damaged_path)
                self.run()
                damaged_filesize = getsize(emoji.damaged_path)
                if damaged_filesize > conf_damaged_filesize:
                    print('Lossy factor of 400 is still not enough. Drop file')
                else:
                    filesizes[lossy_factor] = damaged_filesize
                    lossy_factor = 0
                    self.tp = TasksPool()
                    self.add(input_file=emoji.gif_path,
                             lossy_factor=lossy_factor,
                             color_map=color_map,
                             delay=emoji.delay,
                             output_file=emoji.damaged_path)
                    self.run()
                    damaged_filesize = getsize(emoji.damaged_path)
                    filesizes[lossy_factor] = damaged_filesize
                    f_list = sorted(list(zip(filesizes.keys(), filesizes.values())))
                    x_distance = f_list[1][0]-f_list[0][0]  # Change in lossy
                    y_distance = f_list[1][1]-f_list[0][1]  # Change in filesize
                    delta_x = y_distance/x_distance  # Change in y over one x
                    # Lossy prediction = 500Kb-filesize of first point / delta_x(fsize decline over one lossy factor) +
                    # x offset of first point
                    x = ((conf_damaged_filesize-f_list[0][1])/delta_x)+f_list[0][0]
                    lossy_factor = int(x)
                    endless_loop_check = {'+': 0, '-': 0}
                    # How precise do we want to get to conf_damaged_filesize (500kb)
                    filesize_headroom = -1024*5
                    while damaged_filesize > conf_damaged_filesize:
                        # Start the loop of processing
                        self.loop(emoji, lossy_factor, color_map)
                        # Get new filesize and difference
                        damaged_filesize = getsize(emoji.damaged_path)
                        filesize_difference = damaged_filesize - conf_damaged_filesize
                        print('Lossy: {}, Current filesize: {} bytes, Needed filesize {} bytes, Difference {} bytes'
                              .format(lossy_factor, damaged_filesize, conf_damaged_filesize, filesize_difference))
                        # If filesize is 10Kb too less
                        if filesize_difference < filesize_headroom:
                            # Do more quality and more size
                            lossy_factor -= 2
                            # Make the while pass the size test
                            damaged_filesize = conf_damaged_filesize+1
                            # Count how much have we decreased lossy factor
                            endless_loop_check['-'] += 1
                        else:
                            # Do less quality and less size
                            lossy_factor += 1
                            # Count how much have we increased lossy factor
                            endless_loop_check['+'] += 1
                        # If endless loop detected, than double the headroom
                        if endless_loop_check['+'] >= 3 and endless_loop_check['-'] >= 3:
                            # Reset the counter
                            endless_loop_check = {'+': 0, '-': 0}
                            # Double the headroom
                            filesize_headroom *= 2
                            print('Endless loop detected, new headroom is: {} bytes'.format(filesize_headroom))
            else:
                print('Lossy file is {} Kb, there is no need for damaged file'.format(lossy_filesize))

    def loop(self, emoji, lossy_factor, color_map):
        self.tp = TasksPool()
        # Make consecutive damaged files
        self.add(input_file=emoji.lossy_path,
                 lossy_factor=lossy_factor,
                 color_map=color_map,
                 delay=emoji.delay,
                 output_file=emoji.damaged_path)
        self.run()
        QTimer.singleShot(0, self.loop_done)

    def add(self, input_file, lossy_factor, color_map, fps=30, delay=None, output_file=None):
        """

        """
        if output_file is None:
            output_file = input_file
        if delay is None:
            delay = int(100/int(fps))
        if splitext(color_map)[1] == '.act':
            color_map = create_gifsicle_colormap(color_map)
        cmd = r'bin\gifsicle.exe -O3 --no-comments --no-names --no-extensions -d{} --lossy={} ' \
              r'--use-colormap "{}" {} -o {}'.format(delay, lossy_factor, color_map, input_file, output_file)

        self.tp.add_task(cmd)
        return input_file

    def run(self):
        """
        Launches GifSicle conversion process queue filled with add() method
        """
        self.tp.launch_list()
        self.tp = None


def lossy(input_file, lossy_factor, color_map, delay=3, output_file=None):

    if output_file is None:
        output_file = input_file


if __name__ == '__main__':
    GifSicle(Emoji(r'C:\Python\Vault_Of_Gifs\input\Marshawn_Lynch_Emoji-01-280x280-30FPS.gif'),
             100,
             r"C:\Python\Vault_Of_Gifs\input\_Marshall_Lynch_Emoji_01.act",
             to_damaged=True)
    # gc = GifSicle()
    # gc.add(r'C:\Python\Vault_Of_Gifs\input\Emoji-02-280x280-30FPS.gif',
    #        200,
    #        r"C:\Python\Vault_Of_Gifs\act\xxx.act",
    #        output_file=r'C:\Python\Vault_Of_Gifs\input\Emoji-02-280x280-30FPS-lossy.gif')
    # gc.add(r'C:\Python\Vault_Of_Gifs\input\Marshawn_Lynch_Emoji-01-280x280-30FPS.gif',
    #        200,
    #        r"C:\Python\Vault_Of_Gifs\act\perc.act",
    #        output_file=r'C:\Python\Vault_Of_Gifs\input\Marshawn_Lynch_Emoji-01-280x280-30FPS-lossy.gif')
    # gc.run()
    pass