# encoding: utf-8
from os import path

def act_to_list(act_file):
    with open(act_file, 'rb') as act:
        raw_data = act.readline()
        hex_data = ''
        for i in bytearray(raw_data):
            hex_data += ("{0:x}".format(i).zfill(2))
        colors = [hex_data[i:i+6] for i in range(0, len(hex_data), 6)]

        # Delete duplicating colors
        unique_set = set()
        unique_list = []
        for x in colors:
            if x not in unique_set:
                unique_list.append(x)
                unique_set.add(x)
        colors = unique_list

        # Convert color ints to #ffffff format
        colors = ['#'+i+'\n' for i in colors]
        colors[-1] = colors[-1].strip('\n')
        if len(colors[-1]) < 7:
            del colors[-1]
        # print(len(colors[-1]) < 7) (is the color full length?)
        colors_count = '"' + act_file + '"' + ' contains {} color(s)'.format(len(colors))
        return colors, colors_count


def create_gifsicle_colormap(act_file, output=None):
    if output is None:
        output = path.join('.\\temp', path.splitext(path.split(act_file)[1])[0] + '.txt')
    with open(output, 'w') as txt:
        txt.writelines(act_to_list(act_file)[0])
    return output

if __name__ == '__main__':
    act_file = 'act\\Marshall_Lynch_Emoji_01_by_ue.act'
    print(act_to_list(act_file))
    # create_gifsicle_colormap(act_file, act_file.split('.')[0]+'.txt')
