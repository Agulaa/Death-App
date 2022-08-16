import pandas as pd
import numpy as np


class DataValidator:
    """
    Checks if the new datasets follow the structure required by the app.
    """

    def __init__(self, path_to_death_dataset: str, path_to_index_dataset: str) -> None:
        self.path_to_death_dataset = path_to_death_dataset
        self.path_to_index_dataset = path_to_index_dataset

    # DEATH DATASET
    def check_minimal_size_in_death_dataset(self) -> bool:
        """
        Death dataset must contain columns ‘country’, ‘year’, ‘population’ and
        at least one column with cause of death and minimal one row with data
        """
        data = pd.read_csv(self.path_to_death_dataset, nrows=1)
        return data.shape[0] == 1 and data.shape[1] >= 5

    def check_columns_name_in_death_dataset(self) -> bool:
        """
        Death dataset must contain columns with name‘country’, ‘year’, ‘population’ and at least one column with causes
        of death with name starts with "d: causes"
        """
        data = pd.read_csv(self.path_to_death_dataset, nrows=0)
        if list(data.columns[:4]) != ["country", "code", "year", "population"]:
            return False
        if sum([causes.startswith("d: ") for causes in list(data.columns[4:])]) != len(
            list(data.columns[4:])
        ):
            return False
        return True

    def check_country_type_in_death_dataset(self) -> bool:
        """
        Column 'country' have to contain string
        """
        is_not_valid = True
        for chunk in pd.read_csv(self.path_to_death_dataset, chunksize=100):
            try:
                chunk["country"].astype(str)
            except ValueError:
                is_not_valid = False
                if ~is_not_valid:
                    return is_not_valid
        return is_not_valid

    def check_code_type_in_death_dataset(self) -> bool:
        """
        Column 'code' have to contain string
        """
        is_not_valid = True
        for chunk in pd.read_csv(self.path_to_death_dataset, chunksize=100):
            try:
                chunk["code"].astype(str)
            except ValueError:
                is_not_valid = False
                if ~is_not_valid:
                    return is_not_valid
        return is_not_valid

    def check_year_type_in_death_dataset(self) -> bool:
        """
        Column 'year' have to contain integer
        """
        is_not_valid = True
        for chunk in pd.read_csv(self.path_to_death_dataset, chunksize=100):
            try:
                chunk["year"].astype(int)
            except ValueError:
                is_not_valid = False
                if ~is_not_valid:
                    return is_not_valid
        return is_not_valid

    def check_population_type_in_death_dataset(self) -> bool:
        """
        Column 'population' have to contain float
        """
        is_not_valid = True
        for chunk in pd.read_csv(self.path_to_death_dataset, chunksize=100):
            try:
                chunk["population"].astype(float)
            except ValueError:
                is_not_valid = False
                if ~is_not_valid:
                    return is_not_valid
        return is_not_valid

    def check_death_type_in_death_dataset(self) -> bool:
        """
        Columns with death causes have to contain float
        """
        is_not_valid = True
        for chunk in pd.read_csv(self.path_to_death_dataset, chunksize=100):
            try:
                chunk[chunk.columns[4:]].astype(float)
            except ValueError:
                is_not_valid = False
                if ~is_not_valid:
                    return is_not_valid
        return is_not_valid

    def check_values_in_death_dataset(self) -> bool:
        """
        Columns with population, year and death causes have to contain values greater than or equal to 0
        """
        is_not_valid = True
        for chunk in pd.read_csv(self.path_to_death_dataset, chunksize=100):
            if not (chunk.iloc[:, 2:] >= 0).all().all():
                is_not_valid = False
            if ~is_not_valid:
                return is_not_valid
        return is_not_valid

    def check_row_values_in_death_dataset(self) -> bool:
        """
        Column population in each year have to be greater than summed causes of death
        """
        is_not_valid = True
        for chunk in pd.read_csv(self.path_to_death_dataset, chunksize=100):
            if not all((chunk["population"] - chunk.iloc[:, 4:].sum(axis=1)) > 0):
                is_not_valid = False
        return is_not_valid

    def check_year_and_country_in_death_dataset(self) -> bool:
        """
        Columns year for each country have to have only one row for specific year
        and the range of year must be continuous for every year
        """
        chunk = pd.read_csv(self.path_to_death_dataset, chunksize=100)
        data = pd.concat(chunk)
        is_not_valid = True
        countries = list(data["country"].unique())
        for country in countries:
            df_country = data[data["country"] == country]
            years = df_country["year"]
            is_not_valid = (sorted(years)) == list(
                np.arange(min(years), max(years) + 1)
            )
            if ~is_not_valid:
                return is_not_valid
        return is_not_valid

    def check_nan_values_in_death_dataset(self) -> bool:
        """
        Death datasets must not have NaN values
        """
        is_not_valid = True
        for chunk in pd.read_csv(self.path_to_death_dataset, chunksize=100):
            is_not_valid = chunk.isna().any().sum() == 0
            if ~is_not_valid:
                return is_not_valid
        return is_not_valid

    def check_duplication_in_death_dataset(self) -> bool:
        """
        Death datasets must not have duplications
        """
        is_not_valid = True
        for chunk in pd.read_csv(self.path_to_death_dataset, chunksize=100):
            is_not_valid = chunk.duplicated().any().sum() == 0
            if ~is_not_valid:
                return is_not_valid
        return is_not_valid

    # INDEX DATASET
    def check_minimal_size_in_index_dataset(self) -> bool:
        """
        Index dataset must contain columns ‘country’, ‘code’, ‘hdi’ and 'development' and minimal one row with data
        """
        data = pd.read_csv(self.path_to_index_dataset, nrows=1)
        return data.shape[0] == 1 and data.shape[1] == 4

    def check_columns_name_in_index_dataset(self):
        """
        Index dataset must contain columns name: ‘country’, ‘code’, ‘hdi’ and 'development'
        """
        data = pd.read_csv(self.path_to_index_dataset, nrows=0)
        return list(data.columns) == ["country", "code", "hdi", "development"]

    def check_country_type_in_index_dataset(self) -> bool:
        """
        Column 'country' have to contain string
        """
        is_not_valid = True
        for chunk in pd.read_csv(self.path_to_index_dataset, chunksize=100):
            try:
                chunk["country"].astype(str)
            except ValueError:
                is_not_valid = False
                if ~is_not_valid:
                    return is_not_valid
        return is_not_valid

    def check_code_type_in_index_dataset(self) -> bool:
        """
        Column 'code' have to contain string
        """
        is_not_valid = True
        for chunk in pd.read_csv(self.path_to_index_dataset, chunksize=100):
            try:
                chunk["code"].astype(str)
            except ValueError:
                is_not_valid = False
                if ~is_not_valid:
                    return is_not_valid
        return is_not_valid

    def check_hdi_type_in_index_dataset(self) -> bool:
        """
        Column 'hdi' have to contain float
        """
        is_not_valid = True
        for chunk in pd.read_csv(self.path_to_index_dataset, chunksize=100):
            try:
                chunk["hdi"].astype(float)
            except ValueError:
                is_not_valid = False
                if ~is_not_valid:
                    return is_not_valid
        return is_not_valid

    def check_development_type_in_index_dataset(self) -> bool:
        """
        Column 'development' have to contain string
        """
        is_not_valid = True
        for chunk in pd.read_csv(self.path_to_index_dataset, chunksize=100):
            try:
                chunk["development"].astype(str)
            except ValueError:
                is_not_valid = False
                if ~is_not_valid:
                    return is_not_valid
        return is_not_valid

    def check_nan_values_in_index_dataset(self) -> bool:
        """
        Index datasets must not have NaN values
        """
        is_not_valid = True
        for chunk in pd.read_csv(self.path_to_index_dataset, chunksize=100):
            is_not_valid = chunk.isna().any().sum() == 0
            if ~is_not_valid:
                return is_not_valid
        return is_not_valid

    def check_duplication_in_index_dataset(self) -> bool:
        """
        Index datasets must not have duplications
        """
        is_not_valid = True
        for chunk in pd.read_csv(self.path_to_index_dataset, chunksize=100):
            is_not_valid = chunk.duplicated().any().sum() == 0
            if ~is_not_valid:
                return is_not_valid
        return is_not_valid

    def check_code_in_death_and_index(self) -> bool:
        """
        Index dataset have to contain at least one country code like in death dataset
        """
        is_not_valid = False
        chunk = pd.read_csv(self.path_to_index_dataset, chunksize=100)
        index = pd.concat(chunk)
        for chunk in pd.read_csv(self.path_to_death_dataset, chunksize=100):
            is_not_valid = any(chunk["code"].isin(list(index.code)))
            if is_not_valid:
                return is_not_valid
        return is_not_valid

    def check_pipeline(self) -> bool:
        """
        Checkin pipeline
        """
        if not self.check_minimal_size_in_death_dataset():
            print("Wrong minimal size in death dataset")
            return False
        if not self.check_columns_name_in_death_dataset():
            print("Wrong columns name in death dataset")
            return False
        if not self.check_country_type_in_death_dataset():
            print("Wrong country type in death dataset")
            return False
        if not self.check_code_type_in_death_dataset():
            print("Wrong code type in death dataset")
            return False
        if not self.check_year_type_in_death_dataset():
            print("Wrong year type in death dataset")
            return False
        if not self.check_population_type_in_death_dataset():
            print("Wrong population type in death dataset")
            return False
        if not self.check_death_type_in_death_dataset():
            print("Wrong death type in death dataset")
            return False
        if not self.check_values_in_death_dataset():
            print(
                "Wrong values in columns population or year or death causes. "
                "Values have to be greater than or equal to 0 "
            )
            return False
        if not self.check_row_values_in_death_dataset():
            print(
                "Wrong values in columns with death of causes. For all rows sum of deaths cannot exceed the "
                "population."
            )
            return False
        if not self.check_year_and_country_in_death_dataset():
            print(
                "Wrong values in columns with year. For each country you have to have only one row for specific year "
                "and the range of year must be continuous for every year"
            )
            return False
        if not self.check_nan_values_in_death_dataset():
            print("Wrong values, your death dataset contain NaN.")
            return False
        if not self.check_duplication_in_death_dataset():
            print("Your death datasets contain duplication.")
            return False
        if not self.check_minimal_size_in_index_dataset():
            print("Wrong minimal size in index dataset")
            return False
        if not self.check_columns_name_in_index_dataset():
            print("Wrong columns name in index dataset")
            return False
        if not self.check_country_type_in_index_dataset():
            print("Wrong country type in index dataset")
            return False
        if not self.check_code_type_in_index_dataset():
            print("Wrong code type in index dataset")
            return False
        if not self.check_hdi_type_in_index_dataset():
            print("Wrong hid type in index dataset")
            return False
        if not self.check_development_type_in_index_dataset():
            print("Wrong development type in index dataset")
            return False
        if not self.check_nan_values_in_index_dataset():
            print("Wrong values, your index dataset contain NaN.")
            return False
        if not self.check_duplication_in_index_dataset():
            print("Your index datasets contain duplication.")
            return False
        if not self.check_code_in_death_and_index():
            print(
                "Index dataset have to contain at least one country code like in death dataset"
            )
            return False
        print("New datasets are correct.")
        return True
