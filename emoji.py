# encoding: utf-8
from os import path
from config import Config
import re

__config = Config()
fps_delays = __config()['fps_delays']

class Emoji(object):
    def __init__(self, filename):
        # Declare variables
        """
        :type filename: str
        :param filename: File path to convert to Emoji object
        Creates Emoji objects from a file, based on a naming convention: [Name]-[02]-[280х280]-[30FPS].[ext]
        """
        self.name = self.version = self.resolution = self.fps = self.lossy = self.damaged = self.has_gif =\
            self.has_lossy = self.has_damaged = self.gif = False
        # Set full path
        self.full_path = filename
        # Set containing folder and filename
        self.folder, self.filename = path.split(filename)
        # Set filename without extension and extension
        self.name_no_ext, self.ext = path.splitext(self.filename)
        # Separate file name to it's parts
        name_and_version, self.resolution, self.fps = self.name_no_ext.rsplit('-', 2)
        # Extract name and version from user input
        self.name, self.version = re.split('(\d*$)', name_and_version)[:2]
        # Remove spaces from name in the beginning and the end
        self.name = self.name.strip()
        # else:
        #     raise Exception('Something went wrong with the name of {}'.format(filename))
        # Set FPS to caps and remove the letters FPS
        self.fps = self.fps.upper().rstrip('FPS')
        # Set delay using config
        self.delay = fps_delays[str(self.fps)]
        # Check if there are gif derivatives
        self.gif_path = path.splitext(self.full_path)[0]+'.gif'
        if path.exists(self.gif_path):
            self.has_gif = True
        self.lossy_path = path.splitext(self.full_path)[0]+'-lossy'+'.gif'
        if path.exists(self.lossy_path):
            self.has_lossy = True
        self.damaged_path = path.splitext(self.full_path)[0]+'-lossy-damaged'+'.gif'
        if path.exists(self.damaged_path):
            self.has_damaged = True

    def __repr__(self):
        data = 'Name: {} | version: {} | resolution: {} | fps: {} | gif: {} | lossy: {} | damaged: {}'\
            .format(self.name, self.version, self.resolution, self.fps, self.has_gif, self.has_lossy, self.has_damaged)
        return data

    def full_info(self):
        """
        :rtype: str
        :return: Returns out all the variables for a given object
        """
        data = 'Name: {} | version: {} | resolution: {} | fps: {} | gif: {} ({}) | lossy: {} ({}) | damaged: {} ({}) | Fullpath: {} | Folder: {} | Filename: {} | NameNoExt {} | Ext {} | SplitProperties {}'\
            .format(self.name, self.version, self.resolution, self.fps, self.has_gif, self.gif_path, self.has_lossy, self.lossy_path, self.has_damaged, self.damaged_path, self.full_path, self.folder, self.filename, self.name_no_ext, self.ext, self.split_properties)
        return data

if __name__ == '__main__':
    e = Emoji(r"C:\Python\Vault_Of_Gifs\input1\Animation 2 2132001-280x280-30FPS.avi")
    print(e)