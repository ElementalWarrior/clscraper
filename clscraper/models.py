from contextlib import contextmanager
from sqlalchemy import *
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

from .settings import Config

engine = create_engine(URL(**Config.DATABASE))
Session = sessionmaker(bind=engine)


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