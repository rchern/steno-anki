import genanki

from options import values as options
import util

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
            {'name': 'Outline'},
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
        css=
"""@font-face { 
    font-family: "StenoDisplay-LetterFont"; 
    src: url("_StenoDisplay-LetterFont.ttf"); 
} 
.card { 
    font-family: arial; 
    font-size: 20px; 
    text-align: center; 
} 
.steno { 
    font-family: "StenoDisplay-LetterFont"; 
    font-size: 128px; 
    color: teal;
}"""
    )

    def __init__(self):
        self.decks = [];
        self.current_deck = None

    

    def generate_package(self):
        print('Generating package')

        package = genanki.Package(self.decks)
        package.media_files = ["_StenoDisplay-LetterFont.ttf"]
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

        translation, outline = util.split_strip(entry, '\t')
        diagrams_html = ''

        for chord in util.split_strip(outline, '/'):
            diagrams_html += f'<div class="steno">{chord}</div>'

        self.current_deck.add_note(
            StenoNote(
                model=Anki.steno_model,
                fields=[translation, outline, diagrams_html]
            )
        )
