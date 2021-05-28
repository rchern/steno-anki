import os
import os.path
import urllib.request

from . import options

path = os.path.abspath(options.values.diagrams)

if not os.path.isdir(path):
    os.mkdir(path)

def download(chord):
    sanitized_name = chord.replace('*', '_star_').replace('#', '_num_')
    filename = f'plover-{sanitized_name}.png'

    sanitized_chord = chord.replace('#', '%23')

    filepath = os.path.join(path, filename)

    if not os.path.isfile(filepath):
        urllib.request.urlretrieve(f'https://spectra.sammdot.ca/diagram/{sanitized_chord}/png', filepath)

    return filename