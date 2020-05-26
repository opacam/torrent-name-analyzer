from pathlib import Path

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from torrent_name_analyzer.config import config_by_name

Base = declarative_base()


class Torrent(Base):
    __tablename__ = "torrents"
    torrent_id = Column(Integer, primary_key=True)
    torrent_name = Column(String(150), unique=True)
    title = Column(String(150))
    year = Column(Integer())
    month = Column(Integer())
    day = Column(Integer())
    season = Column(String(150))
    episode = Column(String(150))
    episodeName = Column(String(150))
    resolution = Column(String(30))
    audio = Column(String(30))
    bitDepth = Column(String(30))
    codec = Column(String(30))
    quality = Column(String(30))
    encoder = Column(String(30))
    group = Column(String(30))
    website = Column(String(30))
    language = Column(String(30))
    region = Column(String(30))
    subtitles = Column(String(30))
    container = Column(String(30))
    size = Column(String(30))

    rip_properties = Column(String(150))

    excess = Column(String(30))

    timestamp = Column(DateTime())

    def update(self, **kwargs):
        for key, old_value in vars(self).items():
            if not key.startswith("_") and key in kwargs:
                setattr(self, key, kwargs[key])

    def dump(self):
        data = {}
        for k, v in vars(self).items():
            if k.startswith("_"):
                continue
            if v is None:
                continue
            data[k] = v
        return data


def init_db(config_name):
    uri = config_by_name[config_name].SQLALCHEMY_DATABASE_URI

    # make sure that we start our test with a clean database
    if config_name == "test":
        db_file = Path(uri.split("///")[1])
        if db_file.is_file():
            db_file.unlink()

    engine = create_engine(uri)
    db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
    return db_session
