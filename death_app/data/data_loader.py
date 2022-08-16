import pandas as pd
from functools import lru_cache


class DataLoader:
    """
    Reads specific information from dataset (available countries and min/max years)
    Reads dataset and finds rows with specific countries between specific years
    Reads dataset and finds rows between specific years with level of development
    """

    def __init__(self, path_to_dataset: str, path_to_index: str) -> None:
        self.data = self.read_dataframe(path_to_dataset, 1000)
        self.index = self.read_dataframe(path_to_index, 1000)

    @staticmethod
    def read_dataframe(path_to_file: str, chunk_size: int) -> pd.DataFrame:
        """
        Read from csv file
        :param path_to_file:
        :param chunk_size:
        :return: dataframe
        """
        chunk = pd.read_csv(path_to_file, chunksize=chunk_size)
        return pd.concat(chunk)

    @lru_cache(maxsize=None)
    def get_list_of_countries(self) -> list[str]:
        """
        Return list of available countries in application
        :return: list with countries name
        """
        return list(self.data["country"].unique())

    @lru_cache(maxsize=None)
    def get_number_of_death_causes(self) -> int:
        """
        Return number of available causes of death
        first 4th columns = 'country', 'code', 'year', 'population'
        next => causes_of_death
        :return: number
        """
        return len(self.data.columns[4:])

    @lru_cache(maxsize=None)
    def get_death_causes(self) -> list[str]:
        """
        Return  available causes of death
        first 4th columns = 'country', 'code', 'year', 'population'
        next => causes_of_death "d: causes..."
        :return: list with death causes without "d: "
        """
        return sorted([name[3:] for name in self.data.columns[4:]])

    @lru_cache(maxsize=None)
    def get_types_of_development(self) -> list[str]:
        """
        Return list with types of development
        :return list of strings
        """

        return list(
            pd.merge(self.data, self.index, on=["code"], how="inner")[
                "development"
            ].unique()
        )

    def get_range_years_for_country(self, countries: list[str]) -> tuple:
        """
        Return tuple with minimal and maximal available year for specific country
        :param countries: list of countries name
        :return: tuple (min_year, max_year)
        """
        all_set_with_years = []
        for country in countries:
            all_set_with_years.append(
                set(self.data[self.data["country"] == country].year)
            )
        set_with_common_year = set.intersection(*tuple(all_set_with_years))
        return min(set_with_common_year), max(set_with_common_year)

    def get_data_from_specific_countries_and_year(
        self, countries: list[str], year_start: int, year_end: int
    ) -> pd.DataFrame:
        """
        Get specific data from dataset
        :param countries: list of countries name
        :param year_start: minimal year
        :param year_end: maximal year
        :return: filtered dataset
        """
        return self.data[
            (self.data["country"].isin(countries))
            & (self.data["year"].between(year_start, year_end))
        ]

    def get_range_of_years_for_development(self) -> tuple:
        """
        Return tuple with minimal and maximal available year for country which have index of development
        :return: minimal year, maximal year
        """
        develop = (
            pd.merge(self.data, self.index, on=["code"], how="inner")
            .drop(columns=["country_y", "hdi"])
            .rename(columns={"country_x": "country"})
        )
        return min(develop["year"]), max(develop["year"])

    def get_data_by_level_of_development(
        self, development: list[str], year_start: int, year_end: int
    ) -> pd.DataFrame:
        """
        Get specific data from dataset and merge with index of development
        :param development: levels of development
        :param year_start: minimal year
        :param year_end: maximal year
        :return: filtered dataset with last column 'development' (low, medium, highly)
        """
        result = self.data[self.data["year"].between(year_start, year_end)]
        develop = (
            pd.merge(result, self.index, on=["code"], how="inner")
            .drop(columns=["country_y", "hdi"])
            .rename(columns={"country_x": "country"})
        )
        return develop[develop["development"].isin(development)]
