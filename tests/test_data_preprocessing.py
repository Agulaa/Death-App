from death_app.data.data_preprocessing_pipeline import (
    DataPreprocessingPipeline,
)
from config import settings
import os

dp = DataPreprocessingPipeline(
    path_death=settings["paths"]["path_death"],
    path_population=settings["paths"]["path_population"],
    path_index=settings["paths"]["path_index"],
    path_save_death=settings["paths"]["path_save_death"],
    path_save_population=settings["paths"]["path_save_population"],
    population_from_api=False,
    path_save_index=settings["paths"]["path_save_index"],
    path_to_save_input=settings["paths"]["path_to_save_input"],
)
dp.preprocess_data()
dp.save_preprocessed_dataset()


def test_read_path():
    """
    Check if DataPreprocessingPipeline read good path from config file
    """
    assert dp.path_save_death == settings["paths"]["path_save_death"]


def test_death_dropped_columns():
    """
    Check dropped unnecessary columns
    """
    assert "Number of executions (Amnesty International)" not in dp.df_death.columns


def test_death_renamed_columns():
    """
    Check renamed columns name
    """
    assert all(
        name in dp.df_death.columns
        for name in ["country", "year", "code", "d: Meningitis"]
    )


def test_death_dropped_nan():
    """
    Check dropped NaN values and fill NaN
    """
    assert ~dp.df_death.isnull().values.any()


def test_death_dropped_duplicates():
    """
    Check dropped duplicates
    """
    assert ~any(dp.df_death.duplicated())


def test_population_dropped_columns():
    """
    Check dropped unnecessary columns
    """
    assert all(
        name not in dp.df_population.columns for name in ["Series Name", "Series Code"]
    )


def test_population_renamed_columns():
    """
    Check renamed columns name
    """
    assert all(name in dp.df_population.columns for name in ["country", "code"])


def test_population_dropped_nan():
    """
    Check dropped NaN values and fill NaN
    """
    assert ~dp.df_population.isnull().values.any()


def test_population_dropped_duplicates():
    """
    Check dropped duplicates
    """
    assert ~any(dp.df_population.duplicated())


def test_index_named_columns():
    """
    Check name of columns
    """
    assert all(
        name in dp.df_index.columns
        for name in ["country", "code", "hdi", "development"]
    )


def test_index_dropped_nan():
    """
    Check dropped NaN values and fill NaN
    """
    assert ~dp.df_index.isnull().values.any()


def test_index_dropped_duplicates():
    """
    Check dropped duplicates
    """
    assert ~any(dp.df_index.duplicated())


def test_if_datasets_saved():
    """
    Checks if the dataset is saved
    """
    assert os.path.exists(settings["paths"]["path_to_save_input"])
    assert os.path.exists(settings["paths"]["path_save_index"])
    assert os.path.exists(settings["paths"]["path_save_population"])
    assert os.path.exists(settings["paths"]["path_save_death"])
