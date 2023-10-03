--============================================================================
-- TABLE DEFINITIONS
--============================================================================
CREATE TABLE country (
         country_id INTEGER PRIMARY KEY AUTOINCREMENT,
       country_name VARCHAR(42) UNIQUE NOT NULL,
       alpha_2_code CHAR(2) UNIQUE NOT NULL,
  country_continent VARCHAR(13) NOT NULL
);

CREATE TABLE region (
    region_id INTEGER PRIMARY KEY AUTOINCREMENT,
         name TEXT,
  region_abbr VARCHAR(30),
   country_id INTEGER,
              CONSTRAINT FK_country__region FOREIGN KEY (country_id) REFERENCES country (country_id)
);

CREATE TABLE location (
  location_id INTEGER PRIMARY KEY AUTOINCREMENT,
         city TEXT NOT NULL,
    region_id INTEGER,
              CONSTRAINT FK_region__location FOREIGN KEY (region_id) REFERENCES region (region_id)
);

CREATE TABLE artist (
              artist_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
         formation_date CHAR(10) DEFAULT '0000-00-00',
  formation_location_id INTEGER,
           disband_date CHAR(10),
              favourite BOOLEAN DEFAULT FALSE,
            artist_type TEXT NOT NULL,
                   isni CHAR(19) UNIQUE,
                        CONSTRAINT FK_location__artist FOREIGN KEY (formation_location_id) REFERENCES location (location_id)
);

CREATE TABLE genre (
     genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
         name TEXT UNIQUE NOT NULL,
  origin_year SMALLINT NOT NULL,
    favourite BOOLEAN DEFAULT FALSE NOT NULL
);

CREATE TABLE genre_hierarchy (
         genre_id INTEGER,
  parent_genre_id INTEGER,
                  PRIMARY KEY (genre_id, parent_genre_id),
                  CONSTRAINT FK_genre__genre_id FOREIGN KEY (genre_id) REFERENCES genre (genre_id),
                  CONSTRAINT FK_genre__parent_genre_id FOREIGN KEY (parent_genre_id) REFERENCES genre (genre_id)
);

CREATE TABLE artist_genres (
  artist_id INTEGER,
   genre_id INTEGER,
            PRIMARY KEY (artist_id, genre_id),
            CONSTRAINT FK_artist__artist_genres FOREIGN KEY (artist_id) REFERENCES artist (artist_id),
            CONSTRAINT FK_genre__artist_genres FOREIGN KEY (genre_id) REFERENCES genre (genre_id)
);

CREATE TABLE composer (
        composer_id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
         birth_date CHAR(10) DEFAULT '0000-00-00',
  birth_location_id INTEGER,
         death_date CHAR(10),
                    CONSTRAINT FK_location_composer FOREIGN KEY (birth_location_id) REFERENCES location (location_id)
);

CREATE TABLE label (
               label_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
         formation_date CHAR(10) DEFAULT '0000-00-00',
  formation_location_id INTEGER,
           closing_date CHAR(10),
              favourite BOOLEAN DEFAULT FALSE,
             label_code CHAR(8),
                        CONSTRAINT FK_location__label FOREIGN KEY (formation_location_id) REFERENCES location (location_id)
);

CREATE TABLE media (
        media_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
      media_abbr VARCHAR(20),
  classification VARCHAR(50) NOT NULL,
     origin_year SMALLINT
);

CREATE TABLE producer (
        producer_id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
         birth_date CHAR(10) DEFAULT '0000-00-00',
  birth_location_id INTEGER,
         death_date CHAR(10),
                    CONSTRAINT FK_location__producer FOREIGN KEY (birth_location_id) REFERENCES location (location_id)
);

CREATE TABLE vendor (
    vendor_id INTEGER PRIMARY KEY AUTOINCREMENT,
         name TEXT NOT NULL,
      address TEXT NOT NULL,
     postcode VARCHAR(10) NOT NULL,
  location_id INTEGER,
  description VARCHAR(255),
              CONSTRAINT FK_location__vendor FOREIGN KEY (location_id) REFERENCES location (location_id)
);

CREATE TABLE purchase (
    purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
          price NUMERIC NOT NULL,
  currency_code CHAR(3) DEFAULT 'USD',
      vendor_id INTEGER,
                CONSTRAINT FK_vendor__purchase FOREIGN KEY (vendor_id) REFERENCES vendor (vendor_id)
);

