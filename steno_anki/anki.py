import genanki
import util

class StenoNote(genanki.Note):
    @property
    def guid(self):
        return genanki.guid_for(self.fields[0])

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
                'qfmt': '{{Translation}}<br>{{type:Outline}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Diagram}}'
            },
            {
                'name': 'Steno Card 2',
                'qfmt': '{{Diagram}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Translation}}'
            }
        ],
        css=
"""
@font-face { 
    font-family: "Stenodisplay-ClassicLarge";
    src: url("_Stenodisplay-ClassicLarge.ttf");
} 
.card { 
    font-family: arial; 
    font-size: 20px; 
    text-align: center; 
} 
.steno { 
    font-family: "Stenodisplay-ClassicLarge";
    font-size: 168px;
    color: #008080;
    white-space: nowrap;
}
.typeGood,
.nightMode .typeGood,
.night_mode .typeGood
 {
    background-color: #008080;
    color: white;
}
.typeBad, 
.typeMissed,
.nightMode .typeBad,
.nightMode .typeMissed,
.night_mode .typeBad,
.night_mode .typeMissed {
    background-color: #800000;
    color: white;
}
"""
    )

    def __init__(self):
        self.decks = [];
        self.current_deck = None

    def generate_package(self, output):
        package = genanki.Package(self.decks)
        package.media_files = ["_Stenodisplay-ClassicLarge.ttf"]
        package.write_to_file(output)

    def generate_deck(self, entry):
        title, id_string = map(lambda s: s.strip(), entry.split('~~~'))
        id = util.generate_identifier(id_string)

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
