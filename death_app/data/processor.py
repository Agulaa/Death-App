import pandas as pd


class DataProcessor:
    """
    A set of functions which help to process data to a form requested by particular plots.
    """

    def __init__(self):
        pass

    @staticmethod
    def get_top_causes_summed_by_range_of_year(
        df: pd.DataFrame, top: int
    ) -> pd.DataFrame:
        """
        Shows top N causes of death in a set of countries, summed across specified date range
        :param df: dataframe with specific countries and data range
        :param top: number of causes
        :return: dataframe summed by range of year with top N causes of death in specified countries
        """
        # set index and summed for country and year
        sum_by_year = df.set_index(["country", "year"]).groupby("country").sum()
        # Calculate death per X inhabitants
        inhabitants = 10_000
        # first  column ['population'] next columns are death causes
        result = (
            sum_by_year.iloc[:, 1:].divide(sum_by_year["population"], axis=0)
            * inhabitants
        )
        # found top causes in each country
        top_result = []
        for index, row in result.iterrows():
            top_result.append(row.sort_values(ascending=False)[:top])
        # fill 0 NaN
        return pd.DataFrame(top_result).fillna(0)

    @staticmethod
    def get_top_causes_in_each_year(df: pd.DataFrame, top: int) -> pd.DataFrame:
        """
        Shows top N causes of death in a set of countries, in each year from a specified date range
        :param df: dataframe with specific countries and data range
        :param top: top number of causes
        :return: dataframe with top N causes of death in each year in specified countries
        """
        # Calculate death per X inhabitants
        inhabitants = 10_000
        # first 4 columns ['country', 'code', 'year', 'population'] next columns are death causes
        result = df.iloc[:, 4:].divide(df["population"], axis=0) * inhabitants
        # keep info about country and year
        result["country"] = df["country"]
        result["year"] = df["year"]
        # set index
        result = result.set_index(["year", "country"]).T
        each_year = []
        for column in list(result.columns):
            each_year.append(result[column].sort_values(ascending=False)[:top])

        df_result = pd.DataFrame(each_year)
        df_result = df_result.rename_axis(("year", "country"))
        df_result = (
            df_result.stack()
            .reset_index()
            .rename(columns={"level_2": "Causes of death", 0: "values"})
            .sort_values(by=["year", "country"])
        )

        return df_result

    @staticmethod
    def get_trend_cause_in_each_year_in_countries(
        df: pd.DataFrame, cause: str
    ) -> pd.DataFrame:
        """
        Shows trend in cause of death in set of countries, in each year, from a specified date range
        :param df: dataframe with specific level of development and data range
        :param cause:  one cause of death
        :return: dataframe in specific range of year, in each year, with one cause of death in specified countries
        """
        # Calculate death per X inhabitants
        inhabitants = 100_000
        # first 4 columns ['country', 'code', 'year', 'population']  next columns are death causes
        result = df.iloc[:, 4:].divide(df["population"], axis=0) * inhabitants
        result["country"] = df["country"]
        result["year"] = df["year"]
        # update causes name
        cause = f"d: {cause}"
        # return only with specific causes
        return result.loc[:, ["country", "year", cause]].sort_values(
            by=["country", "year"]
        )

    @staticmethod
    def get_top_causes_summed_by_level_of_develop(
        df: pd.DataFrame, top: int
    ) -> pd.DataFrame:
        """
        Shows top N causes of death by the level of development, summed across specified date range
        :param df: dataframe with specific level of development and data range
        :param top: top number of causes
        :return: dataframe summed by range of year with top N causes of death in specified level of development
        """
        # grouped by development and divide by group size
        sum_by_level = df.groupby("development").sum()
        # Calculate death per X inhabitants
        inhabitants = 100_000
        # first 2 columns are 'year' and 'population' next columns are death causes
        result = (
            sum_by_level.iloc[:, 2:].divide(sum_by_level["population"], axis=0)
            * inhabitants
        )
        # found top causes in each level of development
        top_result = []
        for index, row in result.iterrows():
            top_result.append(row.sort_values(ascending=False)[:top])
        return pd.DataFrame(top_result).fillna(0)

    @staticmethod
    def get_top_causes_in_each_year_by_level_of_develop(
        df: pd.DataFrame, top: int
    ) -> pd.DataFrame:
        """
        Shows top N causes of death by the level of development, summed across specified date range
        :param df: dataframe with specific level of development and data range
        :param top: top number of causes
        :return: dataframe summed by range of year with top N causes of death in specified level of development
        """
        # grouped by year and development
        sum_by_level = df.groupby(["year", "development"]).sum()
        # Calculate death per X inhabitants
        inhabitants = 100_000
        # first  column is 'population' next columns are death causes
        result = (
            sum_by_level.iloc[:, 1:].divide(sum_by_level["population"], axis=0)
            * inhabitants
        ).T
        each_year = []
        for column in list(result.columns):
            each_year.append(result[column].sort_values(ascending=False)[:top])

        df_result = pd.DataFrame(each_year)
        df_result = df_result.rename_axis(("year", "development"))
        df_result = (
            df_result.stack()
            .reset_index()
            .rename(columns={"level_2": "Causes of death", 0: "values"})
            .sort_values(by=["year", "development"])
        )
        # return only with specific causes
        return df_result

    @staticmethod
    def get_trend_cause_in_each_year_by_level_of_develop(
        df: pd.DataFrame, cause: str
    ) -> pd.DataFrame:
        """
        Show trend in cause of death by level of development from a specified date range
        :param df: dataframe with specific level of development and data range
        :param cause: one cause of death
        :return: dataframe in specific range of year, in each year, with one cause of death in specified level of
        development
        """
        # grouped by year and development
        sum_by_level = df.groupby(["year", "development"]).sum()
        # Calculate death per X inhabitants
        inhabitants = 100_000
        # first  column is 'population' next columns are death causes
        result = (
            (
                sum_by_level.iloc[:, 1:].divide(sum_by_level["population"], axis=0)
                * inhabitants
            )
            .reset_index()
            .sort_values("year")
        )
        # update causes name
        cause = f"d: {cause}"
        # return only with specific causes
        result = result.loc[:, ["year", "development", cause]]
        return result