CREATE TABLE series (
    series_id INTEGER PRIMARY KEY AUTOINCREMENT,
         name TEXT NOT NULL,
  origin_year SMALLINT,
   country_id INTEGER,
              CONSTRAINT FK_country__series FOREIGN KEY (country_id) REFERENCES country (country_id)
);

CREATE TABLE release (
        release_id INTEGER PRIMARY KEY AUTOINCREMENT,
             title TEXT NOT NULL,
      release_date CHAR(10) DEFAULT '0000-00-00',
         favourite BOOLEAN DEFAULT FALSE,
        rym_rating NUMERIC(3, 2),
         aoty_rank SMALLINT,
          bea_rank SMALLINT,
  christgau_rating CHAR(3),
   scaruffi_rating NUMERIC(2, 1),
  pitchfork_rating FLOAT(2, 1),
        metacritic SMALLINT,
       is_official BOOLEAN NOT NULL
);

CREATE TABLE release_artists (
  release_id INTEGER,
   artist_id INTEGER,
             PRIMARY KEY (release_id, artist_id),
             CONSTRAINT FK_release__release_artists FOREIGN KEY (release_id) REFERENCES release (release_id),
             CONSTRAINT FK_artist__release_artists FOREIGN KEY (artist_id) REFERENCES artist (artist_id)
);

CREATE TABLE release_genres (
  release_id INTEGER,
    genre_id INTEGER,
             PRIMARY KEY (release_id, genre_id),
             CONSTRAINT FK_release__release_genres FOREIGN KEY (release_id) REFERENCES release (release_id),
             CONSTRAINT FK_genre__release_genres FOREIGN KEY (genre_id) REFERENCES genre (genre_id)
);

CREATE TABLE release_languages (
   release_id INTEGER,
     language VARCHAR(50),
              PRIMARY KEY (release_id, language),
              CONSTRAINT FK_release__release_languages FOREIGN KEY (release_id) REFERENCES release (release_id)
);

CREATE TABLE release_producers (
   release_id INTEGER,
  producer_id INTEGER,
              PRIMARY KEY (release_id, producer_id),
              CONSTRAINT FK_release__release_producers FOREIGN KEY (release_id) REFERENCES release (release_id),
              CONSTRAINT FK_producer__release_producers FOREIGN KEY (producer_id) REFERENCES producer (producer_id)
);

CREATE TABLE release_series (
  release_id INTEGER,
   series_id INTEGER,
             PRIMARY KEY (release_id, series_id),
             CONSTRAINT FK_release__release_series FOREIGN KEY (release_id) REFERENCES release (release_id),
             CONSTRAINT FK_series__release_series FOREIGN KEY (series_id) REFERENCES series (series_id)
);

CREATE TABLE release_types (
    release_id INTEGER,
  release_type VARCHAR(50),
               PRIMARY KEY(release_id, release_type),
               CONSTRAINT FK_release__release_types FOREIGN KEY (release_id) REFERENCES release (release_id)
);

CREATE TABLE collection_digital (
  d_collection_id INTEGER PRIMARY KEY AUTOINCREMENT,
       release_id INTEGER,
         media_id INTEGER,
     total_tracks SMALLINT NOT NULL,
   missing_tracks SMALLINT DEFAULT 0,
      total_discs SMALLINT NOT NULL,
    missing_discs SMALLINT DEFAULT 0,
      art_quality VARCHAR(20) NOT NULL,
      tag_quality VARCHAR(20) NOT NULL,
           status VARCHAR(20) NOT NULL,
      description TEXT,
                  CONSTRAINT FK_release__collection_digital FOREIGN KEY (release_id) REFERENCES release (release_id),
                  CONSTRAINT FK_media__collection_digital FOREIGN KEY (media_id) REFERENCES media (media_id)
);

CREATE TABLE issue (
        issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
        label_id INTEGER,
      release_id INTEGER,
    release_date CHAR(10) DEFAULT '0000-00-00',
    catalogue_id VARCHAR(30) NOT NULL,
         edition VARCHAR(50),
    is_rerelease BOOLEAN NOT NULL,
     is_official BOOLEAN,
         barcode TEXT,
        media_id INTEGER,
   matrix_runout TEXT,
     description TEXT,
                 CONSTRAINT FK_label__issue FOREIGN KEY (label_id) REFERENCES label (label_id),
                 CONSTRAINT FK_release__issue FOREIGN KEY (release_id) REFERENCES release (release_id),
                 CONSTRAINT FK_media__issue FOREIGN KEY (media_id) REFERENCES media (media_id)
);

