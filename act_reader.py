# encoding: utf-8
from codecs import encode
from os import path, makedirs, curdir


def act_to_list(act_file):
    with open(act_file, 'rb') as act:
        raw_data = act.read()                               # Read binary data
    hex_data = encode(raw_data, 'hex')                  # Convert it to hexadecimal values
    total_colors_count = (int(hex_data[-7:-4], 16))     # Get last 3 digits to get number of colors total
    misterious_count = (int(hex_data[-4:-3], 16))       # I have no idea what does it do
    colors_count = (int(hex_data[-3:], 16))             # Get last 3 digits to get number of nontransparent colors
    # Decode colors from hex to string and split it by 6
    colors = [hex_data[i:i+6].decode() for i in range(0, total_colors_count*6, 6)]
    # Add # to each item and filter empty items if there is a corrupted total_colors_count bit
    colors = ['#'+i for i in colors if len(i)]

    # colors_count = '"' + act_file + '"' + ' contains {} color(s)'.format(len(colors))
    return colors, total_colors_count


def create_gifsicle_colormap(act_file, output=None):
    """
    :type act_file: str
    :param act_file: Input act file
    :type output: str
    :param output: Resulting txt file's path (Default temp folder+act_filename)
    :rtype: str
    :return: Returns the resulting txt file's path
    """
    if output is None:
        # makedirs(path.join(curdir, 'temp'), exist_ok=True)
        output = path.join(path.curdir, path.splitext(path.split(act_file)[1])[0] + '.txt')
    with open(output, 'w') as txt:
        txt.writelines(act_to_list(act_file)[0])
    return output


if __name__ == '__main__':
    act_file = "C:\Python\Giftcher\GeicoEmoji_01\GeicoEmoji_01.act"
    print(act_to_list(act_file))
    # create_gifsicle_colormap(act_file, act_file.split('.')[0]+'.txt')
