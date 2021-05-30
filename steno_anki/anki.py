import genanki
import os.path

from options import values as options
import util, diagram

class StenoNote(genanki.Note):
    @property
    def guid(self):
        return genanki.guid_for(self.tags, self.fields[0])

class Anki:
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

    def __init__(self):
        self.media = [];
        self.decks = [];
        self.current_deck = None

    

    def generate_package(self):
        package = genanki.Package(self.decks)
        package.media_files = self.media
        package.write_to_file(options.output)

    def generate_deck(self, entry):
        title, id_string = map(lambda s: s.strip(), entry.split('~~~'))
        id = util.generate_identifier(id_string)

        print([title, id_string, id])

        self.current_deck = genanki.Deck(id, title)
        self.decks.append(self.current_deck)

    def generate_note(self, entry):
        if self.current_deck is None:
            raise Exception('Must define a deck first')

        translation, outline = util.split_strip(entry, '|||')
        diagrams_html = ''

        for chord in util.split_strip(outline, '/'):
            filename = diagram.download(chord)

            self.media.append(os.path.join(options.diagrams, filename))
            diagrams_html += f'<img src="{filename}" />'

        self.current_deck.add_note(
            StenoNote(
                model=Anki.steno_model,
                fields=[translation, diagrams_html]
            )
        )