CREATE TABLE issue_countries (
    issue_id INTEGER,
  country_id INTEGER,
             PRIMARY KEY(issue_id, country_id),
             CONSTRAINT FK_issue__issue_countries FOREIGN KEY (issue_id) REFERENCES issue (issue_id),
             CONSTRAINT FK_country__issue_countries FOREIGN KEY (country_id) REFERENCES country (country_id)
);

CREATE TABLE collection_physical (
    p_collection_id INTEGER PRIMARY KEY AUTOINCREMENT,
           issue_id INTEGER,
           media_id INTEGER,
  packaging_quality VARCHAR(20) NOT NULL,
      media_quality VARCHAR(20),
        purchase_id INTEGER,
        description TEXT,
                    CONSTRAINT FK_issue__collection_physical FOREIGN KEY (issue_id) REFERENCES issue (issue_id),
                    CONSTRAINT FK_media__collection_physical FOREIGN KEY (media_id) REFERENCES media (media_id),
                    CONSTRAINT FK_purchase__collection_physical FOREIGN KEY (purchase_id) REFERENCES purchase (purchase_id)
);

CREATE TABLE track (
          track_id INTEGER PRIMARY KEY AUTOINCREMENT,
             title TEXT NOT NULL,
  first_release_id INTEGER,
         favourite BOOLEAN DEFAULT FALSE,
        track_type VARCHAR(50) NOT NULL,
                   CONSTRAINT FK_release__track FOREIGN KEY (first_release_id) REFERENCES release (release_id)
);

CREATE TABLE track_composers (
     track_id INTEGER,
  composer_id INTEGER,
              PRIMARY KEY(track_id, composer_id),
              CONSTRAINT FK_track__track_composers FOREIGN KEY (track_id) REFERENCES track (track_id),
              CONSTRAINT FK_composer__track_composers FOREIGN KEY (composer_id) REFERENCES composer (composer_id)
);

CREATE TABLE track_isrc (
  track_id INTEGER,
      isrc CHAR(15),
           PRIMARY KEY(track_id, isrc),
           CONSTRAINT FK_track__track_isrc FOREIGN KEY (track_id) REFERENCES track (track_id)
);

CREATE TABLE track_iswc (
  track_id INTEGER,
      iswc CHAR(15) NOT NULL,
           PRIMARY KEY(track_id, iswc),
           CONSTRAINT FK_track__track_iswc FOREIGN KEY (track_id) REFERENCES track (track_id)
);

CREATE TABLE track_original_artists (
   track_id INTEGER,
  artist_id INTEGER,
            PRIMARY KEY(track_id, artist_id),
            CONSTRAINT FK_track__track_original_artists FOREIGN KEY (track_id) REFERENCES track (track_id),
            CONSTRAINT FK_artist__track_original_artists FOREIGN KEY (artist_id) REFERENCES artist (artist_id)
);

CREATE TABLE track_recorded_artists (
   track_id INTEGER,
  artist_id INTEGER,
            PRIMARY KEY(track_id, artist_id),
            CONSTRAINT FK_track__track_recorded_artists FOREIGN KEY (track_id) REFERENCES track (track_id),
            CONSTRAINT FK_artist__track_recorded_artists FOREIGN KEY (artist_id) REFERENCES artist (artist_id)
);

--============================================================================
-- DATA INITIALISATION
--============================================================================
INSERT INTO country (country_name, alpha_2_code, country_continent) VALUES
  ('United States', 'US', 'North America'),
  ('United Kingdom', 'GB', 'Europe'),
  ('Australia', 'AU', 'Oceania'),
  ('New Zealand', 'NZ', 'Oceania'),
  ('Canada', 'CA', 'North America'),
  ('Germany', 'DE', 'Europe'),
  ('Japan', 'JP', 'Asia');

INSERT INTO region (name, region_abbr, country_id) VALUES
  ('New York', 'NY', 1),
  (NULL, NULL, 2),
  ('Victoria', 'VIC', 3),
  ('Auckland', 'AUK', 4),
  ('Ontario', 'ON', 5),
  ('Berlin', 'BE', 6),
  ('Kantō', NULL, 7),
  ('Illinois', 'IL', 1),
  ('California', 'CA', 1);

INSERT INTO location (city, region_id) VALUES
  ('New York City', 1),
  ('London', 2),
  ('Melbourne', 3),
  ('Auckland', 4),
  ('Toronto', 5),
  ('Berlin', 6),
  ('Tokyo', 7),
  ('Chicago', 8),
  ('Belleville', 8),
  ('Pasadena', 9),
  ('Stockton', 9),
  ('Santa Monica', 9);

