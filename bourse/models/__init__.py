# -*- coding: utf-8 -*-
#

import meta

import ConfigParser
import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from basic import Currency, Date
from ucits import Ucits, UcitsDailyValue
from ucits import UcitsPerformanceUcits, UcitsPerformanceMorningstar

def init():
    parser = ConfigParser.ConfigParser
    home = os.path.expanduser("~")
    parser.read(os.path.join(home, ".franckdbrc"))
    db_url = parser.get("bourse", "db_url")

    engine = create_engine(db_url, echo=False, convert_unicode=True)
    Session = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=engine))

    meta.session = Session()
