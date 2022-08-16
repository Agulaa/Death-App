from death_app.data.data_loader import DataLoader
from config import settings
import pandas as pd

data_loader = DataLoader(
    path_to_dataset=settings["paths"]["path_to_save_input"],
    path_to_index=settings["paths"]["path_save_index"],
)


def test_type_get_list_of_countries():
    assert isinstance(data_loader.get_list_of_countries(), list)


def test_type_get_number_of_death_causes():
    assert isinstance(data_loader.get_number_of_death_causes(), int)


def test_type_get_types_of_development():
    assert isinstance(data_loader.get_types_of_development(), list)


def test_type_get_range_years_for_country():
    assert isinstance(data_loader.get_range_years_for_country(["Afghanistan"]), tuple)


def test_type_get_data_from_specific_countries_and_year():
    assert isinstance(
        data_loader.get_data_from_specific_countries_and_year(
            ["Afghanistan"], 2002, 2003
        ),
        pd.DataFrame,
    )


def test_type_get_range_of_years_for_development():
    assert isinstance(data_loader.get_range_of_years_for_development(), tuple)


def test_type_get_data_by_level_of_development():
    assert isinstance(
        data_loader.get_data_by_level_of_development(["low"], 2002, 2003), pd.DataFrame
    )


def test_type_get_death_causes():
    assert isinstance(data_loader.get_death_causes(), list)
