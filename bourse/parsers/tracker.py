# -*- coding: utf-8 -*-
#

import pdb

import datetime

import requests
from bs4 import BeautifulSoup, SoupStrainer

import os
home = os.path.expanduser("~")

class TrackerBoursorama():
    def __init__(self, url, url_perf):
        self.url = url
        self.url_perf = url_perf

    def get_datas(self):

        def _get_performance(perf_list):
            """
            return(last_week, january_first, last_month, three_months, 
                    six_months, one_year, three_years, five_years, ten_years)
            """
            performance = []
            for elem in perf_list:
                variation = elem.string.strip("%")
                performance.append(float(variation))
            return tuple(performance)

        r_tracker = requests.get(self.url)
        soup_tracker = BeautifulSoup(r_tracker.text, "lxml")
        r_perf = requests.get(self.url_perf)
        soup_perf = BeautifulSoup(r_perf.text, "lxml")
        
        # Datas for Table Tracker"
        # name, code, owner, resume
        tracker_name = soup_tracker.find("a", {"itemprop": "name"}
                                ).contents[0].string.strip()
        tracker_code = soup_tracker.find("h2").string.split()[0]
        tracker_resume = soup_tracker.find("div", {"class": "taj"}
                                    ).find("strong").string
        # Datas for Table UcitsDailyValue :
        # date, value, currency, variation
        price_list = soup_tracker.find("div", {"id": "fiche_cours_details"}
                                                            ).find_all("td")
        for elem in price_list:
            try:
                if len(elem.contents[0].split("/")) == 3:
                    shortyear = elem.contents[0].split("/")[2].replace(
                                                                u'\xa0', u'')
                    date = datetime.date(int(u'20' + shortyear),
                                        int(elem.contents[0].split("/")[1]),
                                        int(elem.contents[0].split("/")[0]))
                    break
            except TypeError:
                pass

        (value, ignore, currency) = soup_tracker.find("span", {"class": 
                                                "cotation"}).string.split(" ")
        
        value = float(value)
        variation = soup_tracker.find("big", {"class": "fv-var"}
                                                ).contents[1].string.strip("%")
        variation = float(variation)
        
        # Data for Table UcitsPerformanceDate
#        table_performance_date = soup_perf.table.contents[1].find(
#                                                    id="perfDate").string
#        perf_date = datetime.date(
#                                int(table_performance_date.split("/")[2]),
#                                int(table_performance_date.split("/")[1]),
#                                int(table_performance_date.split("/")[0]))
#        perf_date = date

        # Data for ucits performance
        # soup_perf.find(id="perfChart")
        table_performance = soup_perf.find(id="perfChart").find_all("td")
        if not len(table_performance) == 40:
            raise ValueError("table of performance is not 30 elements")
        
        # Data for Table UcitsPerformanceUcits
        tracker_perf = _get_performance(table_performance[11:20])

        # Data for Table UcitsPerformanceMorningstar
        tracker_morningstar_perf = _get_performance(table_performance[21:30])


        return {"name": tracker_name, "code": tracker_code,
                "resume": tracker_resume, "date": date,
                "value": value, "currency": currency, "variation": variation, 
                "tracker_perf": tracker_perf, 
                "tracker_morningstar_perf": tracker_morningstar_perf
                }


