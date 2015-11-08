# -*- coding: utf-8 -*-
#

import models
import sqlalchemy
from sqlalchemy import and_

class UcitsAdd():
    def __init__(self, session):
        self.session = session

    def _test_currency(self, cur):
        query = self.session.query(models.Currency)
        query = query.filter(models.Currency.symbol == cur).one_or_none()
        return query

    def _test_ucits(self, code):
        query = self.session.query(models.Ucits)
        query = query.filter(models.Ucits.code == code).one_or_none()
        return query

    def _test_ucits_datas(self, datas):
        query = self.session.query(models.Ucits)
        for elem in "name", "owner", "resume":
            result = query.filter(models.Ucits.code == datas["code"]).one()
            if not getattr(result, elem) == datas[elem]:
                old_value = getattr(result, elem)
                if not getattr(result, elem):
                    old_value = ""
                setattr(result, elem, datas[elem])
                msg = "Updating {} - {} \n from old value {} \n\
                                with new value {}".format("Ucits", 
                                        elem,
                                        old_value.encode("utf_8"),
                                        datas[elem].encode("utf_8"))
                print(msg)
                self.session.commit()

    def _test_date(self, date):
        query = self.session.query(models.Date)
        query = query.filter(models.Date.date == date).one_or_none()
        return query

    def _test_ucits_daily_value(self, code, date):
        code_id = self.session.query(models.Ucits).filter(
                                            models.Ucits.code == code).one().id
        date_id = self.session.query(models.Date).filter(
                                            models.Date.date == date).one().id
        query = self.session.query(models.UcitsDailyValue)
        query = query.filter(and_(models.UcitsDailyValue.ucits_id == code_id,
                                models.UcitsDailyValue.date_id == date_id)
                                ).one_or_none()
        return query

    def _test_ucits_perf(self, code, date):
        code_id = self.session.query(models.Ucits).filter(
                                            models.Ucits.code == code).one().id
        date_id = self.session.query(models.Date).filter(
                                            models.Date.date == date).one().id
        query = self.session.query(models.UcitsPerformance)
        query = query.filter(and_(
                            models.UcitsPerformance.ucits_id == code_id,
                            models.UcitsPerformance.date_id == date_id)
                            ).one_or_none()
        return query

    def _test_ucits_perf_morningstar(self, code, date):
        code_id = self.session.query(models.Ucits).filter(
                                            models.Ucits.code == code).one().id
        date_id = self.session.query(models.Date).filter(
                                            models.Date.date == date).one().id
        query = self.session.query(models.UcitsPerformanceMorningstar)
        query = query.filter(and_(
                        models.UcitsPerformanceMorningstar.ucits_id == code_id,
                        models.UcitsPerformanceMorningstar.date_id == date_id,)
                        ).one_or_none()
        return query

    def add(self, datas):

        # adding the currency
        if not self._test_currency(datas["currency"]):
            values = { "symbol": datas["currency"] }
            try:
                new_entry = models.Currency(**values)
                self.session.add(new_entry)
                self.session.commit()
            except sqlalchemy.exc.IntegrityError:
                print("error while adding currency {}".format(
                                                        datas["currency"]))
                raise

        # adding the ucits
        if not self._test_ucits(datas["code"]):
            values = { "code": datas["code"],
                        "name": datas["name"],
                        "owner": datas["owner"],
                        "resume": datas["resume"]
                    }
            try:
                new_entry = models.Ucits(**values)
                self.session.add(new_entry)
                self.session.commit()
            except sqlalchemy.exc.IntegrityError:
                print("error while adding ucits {}, {}, {}, {}".format(
                                        datas["name"].encode("utf_8"),
                                        datas["code"].encode("utf_8"),
                                        datas["owner"].encode("utf_8"),
                                        datas["resume"].encode("utf_8")))
                raise
        else:
            self._test_ucits_datas(datas)

        # adding the date
        if not self._test_date(datas["date"]):
            values = { "date": datas["date"] }
            try:
                new_entry = models.Date(**values)
                self.session.add(new_entry)
                self.session.commit()
            except sqlalchemy.exc.IntegrityError:
                print("error while adding date {}".format(datas["date"]))
                raise

        # adding the daily values of the ucits
        if not self._test_ucits_daily_value(datas["code"], datas["date"]):
            code = self.session.query(models.Ucits).filter(
                                models.Ucits.code == datas["code"]).one().id
            date = self.session.query(models.Date).filter(
                                models.Date.date == datas["date"]).one().id
            currency = self.session.query(models.Currency).filter(
                                models.Currency.symbol ==datas["currency"]
                                ).one().id
            values = { "ucits_id": code,
                        "date_id": date,
                        "timestamp": datetime.datetime.now(),
                        "currency_id": currency,
                        "value": datas["value"],
                        "variation": datas["variation"]
                    }
            try:
                new_entry = models.UcitsDailyValue(**values)
                self.session.add(new_entry)
                self.session.commit()
            except sqlalchemy.exc.IntegrityError:
                print("error while adding daily value of {} code {}".format(
                                        datas["code"].encode("utf_8"),
                                        datas["name"].encode("utf_8")))
                raise

        # adding performances
        if not self._test_ucits_perf(datas["code"], datas["date"]):
            code = self.session.query(models.Ucits).filter(
                                models.Ucits.code == datas["code"]).one().id
            date = self.session.query(models.Date).filter(
                                models.Date.date == datas["date"]).one().id
            perf = datas["ucits_perf"]
            values = { "ucits_id": code,
                        "date_id": date,
                        "last_week": perf[0],
                        "january_first": perf[1],
                        "last_month": perf[2],
                        "three_months": perf[3],
                        "six_months": perf[4],
                        "one_year": perf[5],
                        "three_years": perf[6],
                        "five_years": perf[7],
                        "ten_years": perf[8]
                    }
            try:
                new_entry = models.UcitsPerformance(**values)
                self.session.add(new_entry)
                self.session.commit()
            except sqlalchemy.exc.IntegrityError:
                print("error while adding performances of ucits {} code {} :\n\
                    values : {}".format( datas["name"], datas["code"], perf))
                raise

        if not self._test_ucits_perf_morningstar(datas["code"], datas["date"]):
            code = self.session.query(models.Ucits).filter(
                                models.Ucits.code == datas["code"]).one().id
            date = self.session.query(models.Date).filter(
                                models.Date.date == datas["date"]).one().id
            perf = datas["ucits_morningstar_perf"]
            values = { "ucits_id": code,
                        "date_id": date,
                        "last_week": perf[0],
                        "january_first": perf[1],
                        "last_month": perf[2],
                        "three_months": perf[3],
                        "six_months": perf[4],
                        "one_year": perf[5],
                        "three_years": perf[6],
                        "five_years": perf[7],
                        "ten_years": perf[8]
                    }
            try:
                new_entry = models.UcitsPerformanceMorningstar(**values)
                self.session.add(new_entry)
                self.session.commit()
            except sqlalchemy.exc.IntegrityError:
                print("error while adding morningstar performances of ucits {}\
                    code {} : \n\
                    values : {}".format( datas["name"], datas["code"], perf))
                raise


