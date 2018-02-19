def file_not_found(i):
    return ('File error',
            'While loading image to the viewport following error occurred.\n\nFile does not exist:\n{}'
            .format(i))
def corrupted_palette(i):
    return ('Palette error',
            'This palette appears to be corrupted.\nPlease test it before exporting.\n\n{}'
            .format(i))
