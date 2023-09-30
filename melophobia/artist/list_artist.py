# Example artist table (use until database integration completed)
ARTIST_TABLE = [
    ("artist_id", "name", "genre(s)", "formation_country", "favourite", "artist_type", "release_#", "isni", "edit",
     "delete"),
    (1, "Wilco", "Alt. Country / Alt. Rock / Americana / Art Rock / Folk Rock / Indie Rock", "US", "★", "Band", "12",
     "0000 0001 1523 0122", "✎", "🗑"),
    (2, "Nirvana", "Acoustic Rock / Alt. Rock / Grunge / Noise Rock", "US", "☆", "Band", "8", "", "✎", "🗑"),
    (3, "Guided By Voices", "Indie Rock / Lo-Fi Indie / Power Pop", "US", "★", "Band", "47", "", "✎", "🗑"),
    (4, "Church, The", "Alt. Rock / Art Rock / Dream Pop / Jangle Pop / Neo-Psy / Post-Punk", "NZ", "☆", "Band", "19",
     "", "✎", "🗑")
]


def on_mount(table):
    table.add_columns(*ARTIST_TABLE[0])
    table.add_rows(ARTIST_TABLE[1:])


def on_activation(label, table):
    label.display = False
    table.display = True
