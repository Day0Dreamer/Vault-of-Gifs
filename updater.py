from os import makedirs
from os.path import join, exists
from tqdm import tqdm
import urllib.request


def my_hook(t):
    """Wraps tqdm instance.
    Don't forget to close() or __exit__()
    the tqdm instance once you're done with it (easiest using `with` syntax).
    """
    last_b = [0]

    def update_to(b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            t.total = tsize
        t.update((b - last_b[0]) * bsize)
        last_b[0] = b

    return update_to


def folder_updater(folder_name, file_names):
    makedirs(folder_name, exist_ok=True)
    missing_binarnies = [file for file in file_names if not exists(join(folder_name, file))]

    for file in missing_binarnies:
        url = "http://vaultofdreams.myds.me/Vaultofgifs/{}/{}".format(folder_name, file)
        with tqdm(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=file) as t:
            urllib.request.urlretrieve(url, filename=join(folder_name, file), reporthook=my_hook(t), data=None)

needed_bins = ['ffmpeg.exe', 'gifsicle.exe', 'HandBrakeCLI.exe']
folder_updater('bin', needed_bins)

needed_icons = ['136x136_15.png', '136x136_15_D.png', '136x136_15_L.png', '136x136_15_L_D.png', '136x136_18.png', '136x136_20.png', '136x136_20_D.png', '136x136_20_L.png', '136x136_20_L_D.png', '136x136_23.png', '136x136_25.png', '136x136_25_D.png', '136x136_25_L.png', '136x136_25_L_D.png', '136x136_30.png', '136x136_30_D.png', '136x136_30_L.png', '136x136_30_L_D.png', '280x280_15.png', '280x280_15_D.png', '280x280_15_L.png', '280x280_15_L_D.png', '280x280_18.png', '280x280_20.png', '280x280_20_D.png', '280x280_20_L.png', '280x280_20_L_D.png', '280x280_23.png', '280x280_25.png', '280x280_25_D.png', '280x280_25_L.png', '280x280_25_L_D.png', '280x280_30.png', '280x280_30_D.png', '280x280_30_L.png', '280x280_30_L_D.png', 'ps.png']
folder_updater('icons', needed_icons)
