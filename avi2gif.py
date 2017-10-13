# encoding: utf-8
import subprocess


def ffmpeg(video, fps=30):
    """
    Using video2gif.bat and ffmpeg | video2gif.bat VIDEO -y -f FPS
    Returns resulting video file's path (HACKED)
    """
    command_line = 'video2gif.bat {} -y -f {}'.format(video, fps)
    p = subprocess.Popen(command_line, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while True:
        line = p.stdout.readline()
        if not line:
            break
        else:
            output = line.decode("utf-8")
            print(output.strip())
    return video.replace('gif', 'avi')
# import sys
# print("%x" % sys.maxsize, sys.maxsize > 2**32)
# MAGICK_HOME = 'c:\Program Files\ImageMagick-6.9.3-Q16'
# from wand.image import Image
# from wand.display import display
# with Image(filename='SteffonDiggsEmoji02280x28030FPS.avi') as img:
#     print(img.size)
#     img.format = 'gif'
#     img.
#     img.save(filename='vvv.gif')


