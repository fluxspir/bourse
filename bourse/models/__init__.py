# -*- coding: utf-8 -*-
#

import meta
import sqlalchemy
import ConfigParser
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from zope.sqlalchemy import ZopeTransactionExtension

from basic import Currency, Date
from ucits import (Ucits, UcitsDailyValue,
                    UcitsPerformanceUcits, UcitsPerformanceMorningstar)

def init():
    parser = ConfigParser.ConfigParser()
    home = os.path.expanduser("~")
    parser.read(os.path.join(home, ".franckdbrc"))
    db_url = parser.get("bourse", "db_url")

    engine = create_engine(db_url, echo=False, convert_unicode=True)
    Session = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=engine))

    meta.session = Session()
