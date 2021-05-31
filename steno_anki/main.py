import fnmatch
from argparse import ArgumentParser
import os

from anki import Anki

args = ArgumentParser()
args.add_argument('-i', '--input', dest='input', default='decks')
args.add_argument('-o', '--output', dest='output', default='plover.apkg')

options = args.parse_args()

print(options)

directory = os.path.abspath(options.input)
files = fnmatch.filter(os.listdir(directory), '*.txt')

anki = Anki()

print(files)

for file in files:
    entries = open(os.path.join(directory, file)).read().splitlines()

    for index, entry in enumerate(entries, start=1):
        if '\t' in entry:
            anki.generate_note(entry)
        elif '~~~' in entry:
            anki.generate_deck(entry)
        elif not entry or entry.startswith('#'):
            continue
        else:
            raise Exception(f'Unknown Line Type {file}#{index}')

anki.generate_package(options.output)
