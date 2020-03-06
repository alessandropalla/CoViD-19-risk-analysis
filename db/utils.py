from utils.logger import logger as log
import pandas as pd
import numpy as np
import os
from enum import Enum


class Database():
    def __init__(self, db_type):

        filename_map = {
            "confirmed": "time_series_19-covid-Confirmed.csv",
            "deaths": "time_series_19-covid-Deaths.csv",
            "recovered": "time_series_19-covid-Recovered.csv"
        }
        self.dataframe = self.load_file(filename_map[db_type.lower()])

    def get_patients_by_country(self, country):
        if country not in self.get_countries():
            log.warning(f"Country {country} is not in the database")
        return self.dataframe[self.dataframe["Country/Region"] == country]

    def get_countries(self):
        return list(set(self.dataframe["Country/Region"].values.tolist()))

    def load_file(self, filename):
        # Database path
        repo = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19"
        db_path = "csse_covid_19_data/csse_covid_19_time_series"
        # File path
        file_path = f"{repo}/master/{db_path}/{filename}"
        # Read CSV
        return pd.read_csv(file_path)
