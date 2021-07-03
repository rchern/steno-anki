from argparse import ArgumentParser
import fnmatch
import os
from pathlib import Path

from anki import Anki

args = ArgumentParser()
args.add_argument('-i', '--input', dest='input', default='decks')
args.add_argument('-o', '--output', dest='output', default='dist')

options = args.parse_args()
print(options);

def process():
    options.input = os.path.abspath(options.input)
    options.output = os.path.abspath(options.output)

    _, deck_folders, deck_files = next(os.walk(options.input))

    Path(options.output).mkdir(parents=True, exist_ok=True)

    for folder in deck_folders:
        folder_path = os.path.join(options.input, folder)
        files = fnmatch.filter(os.listdir(folder_path), "*.txt")

        if len(files) > 0:
            generate_deck(folder_path, files, folder)

    for file in fnmatch.filter(deck_files, "*.txt"):
        generate_deck(options.input, [file], os.path.splitext(file)[0])

def generate_deck(input_directory, files, name):
    output_filepath = os.path.join(options.output, f'{name}.apkg')
    
    anki = Anki()

    for file in files:
        entries = open(os.path.join(input_directory, file)).read().splitlines()

        for index, entry in enumerate(entries, start=1):
           if '\t' in entry:
               anki.generate_note(entry)
           elif '~~~' in entry:
               anki.generate_deck(entry)
           elif not entry or entry.startswith('#'):
               continue
           else:
               raise Exception(f'Unknown Line Type {file}#{index}')

    anki.generate_package(output_filepath)

process()