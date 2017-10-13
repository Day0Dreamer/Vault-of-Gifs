# encoding: utf-8
import subprocess
from PySide import QtCore


# def lossy(parent, input_file, lossy_factor, color_map, delay=3, output_file=None, program='gifsicle.exe', arg=''):
#     if output_file is None:
#         output_file = input_file
#     if arg == '':
#         arg = '-O3 -d={} --no-comments --no-names --no-extensions --lossy={} --use-colormap "{}" {} -o {}'\
#             .format(delay, lossy_factor, color_map, input_file, output_file)
#
#     process = QtCore.QProcess(parent)
#     process.start(program, arg)
#     return process.readAll()


def lossy(input_file, lossy_factor, color_map, delay=3, output_file=None):

    if output_file is None:
        output_file = input_file

    command_line = \
        'gifsicle.exe -O3 -d={} --no-comments --no-names --no-extensions --lossy={} --use-colormap "{}" {} -o {}'.format(
            delay, lossy_factor, color_map, input_file, output_file)

    p = subprocess.Popen(command_line, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while True:
        line = p.stdout.readline()
        if not line:
            break
        else:
            output = line.decode("utf-8")
            print(output.strip())

    return output_file


if __name__ == '__main__':
    lossy('SteffonDiggsEmoji-02-280x280-30FPS.gif', 20, 'table.txt')