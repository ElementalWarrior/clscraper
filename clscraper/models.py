from contextlib import contextmanager
from sqlalchemy import event
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Text, Integer, DECIMAL, String, DateTime, Boolean, ForeignKey
from sqlalchemy import *
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func

from .settings import Config

url = URL(**Config.DATABASE)
engine = create_engine(url)
Session = sessionmaker(bind=engine)
DeclarativeBase = declarative_base()


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class Posting(DeclarativeBase):
    __tablename__ = "postings"

    id = Column(Integer, primary_key=True)
    url = Column(Text, nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text)
    images = Column(JSONB)
    price = Column(DECIMAL)
    price_currency = Column(String(10))
    floor_area = Column(Integer)
    floor_area_units = Column(String(10))
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    location = Column(JSONB)
    # attributes=Column(Text
    datetime_posted = Column(DateTime)
    partial_scrape = Column(Boolean, nullable=False)
    datetime_scraped = Column(DateTime, nullable=False)


class PostingRevision(DeclarativeBase):
    __tablename__ = "posting_revisions"
    __table_args__ = (
        PrimaryKeyConstraint('id', 'posting_id'),
        {},
    )

    # id serves as revision_id
    id = Column(Integer)
    posting_id = Column(Integer, ForeignKey("postings.id"))

    url = Column(Text, nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text)
    images = Column(JSONB)
    price = Column(DECIMAL)
    price_currency = Column(String(10))
    floor_area = Column(Integer)
    floor_area_units = Column(String(10))
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    location = Column(JSONB)
    # attributes=Column(Text
    datetime_posted = Column(DateTime)
    partial_scrape = Column(Boolean, nullable=False)
    datetime_scraped = Column(DateTime, nullable=False)
