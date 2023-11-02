from typing import get_args

from sqlalchemy import select
from sqlalchemy.orm import Session
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.validation import Regex, Length, ValidationResult
from textual.widgets import Footer, Label, Input, Static, Switch, Button, Select, Rule, SelectionList

from melophobia.component.label_submit import LabelSubmit
from melophobia.component.label_validation import LabelValidation
from melophobia.config import DB_ENGINE
from melophobia.enum import ArtistType
from melophobia.model import Location, Genre
from melophobia.service.artist_service import create_artist


class ArtistFormScreen(Screen):
    BINDINGS = [Binding('q', 'app.pop_screen', 'Return to artists list')]

    genre_opts = []
    formation_location_opts = []
    artist_type_opts = []

    def compose(self) -> ComposeResult:
        db_session = Session(DB_ENGINE)

        location_query = select(Location).order_by(Location.city.asc())
        genre_query = select(Genre).order_by(Genre.name.asc())

        genre_idx = 0
        location_idx = 0
        artist_type_idx = 0

        for location in db_session.scalars(location_query):
            abbr = location.region.region_abbr

            self.formation_location_opts.append((
                '{}, {}, {}'.format(location.city, abbr if abbr is not None else location.region.name,
                                    location.region.country.country_name), location_idx))

            location_idx = location_idx + 1

        for genre in db_session.scalars(genre_query):
            self.genre_opts.append((genre.name, genre_idx))

            genre_idx = genre_idx + 1

        for artist_type in get_args(ArtistType):
            self.artist_type_opts.append((artist_type, artist_type_idx))

            artist_type_idx = artist_type_idx + 1

        yield Vertical(
            Rule(line_style='heavy'),
            Label('ADD ARTIST', id='title'),
            Rule(line_style='heavy'),

            # Name
            Horizontal(
                Static('Name:', classes='form-label-alt'),
                Static('*', classes='form-required-label'),
                Input(validators=Length(minimum=1), id='name', classes='form-input form-element'),
                classes='form-container'
            ),
            LabelValidation(id='name-validation', classes='form-validation text-error'),

            # Genre(s)
            Horizontal(
                Static('Genre(s):', classes='form-label'),
                SelectionList(*self.genre_opts, id='artist-genre', classes='form-input form-element form-selectionlist'),
                classes='form-container'
            ),

            # Formation date
            Horizontal(
                Static('Formation Date:', classes='form-label'),
                Input('0000-00-00', validators=Regex('\d{4}-\d{2}-\d{2}'), id='formation-date',
                      placeholder='YYYY-MM-DD', classes='form-input form-element'),
                classes='form-container'
            ),
            LabelValidation(id='formation-date-validation', classes='form-validation text-error'),

            # Formation location
            Horizontal(
                Static('Formation Location:', classes='form-dropdown-label'),
                Select(self.formation_location_opts, id='artist-formation-location', classes='form-input form-element'),
                classes='form-container'
            ),

            # Disband date
            Horizontal(
                Static('Disband Date:', classes='form-label'),
                Input(validators=Regex('^$|\d{4}-\d{2}-\d{2}'), placeholder='YYYY-MM-DD', id='disband-date',
                      classes='form-input form-element'),
                classes='form-container'
            ),
            LabelValidation(id='disband-date-validation', classes='form-validation text-error'),

            # Favourite
            Horizontal(
                Static('Favourite:', classes='form-label'),
                Switch(id='favourite', classes='form-element'),
                classes='form-container'
            ),

            # Artist type
            Horizontal(
                Static('Artist Type:', classes='form-dropdown-label-alt'),
                Static('*', classes='form-dropdown-required-label'),
                Select(self.artist_type_opts, id='artist-type', classes='form-input form-element'),
                classes='form-dropdown-container'
            ),
            LabelValidation(id='artist-type-validation', classes='form-validation text-error'),

            # ISNI
            Horizontal(
                Static('ISNI:', classes='form-label'),
                Input(validators=Regex('^$|\d{4} \d{4} \d{4} \d{4}'), placeholder='ISNI', id='isni',
                      classes='form-input form-element'),
                classes='form-container'
            ),
            LabelValidation(id='isni-validation', classes='form-validation text-error'),

            Horizontal(
                LabelSubmit(id='submit-label', classes='form-label'),
                Button('Submit', classes='form-submit', variant='primary'),
                classes='submit-container'
            ),
            classes='medium-container'
        )
        yield Footer()

    def on_button_pressed(self) -> None:
        name = self.query_one('#name', expect_type=Input)
        name_validation_results = name.validate(name.value)

        formation_date = self.query_one('#formation-date', expect_type=Input)
        formation_date_validation_results = formation_date.validate(formation_date.value)

        disband_date = self.query_one('#disband-date', expect_type=Input)
        disband_date_validation_results = disband_date.validate(disband_date.value)

        isni = self.query_one('#isni', expect_type=Input)
        isni_validation_results = isni.validate(isni.value)

        artist_type = self.query_one('#artist-type', expect_type=Select)

        is_valid_name = self.check_input_validation('#name', name_validation_results, 'Value required')
        is_valid_formation_date = self.check_input_validation('#formation-date', formation_date_validation_results,
                                                              "Invalid format (expected 'YYYY-MM-DD')")
        is_valid_disband_date = self.check_input_validation('#disband-date', disband_date_validation_results,
                                                            "Invalid format (expected 'YYYY-MM-DD')")
        is_valid_isni = self.check_input_validation('#isni', isni_validation_results,
                                                    "Invalid format (expected '#### #### #### ####')")

        is_valid_artist_type = self.check_dropdown_validation('#artist-type', artist_type.value, 'Value required')

        if (is_valid_name and is_valid_formation_date and is_valid_disband_date and is_valid_isni
                and is_valid_artist_type):
            genres = self.query_one('#artist-genre', expect_type=SelectionList)
            formation_location = self.query_one('#artist-formation-location', expect_type=Select)

            genre_list = []

            if genres.selected:
                for opt in self.genre_opts:
                    if opt[1] in genres.selected:
                        genre_list.append(opt[0])

            formation_location_str = ''

            if formation_location is not None:
                for opt in self.formation_location_opts:
                    if opt[1] == formation_location.value:
                        formation_location_str = opt[0]

            artist_type_str = ''

            for opt in self.artist_type_opts:
                if opt[1] == artist_type.value:
                    artist_type_str = opt[0]

            favourite = self.query_one('#favourite', expect_type=Switch)

            create_artist(name.value, genre_list, formation_date.value, formation_location_str, disband_date.value,
                          favourite.value, artist_type_str, isni.value)

            self.app.pop_screen()

    def check_input_validation(self, validation_label_id: str, validation_results: ValidationResult,
                               error_text: str) -> bool:
        validation_label = self.query_one('{}-validation'.format(validation_label_id), expect_type=LabelValidation)

        if not validation_results.is_valid:
            validation_label.update_text(error_text)

            return False

        else:
            validation_label.update_text('')

        return True

    def check_dropdown_validation(self, validation_label_id: str, value: int, error_text: str):
        validation_label = self.query_one('{}-validation'.format(validation_label_id), expect_type=LabelValidation)
        artist_type = self.query_one(validation_label_id)

        if value is None:
            artist_type.add_class('dropdown-error')
            validation_label.update_text(error_text)

            return False

        else:
            artist_type.remove_class('dropdown-error')
            validation_label.update_text('')

        return True
