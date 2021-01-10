from datetime import datetime, timedelta
from sqlalchemy import Column
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.types import DateTime, Numeric
from utils.database import Base


class Symbol(AbstractConcreteBase):
    ts = Column(DateTime, primary_key=True, unique=True)
    open = Column(Numeric)
    high = Column(Numeric)
    low = Column(Numeric)
    close = Column(Numeric)
    volume = Column(Numeric)


class SymbolMixin(Base):
    __abstract__ = True

    @classmethod
    def get_from_last_year(cls):
        filter_after = datetime.today() - timedelta(weeks=52)
        return cls.query.filter(cls.ts >= filter_after).all()


class Etheur(Symbol, SymbolMixin):
    __tablename__ = 'etheur'
