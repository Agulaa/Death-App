import pandas as pd
import wbgapi as wb
from numpy import nan
import os


class DataAPIDownloader:
    """
    Download data with countries population using WBGAPI
    """

    def __init__(
        self, year_start: int, year_end: int, path_to_save: str, path_to_folder: str
    ) -> None:
        self.year_start = year_start
        self.year_end = year_end
        self.path_to_save = path_to_save
        self.path_to_folder = path_to_folder
        self.get_population_dataset()

    def download_population(self) -> pd.DataFrame:
        """
        Download dataset from The World Bank Api
        Database - (40) - Population estimates and projections
        Measure - (SP.POP.TOTL) - Population, total
        :return: raw dataframe
        """

        wb.db = 40
        df = wb.data.DataFrame(
            ["SP.POP.TOTL"], time=range(self.year_start, self.year_end + 1)
        )
        return df

    @staticmethod
    def preprocess_population(df: pd.DataFrame) -> pd.DataFrame:
        """
        Make preprocessing for population data set
        :param df: downloaded dataset
        :return: preprocessed dataframe
        """
        df = df.reset_index().rename(columns={"index": "code"})
        df.columns = df.columns.str.replace("YR", "")
        df = (
            df.set_index("code")
            .stack()
            .reset_index()
            .rename(columns={0: "population", "level_1": "year"})
        )
        df["code"] = df["code"].astype(str)
        df["year"] = df["year"].astype(int)
        df = df.replace("..", nan).fillna(method="ffill")
        df["population"] = df["population"].astype(float)
        df = df.drop_duplicates()
        return df

    def get_population_dataset(self) -> None:
        """
        Download, preprocess and save dataset with population of countries
        """
        df = self.download_population()
        df = self.preprocess_population(df)
        if not os.path.exists(self.path_to_folder):
            os.makedirs(self.path_to_folder)
        df.to_csv(self.path_to_save, index=False)
