from PySumpMon import config
from PySumpMon.domain import Base
from sqlalchemy import create_engine


def db_init():
    engine = create_engine(config.DB_CONNECTION_STRING)
    Base.metadata.create_all(engine)
