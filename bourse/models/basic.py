# -*- coding: utf-8 -*-
#

from meta import Base
from sqlalchemy import Table, Column, Integer, String, Date

class Currency(Base):
    __tablename__ = "currency"
    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True)

class Date(Base):
    __tablename__ = "date"
    id = Column(Integer, primary_key=True)
    date = Column(Date, unique=True)


