# -*- coding: utf-8 -*-
#

import datetime

import requests
from bs4 import BeautifulSoup, SoupStrainer

class UcitsBoursorama():
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

        r_ucits = requests.get(self.url)
        soup_ucits = BeautifulSoup(r_ucits.text, "lxml")
        r_perf = requests.get(self.url_perf)
        soup_perf = BeautifulSoup(r_perf.text, "lxml")

        # Datas for Table Ucits"
        # name, code, owner, resume
        ucits_name = soup_ucits.find("a", {"itemprop": "name"}
                                ).contents[0].string.strip()
        ucits_code = soup_ucits.find("h2").string.split()[0]
        ucits_owner = " ".join(soup_ucits.find("h2").string.split()[3:]
                                    ).lstrip("(").rstrip(")")
        ucits_resume = soup_ucits.find("p", {"class": "taj"}
                                    ).find("b").string
        # Datas for Table UcitsDailyValue :
        # date, value, currency, variation
        price_list = soup_ucits.find("div", {"id": "fiche_cours_details"}
                                                            ).find_all("td")
        for elem in price_list:
            if elem.string:
                try:
                    date = datetime.date(int(elem.string.split("/")[2]),
                                        int(elem.string.split("/")[1]),
                                        int(elem.string.split("/")[0]))
                    break
                except IndexError:
                    pass

        (value, currency) = soup_ucits.find("big", {"class": "fv-last"}
                                ).contents[1].string.split(" ")
        
        value = float(value)
        variation = soup_ucits.find("big", {"class": "fv-var"}
                                                ).contents[1].string.strip("%")
        variation = float(variation)
        
        # Data for Table UcitsPerformanceDate
        table_performance_date = soup_perf.table.contents[1].find(
                                                    id="perfDate").string
        perf_date = datetime.date(
                                int(table_performance_date.split("/")[2]),
                                int(table_performance_date.split("/")[1]),
                                int(table_performance_date.split("/")[0]))

        # Data for ucits performance
        table_performance = soup_perf.table.contents[1].find(
                                                id="perfChart").find_all("td")
        if not len(table_performance) == 30:
            raise ValueError("table of performance is not 30 elements")
        
        # Data for Table UcitsPerformanceUcits
        ucits_perf = _get_performance(table_performance[11:20])

        # Data for Table UcitsPerformanceMorningstar
        ucits_morningstar_perf = _get_performance(table_performance[21:])


        return {"name": ucits_name, "code": ucits_code, "owner": ucits_owner,
                "resume": ucits_resume, "date": date,
                "value": value, "currency": currency, "variation": variation, 
                "ucits_perf": ucits_perf, 
                "ucits_morningstar_perf": ucits_morningstar_perf
                }


