import os
from src import helpers

directory = os.path.abspath(helpers.options.input)
files = os.listdir(directory)

print(files)

for file in files:
    entries = open(os.path.join(directory, file)).read().splitlines()

    for index, entry in enumerate(entries, start=1):
        if '|||' in entry:
            helpers.anki.generate_note(entry)
        elif '~~~' in entry:
            helpers.anki.generate_deck(entry)
        elif not entry or entry.startswith('#'):
            continue
        else:
            raise Exception(f'Unknown Line Type {file}#{index}')

helpers.anki.generate_package()
