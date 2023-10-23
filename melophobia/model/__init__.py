from typing import get_args, Optional, List

from sqlalchemy import CHAR, Enum, String, Table, Column, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

import melophobia.enum as enum


class Base(DeclarativeBase):
    pass


# Association tables
artist_genres = Table('artist_genres', Base.metadata,
                      Column('artist_id', ForeignKey('artist.artist_id')),
                      Column('genre_id', ForeignKey('genre.genre_id')), )


# Base tables
class Country(Base):
    __tablename__ = 'country'

    country_id: Mapped[int] = mapped_column(primary_key=True)
    country_name: Mapped[str] = mapped_column(unique=True)
    alpha_2_code: Mapped[str] = mapped_column(CHAR(2), unique=True)
    country_continent: Mapped[enum.Continent] = mapped_column(Enum(*get_args(enum.Continent), name='country_continent',
                                                                   create_constraint=True, validate_string=True))

    regions: Mapped[List["Region"]] = relationship(back_populates='country')

    def __repr__(self) -> str:
        return f"Country(country_id={self.country_id!r}, name={self.country_name!r})"


class Region(Base):
    __tablename__ = 'region'

    region_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column()
    region_abbr: Mapped[Optional[str]] = mapped_column(String(30))
    country_id: Mapped[int] = mapped_column(ForeignKey("country.country_id"))

    country: Mapped["Country"] = relationship(back_populates='regions')
    locations: Mapped[List["Location"]] = relationship(back_populates='region')

    def __repr__(self) -> str:
        return f"Region(region_id={self.region_id!r}, name={self.name!r}), abbr={self.region_abbr!r})"


class Location(Base):
    __tablename__ = 'location'

    location_id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column()
    region_id: Mapped[int] = mapped_column(ForeignKey('region.region_id'))

    region: Mapped["Region"] = relationship(back_populates='locations')
    artists: Mapped[List["Artist"]] = relationship(back_populates='formation_location')

    def __repr__(self) -> str:
        return f"Location(location_id={self.location_id!r}, city={self.city!r}))"


class Genre(Base):
    __tablename__ = 'genre'

    genre_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    origin_year: Mapped[int] = mapped_column()
    favourite: Mapped[bool] = mapped_column(default=False)

    def __repr__(self) -> str:
        return f"Genre(genre_id={self.genre_id!r}, name={self.name!r})"


class Artist(Base):
    __tablename__ = 'artist'

    artist_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    formation_date: Mapped[str] = mapped_column(CHAR(10), default='0000-00-00')
    formation_location_id: Mapped[int] = mapped_column(ForeignKey('location.location_id'))
    disband_date: Mapped[Optional[str]] = mapped_column(CHAR(10))
    favourite: Mapped[bool] = mapped_column(default=False)
    artist_type: Mapped[enum.ArtistType] = mapped_column(Enum(*get_args(enum.ArtistType), name='artist_type',
                                                              create_constraint=True, validate_string=True))
    isni: Mapped[Optional[str]] = mapped_column(CHAR(19), unique=True)

    formation_location: Mapped["Location"] = relationship(back_populates='artists')
    genres: Mapped[List[Genre]] = relationship(secondary=artist_genres)

    def __repr__(self) -> str:
        return f"Artist(artist_id={self.artist_id!r}, name={self.name!r}, isni={self.isni!r})"
