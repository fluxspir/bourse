# -*- coding: utf-8 -*-
#


from meta import Base

import basic

from sqlalchemy import Table, Column, Integer, Float, String, Date, DateTime
from sqlalchemy import ForeignKey, MetaData
from sqlalchemy.orm import relationship

class Tracker(Base):
    __tablename__ = "tracker"
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    name = Column(String)
    resume = Column(String)

class TrackerDailyValue(Base):
    __tablename__ = "tracker_daily_value"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, unique=True)
    tracker_id = Column(Integer, ForeignKey(Tracker.id), nullable=False)
    tracker= relationship("Tracker")
    date_id = Column(Integer, ForeignKey(basic.Date.id), nullable=False)
    date = relationship("Date")
    currency_id = Column(Integer, ForeignKey(basic.Currency.id), 
                                                    nullable=False)
    currency = relationship("Currency")
    value = Column(Float, nullable=False)
    variation = Column(Float, nullable=False)

class TrackerPerformance(Base):
    __tablename__ = "tracker_performance"
    id = Column(Integer, primary_key=True)
    tracker_id = Column(Integer, ForeignKey(Tracker.id), nullable=False)
    tracker = relationship("Tracker")
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

class TrackerPerformanceMorningstar(Base):
    __tablename__ = "tracker_performance_morningstar"
    id = Column(Integer, primary_key=True)
    tracker_id = Column(Integer, ForeignKey(Tracker.id), nullable=False)
    tracker = relationship("Tracker")
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