INSERT INTO artist (name, formation_date, formation_location_id, disband_date, favourite, artist_type, isni) VALUES
  ('Wilco', '1994-00-00', 8, NULL, TRUE, 'Band', '0000 0001 1523 0122'),
  ('Pavement', '1989-00-00', 11, NULL, TRUE, 'Band', '0000 0001 0657 3203');

INSERT INTO genre (name, origin_year, favourite) VALUES
  ('Rock', 1948, TRUE),
  ('Alternative Rock', 1978, TRUE),
  ('Indie Rock', 1978, TRUE),
  ('Pop', 1898, FALSE),
  ('Country', 1903, FALSE),
  ('Folk', 1889, FALSE),
  ('Synthpop', 1972, FALSE),
  ('Americana', 1970, TRUE),
  ('Slacker Rock', 1978, TRUE),
  ('Noise Rock', 1965, TRUE),
  ('Noise Pop', 1983, TRUE),
  ('Indie Pop', 1978, TRUE);

INSERT INTO composer (name, birth_date, birth_location_id, death_date) VALUES
  ('Jeff Tweedy', '1967-08-25', 9, NULL),
  ('Stephen Malkmus', '1966-05-30', 12, NULL),
  ('Scott Kannberg', '1966-08-30', 11, NULL);

INSERT INTO label (name, formation_date, formation_location_id, closing_date, favourite, label_code) VALUES
  ('Matador Records', '1989-00-00', 1, NULL, TRUE, 'LC 11552');

INSERT INTO media (name, media_abbr, classification, origin_year) VALUES
  ('Compact Disc', 'CD', 'Optical Disc', 1982),
  ('7'' Vinyl', '7''', 'Phonograph Record (PVC)', 1948),
  ('12'' Vinyl', '12''', 'Phonographic Record (PVC)', 1948),
  ('Digital Video Disc', 'DVD', 'Optical Disc', 1995),
  ('Cassette', NULL, 'Magnetic Tape', 1963);

INSERT INTO producer (name, birth_date, birth_location_id, death_date) VALUES
  ('Steve Albini', '1962-07-22', 10, NULL),
  ('<Self Produced>', NULL, NULL, NULL);

INSERT INTO release (title, release_date, favourite, rym_rating, aoty_rank, bea_rank, christgau_rating, scaruffi_rating, pitchfork_rating, metacritic, is_official) VALUES
  ('Watery, Domestic', '1992-11-25', TRUE, 3.86, 106, NULL, 'A-', NULL, NULL, NULL, TRUE);

INSERT INTO issue (label_id, release_id, release_date, catalogue_id, edition, is_rerelease, is_official, barcode, media_id, matrix_runout, description) VALUES
  (1, 1, '2010-03-09', 'OLE 044-1', 'Standard', TRUE, TRUE, '744861004400', 3, 'OLE-044-1A RJ / OLE-044-1B RJ', 'Promotional sticker attached to plastic seal');

INSERT INTO track (title, first_release_id, favourite, track_type) VALUES
  ('Texas Never Whispers', 1, TRUE, 'Original'),
  ('Frontwards', 1, TRUE, 'Original'),
  ('Feed Em To The (Linden) Lions', 1, TRUE, 'Original'),
  ('Shoot The Singer (1 Sick Verse)', 1, TRUE, 'Original');

INSERT INTO artist_genres (artist_id, genre_id) VALUES
  (2, 3),
  (2, 9),
  (2, 10),
  (2, 11),
  (2, 12);

INSERT INTO release_artists (release_id, artist_id) VALUES
  (1, 2);

INSERT INTO release_genres (release_id, genre_id) VALUES
  (1, 9),
  (1, 3);

INSERT INTO release_languages (release_id, language) VALUES
  (1, 'English');

INSERT INTO release_producers (release_id, producer_id) VALUES
  (1, 2);

INSERT INTO release_types (release_id, release_type) VALUES
  (1, 'EP');

INSERT INTO issue_countries (issue_id, country_id) VALUES
  (1, 1);

INSERT INTO track_composers (track_id, composer_id) VALUES
  (1, 2),
  (1, 3),
  (2, 2),
  (2, 3),
  (3, 2),
  (3, 3),
  (4, 2),
  (4, 3);

INSERT INTO track_isrc (track_id, isrc) VALUES
  (1, 'USMTD9204401');

INSERT INTO track_iswc (track_id, iswc) VALUES
  (1, 'T-700.085.847-1');

INSERT INTO track_recorded_artists (track_id, artist_id) VALUES
  (1, 2);