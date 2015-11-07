# -*- coding: utf-8 -*-
#


from meta import Base

import basic

from sqlalchemy import Table, Column, Integer, Float, String, Date, DateTime
from sqlalchemy import ForeignKey, MetaData
from sqlalchemy.orm import relationship

class Ucits(Base):
    __tablename__ = "ucits"
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    name = Column(String)
    owner = Column(String)
    resume = Column(String)

class UcitsDailyValue(Base):
    __tablename__ = "ucits_daily_value"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, unique=True)
    ucits_id = Column(Integer, ForeignKey(Ucits.id), nullable=False)
    ucits= relationship("Ucits")
    date_id = Column(Integer, ForeignKey(basic.Date.id), nullable=False)
    date = relationship("Date")
    currency_id = Column(Integer, ForeignKey(basic.Currency.id), 
                                                    nullable=False)
    currency = relationship("Currency")
    value = Column(Float, nullable=False)
    variation = Column(Float, nullable=False)

class UcitsPerformanceUcits(Base):
    __tablename__ = "ucits_performance_ucits"
    id = Column(Integer, primary_key=True)
    ucits_id = Column(Integer, ForeignKey(Ucits.id), nullable=False)
    ucits = relationship("Ucits")
    date_id = Column(Integer, ForeignKey(basic.Date.id), nullable=False)
    date = relationship("Date")
    last_week = Column(Float)
    january_first = Column(Float)
    last_month = Column(Float)
    three_months = Column(Float)
    six_months = Column(Float)
    one_year = Column(Float)
    three_years = Column(Float)
    five_years = Column(Float)
    ten_years = Column(Float)

class UcitsPerformanceMorningstar(Base):
    __tablename__ = "ucits_performance_morningstar"
    id = Column(Integer, primary_key=True)
    ucits_id = Column(Integer, ForeignKey(Ucits.id), nullable=False)
    ucits = relationship("Ucits")
    date_id = Column(Integer, ForeignKey(basic.Date.id), nullable=False)
    date = relationship("Date")
    last_week = Column(Float)
    january_first = Column(Float)
    last_month = Column(Float)
    three_months = Column(Float)
    six_months = Column(Float)
    one_year = Column(Float)
    three_years = Column(Float)
    five_years = Column(Float)
    ten_years = Column(Float)


