import logging

from sqlalchemy import select
from sqlalchemy.orm import Session
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Footer, DataTable, Rule, Label

from melophobia.config import DB_ENGINE
from melophobia.model import Artist

# Example artist table (use until database integration completed)
ARTIST_HEADER = ("Name", "Genre(s)", "Formation Country", "Favourite", "Artist Type", "Release Count", "ISNI", "Edit",
                 "Delete")

logging.basicConfig(filename='melophobia.log', encoding='utf-8', format='%(asctime)s %(levelname)s:%(message)s',
                    level=logging.DEBUG)


class ListArtistsScreen(Screen):
    BINDINGS = [('n', "push_screen('artist_form')", 'Create new item'),
                ('q', 'app.pop_screen', 'Return to main menu')]

    def compose(self) -> ComposeResult:
        yield Vertical(
            Rule(line_style='heavy'),
            Label('ARTISTS', id='title'),
            Rule(line_style='heavy'),
            DataTable(),
            classes='table-container'
        )
        yield Footer()

    def on_mount(self) -> None:
        db_session = Session(DB_ENGINE)
        query = select(Artist)

        table = self.query_one(DataTable)
        table.add_columns(*ARTIST_HEADER)

        artists = []

        for artist in db_session.scalars(query):
            genre_str = ''

            for genre in artist.genres:
                if genre == artist.genres[-1]:
                    genre_str = genre_str + genre.name

                else:
                    genre_str = genre_str + genre.name + ' / '

            artists.append((artist.name, genre_str, artist.formation_location.region.country.country_name,
                            artist.favourite, artist.artist_type, 0, artist.isni, '✎', '🗑'))

        logging.info(artists)

        table.add_rows(artists[0:])
