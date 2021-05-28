import genanki
import os.path

from .options import values as options
from . import util, diagram

class StenoNote(genanki.Note):
    @property
    def guid(self):
        return genanki.guid_for(self.tags, self.fields[0])

media = [];
decks = [];
current_deck = None

steno_model = genanki.Model(
    util.generate_identifier('Steno'),
    'Steno',
    fields=[
        {'name': 'Translation'},
        {'name': 'Diagram'}
    ],
    templates=[
        {
            'name': 'Steno Card 1',
            'qfmt': '{{Translation}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Diagram}}'
        },
        {
            'name': 'Steno Card 2',
            'qfmt': '{{Diagram}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Translation}}'
        }
    ],
    css='.card { font-family: arial; font-size: 20px; text-align: center; color: black; background-color: white; }'
)

def generate_package():
    package = genanki.Package(decks)
    package.media_files = media
    package.write_to_file(options.output)

def generate_deck(entry):
    title, id_string = map(lambda s: s.strip(), entry.split('~~~'))
    id = util.generate_identifier(id_string)

    print([title, id_string, id])

    global current_deck
    current_deck = genanki.Deck(id, title)
    decks.append(current_deck)

def generate_note(entry):
    if current_deck is None:
        raise Exception('Must define a deck first')

    translation, outline = util.split_strip(entry, '|||')
    diagrams_html = ''

    for chord in util.split_strip(outline, '/'):
        filename = diagram.download(chord)

        media.append(os.path.join(options.diagrams, filename))
        diagrams_html += f'<img src="{filename}" />'

    current_deck.add_note(
        StenoNote(
            model=steno_model,
            fields=[translation, diagrams_html]
        )
    )