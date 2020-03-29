from utils.logger import logger as log
import pandas as pd
import numpy as np


class Database():
    def __init__(self, db_type):

        filename_map = {
            "confirmed": "time_series_covid19_confirmed_global.csv",
            "deaths": "time_series_covid19_deaths_global.csv",
            "recovered": "time_series_covid19_recovered_global.csv"
        }
        self.dataframe = self.load_file(filename_map[db_type.lower()])

    def get_patients_by_country(self, country=None):
        if country is None:
            return self.dataframe
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


def to_numpy(dataframe, start=4, filter=lambda x: x > 100):
    cols = dataframe.keys()
    # Remove the initial columns, sum over all the provinces
    df = dataframe.loc[:, cols[start]:cols[-1]].sum(axis=0)
    # Convert to numpy
    arr = np.array(df)
    dates = np.array(pd.to_datetime(df.keys()))
    # Get the first index that satisfy the filter
    index = min(np.argwhere(filter(arr))).item()
    return dates[index:], arr[index:]
