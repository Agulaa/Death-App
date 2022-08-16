from numpy import nan, select
import pandas as pd


class DataPreprocessingPipeline:
    """
    Preprocessing data set
    - annual-number-of-deaths-by-cause.csv
    - human-development-index.csv
    - population_since_1990.csv if download from google drive
    """

    def __init__(
        self,
        path_death: str,
        path_save_death: str,
        path_population: str,
        path_save_population: str,
        population_from_api: bool,
        path_index: str,
        path_save_index: str,
        path_to_save_input: str,
    ) -> None:
        self.population_from_api = population_from_api
        self.df_death = self.read_dataset(path_to_file=path_death, chunk_size=1000)
        if not self.population_from_api:
            self.df_population = self.read_dataset(
                path_to_file=path_population, chunk_size=100
            )
        else:
            self.df_population = self.read_dataset(
                path_to_file=path_save_population, chunk_size=1000
            )
        self.df_index = self.read_dataset(path_to_file=path_index, chunk_size=100)

        self.path_save_death = path_save_death
        self.path_save_population = path_save_population
        self.path_save_index = path_save_index
        self.path_save_input = path_to_save_input

    @staticmethod
    def read_dataset(path_to_file: str, chunk_size: int) -> pd.DataFrame:
        chunk = pd.read_csv(path_to_file, chunksize=chunk_size)
        return pd.concat(chunk)

    @staticmethod
    def rename_columns_name_death(name_columns: list[str]) -> list[str]:
        name_columns = [
            name.split(" - ")[1] if "Deaths" in name else name for name in name_columns
        ]
        name_columns = [
            "d: " + name if name not in ["country", "year", "code"] else name
            for name in name_columns
        ]
        return name_columns

    def preprocess_data_death(self) -> None:
        """
        Make preprocessing for death data set.
        """
        # Drop unnecessary columns
        drop_columns = ["Number of executions (Amnesty International)"]
        self.df_death = self.df_death.drop(drop_columns, axis=1)

        # Rename columns name
        name_columns = {"Entity": "country", "Year": "year", "Code": "code"}
        self.df_death = self.df_death.rename(columns=name_columns)
        self.df_death.columns = self.rename_columns_name_death(
            list(self.df_death.columns)
        )

        # Drop rows without code and fill NaN 0
        self.df_death = self.df_death[self.df_death["code"].notna()]
        self.df_death = self.df_death.fillna(0)

        # Drop duplicates
        self.df_death = self.df_death.drop_duplicates()

    def preprocess_data_population(self) -> None:
        """
        Make preprocessing for population data set.
        """
        # Drop unnecessary columns
        drop_columns = ["Series Name", "Series Code"]
        self.df_population = self.df_population.drop(drop_columns, axis=1)

        # Rename columns
        name_columns = {"Country Name": "country", "Country Code": "code"}
        self.df_population = self.df_population.rename(columns=name_columns)
        self.df_population.columns = [
            name_column.split(" ")[0] for name_column in self.df_population.columns
        ]

        # Reshaped by index country and rename columns
        self.df_population = (
            self.df_population.set_index(["country", "code"])
            .stack()
            .reset_index()
            .rename(columns={0: "population", "level_2": "year"})
        )

        # Change type and fill NaN
        self.df_population["year"] = self.df_population["year"].astype(int)
        self.df_population = self.df_population.replace("..", nan).fillna(
            method="ffill"
        )
        self.df_population["population"] = self.df_population["population"].astype(
            float
        )

        # Drop duplicates
        self.df_population = self.df_population.drop_duplicates()

    def preprocess_data_index(self) -> None:
        """
        Make preprocessing for index data set.
        HDI > 0.8 - highly level of development,
        0.8 >= HDI > 0.6 - medium level of development,
        0.6 >= HDI - low level of development.
        """
        # Rename columns
        name_columns = {
            "Entity": "country",
            "Code": "code",
            "Year": "year",
            "Human Development Index (UNDP)": "hdi",
        }
        self.df_index = self.df_index.rename(columns=name_columns)

        # drop Nan
        self.df_index = self.df_index[self.df_index["code"].notna()]

        # Calculate mean for hdi
        self.df_index = (
            self.df_index.groupby(["country", "code"]).mean()["hdi"].reset_index()
        )

        # level of development
        conditions = [
            self.df_index["hdi"] > 0.8,
            (self.df_index["hdi"] <= 0.8) & (self.df_index["hdi"] > 0.6),
            self.df_index["hdi"] <= 0.6,
        ]
        values = ["highly", "medium", "low"]
        self.df_index["development"] = select(conditions, values)

        # Drop duplicates
        self.df_index = self.df_index.drop_duplicates()

    def prepare_app_input_data(self) -> None:
        """
        Merge Death dataset with population dataset and save to csv
        This dataset will be use as input data set to app
        Columns:
        ‘country’, string,
        'code', string
        ‘year’, integer,
        ‘population’, float, 0 - 3e6 , population size in thousands;
        ‘d: cause of death1’, float, 0 >=, in thousands;
        """
        # merge to dataframe
        input_data = pd.merge(
            self.df_death, self.df_population, on=["code", "year"], how="inner"
        )
        # Change position column 'population'
        last_column = input_data.pop("population")
        input_data.insert(3, "population", last_column)
        if not self.population_from_api:
            input_data = input_data.drop(columns=["country_y"])
            input_data = input_data.rename(columns={"country_x": "country"})

        #  Change population size and number of death to in thousands
        input_data.iloc[:, 3:] = input_data.iloc[:, 3:] / 1000

        # Drop duplicates
        input_data = input_data.drop_duplicates()

        # Save to csv
        input_data.to_csv(self.path_save_input, index=False)

    def preprocess_data(self) -> None:
        """
        Make preprocessing for all dataset
        """
        self.preprocess_data_death()
        if not self.population_from_api:
            self.preprocess_data_population()
        self.preprocess_data_index()
        self.prepare_app_input_data()

    def save_preprocessed_dataset(self) -> None:
        """
        Save preprocessed data
        """
        self.df_index.to_csv(self.path_save_index, index=False)
        self.df_population.to_csv(self.path_save_population, index=False)
        self.df_death.to_csv(self.path_save_death, index=False)
