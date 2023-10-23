import logging

from sqlalchemy import create_engine

DB_LOCATION = 'C:/sqlite/melophobia/melophobia.db'

logging.basicConfig(filename='melophobia.log', encoding='utf-8', format='%(asctime)s %(levelname)s:%(message)s',
                    level=logging.DEBUG)


def db_init():
    return create_engine(f"sqlite:///{DB_LOCATION}", echo=True)


DB_ENGINE = db_init()


def db_stop():
    DB_ENGINE.dispose()

    logging.info('[SQL] SQLite connection has been closed.')
