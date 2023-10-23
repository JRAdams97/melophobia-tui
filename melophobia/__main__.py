from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Footer, Label, ListView, Rule

import melophobia.view.artist_form
import melophobia.view.list_artists
from melophobia.component.Labelitem import LabelItem


class Melophobia(App):
    BINDINGS = [('q', 'quit', 'Quit the app')]
    CSS_PATH = "resources/melophobia.tcss"

    def compose(self) -> ComposeResult:
        yield Vertical(
            Rule(line_style='heavy'),
            Label('MELOPHOBIA', id='title'),
            Rule(line_style='heavy'),
            ListView(
                LabelItem('Artists'),
                LabelItem('Collections'),
                LabelItem('Composers'),
                LabelItem('Genres'),
                LabelItem('Issues'),
                LabelItem('Labels'),
                LabelItem('Languages'),
                LabelItem('Locations'),
                LabelItem('Media'),
                LabelItem('Producers'),
                LabelItem('Releases'),
                LabelItem('Series'),
                LabelItem('Tracks'),
                LabelItem('Vendors'),
                classes='title-list'
            ),
            classes='small-container'
        )
        yield Footer()

    def on_mount(self) -> None:
        self.install_screen(melophobia.view.list_artists.ListArtistsScreen(), name='list_artists')
        self.install_screen(melophobia.view.artist_form.ArtistFormScreen(), name='artist_form')

    def on_list_view_selected(self, event: ListView.Selected):
        if event.item.label == 'Artists':
            app.push_screen('list_artists')


if __name__ == "__main__":
    app = Melophobia()
    app.run()
