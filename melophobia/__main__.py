from melophobia.artist import list_artist
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Tabs, Label, DataTable, Tab

NAV_TABS = [
    "Artists",
    "Collections",
    "Composers",
    "Countries",
    "Genres",
    "Issues",
    "Labels",
    "Languages",
    "Locations",
    "Media",
    "Moods",
    "Producers",
    "Releases",
    "Series",
    "Tracks"
]


class Melophobia(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    CSS_PATH = "resources/melophobia.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Tabs("⌂")
        yield Label()
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        tabs = self.query_one(Tabs)

        for tab in NAV_TABS:
            tabs.add_tab(Tab(tab, id=tab.lower()))

        tabs.focus()

        list_artist.on_mount(self.query_one(DataTable))

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        label = self.query_one(Label)
        table = self.query_one(DataTable)

        if event.tab is None:
            label.display = False
            table.display = False

        elif event.tab.id == "artists":
            list_artist.on_activation(label, table)

        else:
            label.display = True
            label.update(event.tab.label)
            table.display = False

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark


if __name__ == "__main__":
    app = Melophobia()
    app.run()
