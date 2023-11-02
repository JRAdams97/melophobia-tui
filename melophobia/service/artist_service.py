import logging

from sqlalchemy import select
from sqlalchemy.orm import Session, aliased

from melophobia.config import DB_ENGINE
from melophobia.model import Artist, Genre, Location, Region, Country

logging.basicConfig(filename='melophobia.log', encoding='utf-8', format='%(asctime)s %(levelname)s:%(message)s',
                    level=logging.WARNING)


def create_artist(name: str, genres: list[str], formation_date: str, formation_location: str, disband_date: str,
                  favourite: bool, artist_type: str, isni: str):

    logging.warning('[GENRES] %s', genres)

    artist = Artist(name=name, formation_date=formation_date, disband_date=disband_date, favourite=favourite,
                    artist_type=artist_type, isni=isni)

    db_session = Session(DB_ENGINE)

    split_location = formation_location.split(', ')

    region_alias = aliased(Region)
    country_alias = aliased(Country)

    formation_location_res = db_session.scalars(select(Location)
                                                .join(region_alias, Location.region)
                                                .where(region_alias.name == split_location[1])
                                                .join(country_alias, Region.country)
                                                .where(country_alias.country_name == split_location[2])
                                                .where(Location.city == split_location[0])).first()

    if formation_location_res is not None:
        artist.formation_location = formation_location_res

    genres_result = db_session.query(Genre).filter(Genre.name.in_(genres)).all()

    artist.genres = [genre for genre in genres_result]

    db_session.add(artist)
    db_session.commit()
