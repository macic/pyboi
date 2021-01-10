from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.schema import MetaData
from contextlib import contextmanager

from config.base import db_url

# resources
engine = create_engine(db_url)

# create a configured "Session" class
maker = sessionmaker(bind=engine)
Session = scoped_session(maker)
metadata = MetaData()


@as_declarative()
class Base:
    """
    Add some default properties and methods to the SQLAlchemy declarative base.
    """
    query = Session.query_property()


@contextmanager
def session_scope() -> Session:
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
