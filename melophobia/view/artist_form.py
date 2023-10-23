import logging
from typing import get_args

from sqlalchemy import select
from sqlalchemy.orm import Session
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Footer, Label, Input, Static, Switch, Button, Select, Rule, SelectionList

from melophobia.component.SubmitLabel import SubmitLabel
from melophobia.config import DB_ENGINE
from melophobia.enum import ArtistType
from melophobia.model import Location, Genre

logging.basicConfig(filename='melophobia.log', encoding='utf-8', format='%(asctime)s %(levelname)s:%(message)s',
                    level=logging.DEBUG)


class ArtistFormScreen(Screen):
    BINDINGS = [Binding('q', 'app.pop_screen', 'Return to artists list')]

    def compose(self) -> ComposeResult:
        db_session = Session(DB_ENGINE)

        location_query = select(Location).order_by(Location.city.asc())
        genre_query = select(Genre).order_by(Genre.name.asc())

        formation_location_opts = []
        location_idx = 1

        genre_opts = []
        genre_idx = 1

        artist_type_opts = []
        artist_type_idx = 1

        for location in db_session.scalars(location_query):
            formation_location_opts.append(('{}, {}, {}'.format(
                location.city, location.region.name, location.region.country.country_name), location_idx))

            location_idx = location_idx + 1

        for genre in db_session.scalars(genre_query):
            genre_opts.append((genre.name, genre_idx))

            genre_idx = genre_idx + 1

        for artist_type in get_args(ArtistType):
            artist_type_opts.append((artist_type, artist_type_idx))

            artist_type_idx = artist_type_idx + 1

        yield Vertical(
            Rule(line_style='heavy'),
            Label('ADD ARTIST', id='title'),
            Rule(line_style='heavy'),

            # Name
            Horizontal(
                Static('Name:', classes='form-label'),
                Input(classes='form-input form-element'),
                classes='form-container'
            ),

            # Genre(s)
            Horizontal(
                Static('Genre(s):', classes='form-label'),
                SelectionList(*genre_opts, id='artist-genre', classes='form-input form-element form-selectionlist'),
                classes='form-container'
            ),

            # Formation date
            Horizontal(
                Static('Formation Date:', classes='form-label'),
                Input(placeholder='YYYY-MM-DD', classes='form-input form-element'),
                classes='form-container'
            ),

            # Formation location
            Horizontal(
                Static('Formation Location:', classes='form-label'),
                Select(formation_location_opts, id='artist-formation-location',
                       classes='form-input form-element form-dropdown-override'),
                classes='form-container'
            ),

            # Disband date
            Horizontal(
                Static('Disband Date:', classes='form-label'),
                Input(placeholder='YYYY-MM-DD', classes='form-input form-element'),
                classes='form-container'
            ),

            # Favourite
            Horizontal(
                Static('Favourite:', classes='form-label'),
                Switch(classes='form-element'),
                classes='form-container'
            ),

            # Artist type
            Horizontal(
                Static('Artist Type:', classes='form-label'),
                Select(artist_type_opts, id='artist-type',
                       classes='form-input form-element form-dropdown-override'),
                classes='form-container'
            ),

            # ISNI
            Horizontal(
                Static('ISNI:', classes='form-label'),
                Input(placeholder='ISNI', classes='form-input form-element'),
                classes='form-container'
            ),

            Horizontal(
                SubmitLabel(id='submit-label', classes='form-label'),
                Button('Submit', classes='form-submit', variant='primary'),
                classes='submit-container'
            ),

            classes='medium-container'
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        submit_label = self.query_one(SubmitLabel)
        submit_label.update_text(True)
        submit_label.add_class('text-success')
