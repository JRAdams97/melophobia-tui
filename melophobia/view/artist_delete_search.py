from sqlalchemy import select
from sqlalchemy.orm import Session
from textual.app import ComposeResult
from textual.containers import Grid, Vertical
from textual.screen import ModalScreen
from textual.widgets import Select, Button, Static

from melophobia.config import DB_ENGINE
from melophobia.model import Artist


class ArtistDeleteSearchScreen(ModalScreen[bool]):

    def compose(self) -> ComposeResult:
        db_session = Session(DB_ENGINE)
        query = select(Artist).order_by(Artist.name.asc())

        artists = []
        artist_idx = 1

        for artist in db_session.scalars(query):
            artists.append((artist.name, artist_idx))

            artist_idx = artist_idx + 1

        yield Vertical(
            Static('Choose an artist:', classes='dialog-header'),
            Grid(
                Select(artists, classes='dialog-span dialog-select'),
                Button('Delete', variant='primary', id='delete', classes='dialog-button'),
                Button('Cancel', variant='default', id='cancel', classes='dialog-button'),
                id='dialog'
            ),
            classes='dialog-container'
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'cancel':
            self.dismiss(True)

        else:
            self.app.push_screen('artist_form')
