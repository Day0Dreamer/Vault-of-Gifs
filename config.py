import json
from os.path import exists
from os import remove
from sys import exit

import logging

config_filename = 'config.json'


class ConfigDict(dict):
    def __init__(self):
        super(ConfigDict, self).__init__()

    def __missing__(self, key):
        print('whoops, bad config.')
        remove(config_filename)
        exit(1)


class Config(object):
    def __init__(self):
        logging.basicConfig(format='%(levelname)s:%(name)s:%(message)s', level='DEBUG')
        self.logger = logging.getLogger(__name__)
        self.config = ConfigDict()
        self.default = {
            'damaged_filesize': '500',
            'fps_delays': {'01': 100,
                           '02': 50,
                           '03': 33,
                           '04': 25,
                           '05': 20,
                           '06': 16,
                           '07': 14,
                           '08': 12,
                           '09': 11,
                           '10': 10,
                           '11': 9,
                           '12': 8,
                           '13': 7,
                           '14': 7,
                           '15': 6,
                           '16': 6,
                           '17': 5,
                           '18': 5,
                           '19': 5,
                           '20': 5,
                           '21': 4,
                           '22': 4,
                           '23': 4,
                           '24': 4,
                           '25': 4,
                           '26': 3,
                           '27': 3,
                           '28': 3,
                           '29': 3,
                           '30': 3,
                           '31': 3,
                           '32': 3,
                           '33': 3,
                           '34': 3,
                           '35': 3,
                           '36': 2,
                           '37': 2,
                           '38': 2,
                           '39': 2,
                           '40': 2,
                           '41': 2,
                           '42': 2,
                           '43': 2,
                           '44': 2,
                           '45': 2,
                           '46': 2,
                           '47': 2,
                           '48': 2,
                           '49': 2,
                           '50': 2,
                           '51': 2,
                           '52': 2,
                           '53': 2,
                           '54': 2,
                           '55': 2,
                           '56': 2,
                           '57': 2,
                           '58': 2,
                           '59': 2,
                           '60': 2,
                           '61': 2,
                           '62': 2,
                           '63': 2,
                           '64': 2,
                           '65': 2,
                           '66': 2,
                           '67': 2,
                           '68': 2,
                           '69': 2,
                           '70': 2,
                           '71': 1,
                           '72': 1,
                           '73': 1,
                           '74': 1,
                           '75': 1,
                           '76': 1,
                           '77': 1,
                           '78': 1,
                           '79': 1,
                           '80': 1,
                           '81': 1,
                           '82': 1,
                           '83': 1,
                           '84': 1,
                           '85': 1,
                           '86': 1,
                           '87': 1,
                           '88': 1,
                           '89': 1,
                           '90': 1,
                           '91': 1,
                           '92': 1,
                           '93': 1,
                           '94': 1,
                           '95': 1,
                           '96': 1,
                           '97': 1,
                           '98': 1,
                           '99': 1,
                           '100': 1
                           },
            'logging_level': 'CRITICAL',
            'logging_level_comment': 'CRITICAL, ERROR, WARNING, INFO, DEBUG',
            'console_enabled': False,
            'name_delimiter': '_',
            'default_folder': '',
            'preload_files': True,
            'overwrite_gifs': True
        }
        self.config_filename = config_filename

        # No config file check
        if not exists(self.config_filename):
            json.dump(self.default, open(self.config_filename, 'w'), indent=4)
            self.load_default()
            print('No config file, created default one')
        else:
            self.load()

    def load_default(self):
        self.config.update(self.default)

    def load(self):
        try:
            self.config.update(json.load(open(self.config_filename)))
            self.logger.info('Config is loaded from disk')
            # print('Config is loaded from disk')
        except FileNotFoundError:
            print(self.config_filename, 'is not found.')

    def save(self):
        try:
            json.dump(self.config, open(self.config_filename, 'w'), indent=4)
        except:
            print("Error while saving the config file")

    def __call__(self, *args, **kwargs):
        return self.config