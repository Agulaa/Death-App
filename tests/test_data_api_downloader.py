import pandas as pd
from death_app.data.data_api_downloader import DataAPIDownloader
import os

api_downloader = DataAPIDownloader(
    year_start=2020,
    year_end=2021,
    path_to_save="res/test/test_population.csv",
    path_to_folder="res/test",
)


def test_download_population():
    """
    Check if DataAPIDownloader downloaded dataset to correct folder
    """
    assert os.path.exists("res/test/test_population.csv")


def test_duplication_population():
    """
    Check if DataAPIDownloader dropped duplicates
    """
    df = pd.read_csv("res/test/test_population.csv")
    assert ~any(df.duplicated())


def test_column_name():
    """
    Check if DataAPIDownloader preprocess dataset with correct column name
    """
    df = pd.read_csv("res/test/test_population.csv")
    assert list(df.columns) == list(["code", "year", "population"])


def test_nan_value():
    """
    Check if DataAPIDownloader dropped NaN values and fill NaN
    """
    df = pd.read_csv("res/test/test_population.csv")
    assert ~df.isnull().values.any()


def test_range_population_dataset():
    """
    Check if DataAPIDownloader downloaded data with correct range of year
    """
    df = pd.read_csv("res/test/test_population.csv")
    assert min(df["year"]) == 2020
    assert max(df["year"]) == 2021


def test_remove():
    """
    Remove test file and folder
    """
    os.remove("res/test/test_population.csv")
    os.rmdir("res/test")
    assert True
