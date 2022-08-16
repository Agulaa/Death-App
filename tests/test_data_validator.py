import pandas as pd
from death_app.data.data_validator import DataValidator
from config import settings
import os
import numpy as np


dv = DataValidator(
    settings["paths"]["path_to_new_death"], settings["paths"]["path_to_new_index"]
)


def test_minimal_size_in_death_dataset():
    # INCORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Spain", "Italy", "Italy"],
            "code": ["ESP", "ESP", "ITA", "ITA"],
            "year": [2017, 2018, 2017, 2018],
            "population": [46593.236, 46797.754, 60536.709, 60421.760],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    assert ~dv.check_minimal_size_in_death_dataset()
    os.remove(settings["paths"]["path_to_new_death"])
    # CORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Spain", "Italy", "Italy"],
            "code": ["ESP", "ESP", "ITA", "ITA"],
            "year": [2017, 2018, 2017, 2018],
            "population": [46593.236, 46797.754, 60536.709, 60421.760],
            "d: Parkinson's disease": [7.720, 8.036, 5.941, 6.048],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    assert dv.check_minimal_size_in_death_dataset()
    os.remove(settings["paths"]["path_to_new_death"])


def test_columns_name_in_death_dataset():
    # INCORRECT
    pd.DataFrame(
        {
            "countries": ["Spain", "Spain", "Italy", "Italy"],
            "codes": ["ESP", "ESP", "ITA", "ITA"],
            "years": [2017, 2018, 2017, 2018],
            "num_population": [46593.236, 46797.754, 60536.709, 60421.760],
            "Parkinson's disease": [7.720, 8.036, 5.941, 6.048],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    assert ~dv.check_columns_name_in_death_dataset()
    os.remove(settings["paths"]["path_to_new_death"])
    # CORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Spain", "Italy", "Italy"],
            "code": ["ESP", "ESP", "ITA", "ITA"],
            "year": [2017, 2018, 2017, 2018],
            "population": [46593.236, 46797.754, 60536.709, 60421.760],
            "d: Parkinson's disease": [7.720, 8.036, 5.941, 6.048],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    assert dv.check_columns_name_in_death_dataset()
    os.remove(settings["paths"]["path_to_new_death"])


def test_country_type_in_death_dataset():
    # INCORRECT
    pd.DataFrame(
        {
            "country": ["Spain", 122, "Italy", 122],
            "code": ["ESP", "ESP", "ITA", "ITA"],
            "year": [2017, 2018, 2017, 2018],
            "population": [46593.236, 46797.754, 60536.709, 60421.760],
            "d: Parkinson's disease": [7.720, 8.036, 5.941, 6.048],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    assert ~dv.check_country_type_in_death_dataset()
    os.remove(settings["paths"]["path_to_new_death"])
    # CORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Spain", "Italy", "Italy"],
            "code": ["ESP", "ESP", "ITA", "ITA"],
            "year": [2017, 2018, 2017, 2018],
            "population": [46593.236, 46797.754, 60536.709, 60421.760],
            "d: Parkinson's disease": [7.720, 8.036, 5.941, 6.048],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    assert dv.check_country_type_in_death_dataset()
    os.remove(settings["paths"]["path_to_new_death"])


def test__code_type_in_death_dataset():
    # INCORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Spain", "Italy", "Italy"],
            "code": ["ESP", 122, "ITA", 122],
            "year": [2017, 2018, 2017, 2018],
            "population": [46593.236, 46797.754, 60536.709, 60421.760],
            "d: Parkinson's disease": [7.720, 8.036, 5.941, 6.048],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    assert ~dv.check_code_type_in_death_dataset()
    os.remove(settings["paths"]["path_to_new_death"])
    # CORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Spain", "Italy", "Italy"],
            "code": ["ESP", "ESP", "ITA", "ITA"],
            "year": [2017, 2018, 2017, 2018],
            "population": [46593.236, 46797.754, 60536.709, 60421.760],
            "d: Parkinson's disease": [7.720, 8.036, 5.941, 6.048],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    assert dv.check_code_type_in_death_dataset()
    os.remove(settings["paths"]["path_to_new_death"])


def test_year_type_in_death_dataset():
    # INCORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Spain", "Italy", "Italy"],
            "code": ["ESP", "ESP", "ITA", "ITA"],
            "year": [2017, "yey", 2017, "year 2018"],
            "population": [46593.236, 46797.754, 60536.709, 60421.760],
            "d: Parkinson's disease": [7.720, 8.036, 5.941, 6.048],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    assert ~dv.check_year_type_in_death_dataset()
    os.remove(settings["paths"]["path_to_new_death"])
    # CORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Spain", "Italy", "Italy"],
            "code": ["ESP", "ESP", "ITA", "ITA"],
            "year": [2017, 2018, 2017, 2018],
            "population": [46593.236, 46797.754, 60536.709, 60421.760],
            "d: Parkinson's disease": [7.720, 8.036, 5.941, 6.048],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    assert dv.check_year_type_in_death_dataset()
    os.remove(settings["paths"]["path_to_new_death"])


def test_population_type_in_death_dataset():
    # INCORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Spain", "Italy", "Italy"],
            "code": ["ESP", "ESP", "ITA", "ITA"],
            "year": [2017, 2018, 2017, 2018],
            "population": ["46593.236s", 46797.754, "population", 60421.760],
            "d: Parkinson's disease": [7.720, 8.036, 5.941, 6.048],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    assert ~dv.check_population_type_in_death_dataset()
    os.remove(settings["paths"]["path_to_new_death"])
    # CORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Spain", "Italy", "Italy"],
            "code": ["ESP", "ESP", "ITA", "ITA"],
            "year": [2017, 2018, 2017, 2018],
            "population": [46593.236, 46797.754, 60536.709, 60421.760],
            "d: Parkinson's disease": [7.720, 8.036, 5.941, 6.048],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    assert dv.check_population_type_in_death_dataset()
    os.remove(settings["paths"]["path_to_new_death"])


def test_death_type_in_death_dataset():
    # INCORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Spain", "Italy", "Italy"],
            "code": ["ESP", "ESP", "ITA", "ITA"],
            "year": [2017, 2018, 2017, 2018],
            "population": [46593.236, 46797.754, 60536.709, 60421.760],
            "d: Parkinson's disease": [7.720, "8.036s", "parkinson", 6.048],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    assert ~dv.check_death_type_in_death_dataset()
    os.remove(settings["paths"]["path_to_new_death"])
    # CORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Spain", "Italy", "Italy"],
            "code": ["ESP", "ESP", "ITA", "ITA"],
            "year": [2017, 2018, 2017, 2018],
            "population": [46593.236, 46797.754, 60536.709, 60421.760],
            "d: Parkinson's disease": [7.720, 8.036, 5.941, 6.048],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    assert dv.check_death_type_in_death_dataset()
    os.remove(settings["paths"]["path_to_new_death"])


def test_values_in_death_dataset():
    # INCORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Spain", "Italy", "Italy"],
            "code": ["ESP", "ESP", "ITA", "ITA"],
            "year": [2017, 2018, -2017, 2018],
            "population": [-46593.236, 46797.754, 60536.709, 60421.760],
            "d: Parkinson's disease": [7.720, -8.036, 5.941, 6.048],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    assert ~dv.check_values_in_death_dataset()
    os.remove(settings["paths"]["path_to_new_death"])
    # CORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Spain", "Italy", "Italy"],
            "code": ["ESP", "ESP", "ITA", "ITA"],
            "year": [2017, 2018, 2017, 2018],
            "population": [46593.236, 46797.754, 60536.709, 60421.760],
            "d: Parkinson's disease": [7.720, 8.036, 5.941, 6.048],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    assert dv.check_values_in_death_dataset()
    os.remove(settings["paths"]["path_to_new_death"])


def test_row_values_in_death_dataset():
    # INCORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Spain", "Italy", "Italy"],
            "code": ["ESP", "ESP", "ITA", "ITA"],
            "year": [2017, 2018, 2017, 2018],
            "population": [3.236, 46797.754, 2.0, 0.760],
            "d: Parkinson's disease": [7.720, 8.036, 5.941, 6.048],
            "d: Acute hepatitis": [1.04, 2.04, 0.08, 0.014],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    assert ~dv.check_row_values_in_death_dataset()
    os.remove(settings["paths"]["path_to_new_death"])
    # CORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Spain", "Italy", "Italy"],
            "code": ["ESP", "ESP", "ITA", "ITA"],
            "year": [2017, 2018, 2017, 2018],
            "population": [46593.236, 46797.754, 60536.709, 60421.760],
            "d: Parkinson's disease": [7.720, 8.036, 5.941, 6.048],
            "d: Acute hepatitis": [1.04, 2.04, 0.08, 0.014],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    assert dv.check_row_values_in_death_dataset()
    os.remove(settings["paths"]["path_to_new_death"])


def test_year_and_country_in_death_dataset():
    # INCORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Spain", "Italy", "Italy"],
            "code": ["ESP", "ESP", "ITA", "ITA"],
            "year": [2017, 2019, 2020, 2020],
            "population": [46593.236, 46797.754, 60536.709, 60421.760],
            "d: Parkinson's disease": [7.720, 8.036, 5.941, 6.048],
            "d: Acute hepatitis": [1.04, 2.04, 0.08, 0.014],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    assert ~dv.check_year_and_country_in_death_dataset()
    os.remove(settings["paths"]["path_to_new_death"])
    # CORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Spain", "Italy", "Italy"],
            "code": ["ESP", "ESP", "ITA", "ITA"],
            "year": [2017, 2018, 2017, 2018],
            "population": [46593.236, 46797.754, 60536.709, 60421.760],
            "d: Parkinson's disease": [7.720, 8.036, 5.941, 6.048],
            "d: Acute hepatitis": [1.04, 2.04, 0.08, 0.014],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    assert dv.check_year_and_country_in_death_dataset()
    os.remove(settings["paths"]["path_to_new_death"])


def test_nan_values_in_death_dataset():
    # INCORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Spain", "Italy", np.nan],
            "code": ["ESP", "ESP", "ITA", "ITA"],
            "year": [2017, np.nan, 2017, 2018],
            "population": [46593.236, 46797.754, 60536.709, 60421.760],
            "d: Parkinson's disease": [7.720, 8.036, 5.941, 6.048],
            "d: Acute hepatitis": [1.04, 2.04, 0.08, 0.014],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    assert ~dv.check_nan_values_in_death_dataset()
    os.remove(settings["paths"]["path_to_new_death"])
    # CORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Spain", "Italy", "Italy"],
            "code": ["ESP", "ESP", "ITA", "ITA"],
            "year": [2017, 2018, 2017, 2018],
            "population": [46593.236, 46797.754, 60536.709, 60421.760],
            "d: Parkinson's disease": [7.720, 8.036, 5.941, 6.048],
            "d: Acute hepatitis": [1.04, 2.04, 0.08, 0.014],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    assert dv.check_nan_values_in_death_dataset()
    os.remove(settings["paths"]["path_to_new_death"])


def test_duplication_in_death_dataset():
    # INCORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Spain", "Italy", "Italy"],
            "code": ["ESP", "ESP", "ITA", "ITA"],
            "year": [2017, 2017, 2020, 2020],
            "population": [46593.236, 46593.236, 60536.709, 60421.760],
            "d: Parkinson's disease": [7.720, 7.720, 5.941, 6.048],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    assert ~dv.check_duplication_in_death_dataset()
    os.remove(settings["paths"]["path_to_new_death"])
    # CORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Spain", "Italy", "Italy"],
            "code": ["ESP", "ESP", "ITA", "ITA"],
            "year": [2017, 2018, 2017, 2018],
            "population": [46593.236, 46797.754, 60536.709, 60421.760],
            "d: Parkinson's disease": [7.720, 8.036, 5.941, 6.048],
            "d: Acute hepatitis": [1.04, 2.04, 0.08, 0.014],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    assert dv.check_duplication_in_death_dataset()
    os.remove(settings["paths"]["path_to_new_death"])


def test_minimal_size_in_index_dataset():
    # INCORRECT
    pd.DataFrame({"country": [], "code": [], "hdi": [], "development": []}).to_csv(
        settings["paths"]["path_to_new_index"], index=False
    )
    assert ~dv.check_minimal_size_in_index_dataset()
    os.remove(settings["paths"]["path_to_new_index"])
    pd.DataFrame(
        {
            "country": ["Spain"],
            "code": ["ESP"],
            "hdi": [0.720],
            "development": ["highly"],
        }
    ).to_csv(settings["paths"]["path_to_new_index"], index=False)
    assert dv.check_minimal_size_in_index_dataset()
    os.remove(settings["paths"]["path_to_new_index"])


def test_columns_name_in_index_dataset():
    # INCORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Italy"],
            "code": ["ESP", "ITA"],
            "hdi": [0.720, 0.636],
            "development": ["highly", "medium"],
        }
    ).to_csv(settings["paths"]["path_to_new_index"], index=False)
    assert ~dv.check_columns_name_in_index_dataset()
    os.remove(settings["paths"]["path_to_new_index"])
    pd.DataFrame(
        {
            "country": ["Spain", "Italy"],
            "code": ["ESP", "ITA"],
            "hdi": [0.720, 0.636],
            "development": ["highly", "medium"],
        }
    ).to_csv(settings["paths"]["path_to_new_index"], index=False)
    assert dv.check_columns_name_in_index_dataset()
    os.remove(settings["paths"]["path_to_new_index"])


def test_country_type_in_index_dataset():
    # INCORRECT
    pd.DataFrame(
        {
            "country": [111, "Italy"],
            "code": ["ESP", "ITA"],
            "hdi": [0.720, 0.636],
            "development": ["highly", "medium"],
        }
    ).to_csv(settings["paths"]["path_to_new_index"], index=False)
    assert ~dv.check_country_type_in_index_dataset()
    os.remove(settings["paths"]["path_to_new_index"])
    pd.DataFrame(
        {
            "country": ["Spain", "Italy"],
            "code": ["ESP", "ITA"],
            "hdi": [0.720, 0.636],
            "development": ["highly", "medium"],
        }
    ).to_csv(settings["paths"]["path_to_new_index"], index=False)
    assert dv.check_country_type_in_index_dataset()
    os.remove(settings["paths"]["path_to_new_index"])


def test_code_type_in_index_dataset():
    # INCORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Italy"],
            "code": [123, "ITA"],
            "hdi": [0.720, 0.636],
            "development": ["highly", "medium"],
        }
    ).to_csv(settings["paths"]["path_to_new_index"], index=False)
    assert ~dv.check_code_type_in_index_dataset()
    os.remove(settings["paths"]["path_to_new_index"])
    pd.DataFrame(
        {
            "country": ["Spain", "Italy"],
            "code": ["ESP", "ITA"],
            "hdi": [0.720, 0.636],
            "development": ["highly", "medium"],
        }
    ).to_csv(settings["paths"]["path_to_new_index"], index=False)
    assert dv.check_code_type_in_index_dataset()
    os.remove(settings["paths"]["path_to_new_index"])


def test_hdi_type_in_index_dataset():
    # INCORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Italy"],
            "code": [123, "ITA"],
            "hdi": ["0.720s", 0.636],
            "development": ["highly", "medium"],
        }
    ).to_csv(settings["paths"]["path_to_new_index"], index=False)
    assert ~dv.check_hdi_type_in_index_dataset()
    os.remove(settings["paths"]["path_to_new_index"])
    pd.DataFrame(
        {
            "country": ["Spain", "Italy"],
            "code": ["ESP", "ITA"],
            "hdi": [0.720, 0.636],
            "development": ["highly", "medium"],
        }
    ).to_csv(settings["paths"]["path_to_new_index"], index=False)
    assert dv.check_hdi_type_in_index_dataset()
    os.remove(settings["paths"]["path_to_new_index"])


def test_development_type_in_index_dataset():
    # INCORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Italy"],
            "code": [123, "ITA"],
            "hdi": ["0.720s", 0.636],
            "development": ["highly", "medium"],
        }
    ).to_csv(settings["paths"]["path_to_new_index"], index=False)
    assert ~dv.check_development_type_in_index_dataset()
    os.remove(settings["paths"]["path_to_new_index"])
    pd.DataFrame(
        {
            "country": ["Spain", "Italy"],
            "code": ["ESP", "ITA"],
            "hdi": [0.720, 0.636],
            "development": ["highly", "medium"],
        }
    ).to_csv(settings["paths"]["path_to_new_index"], index=False)
    assert dv.check_development_type_in_index_dataset()
    os.remove(settings["paths"]["path_to_new_index"])


def test_nan_values_in_index_dataset():
    # INCORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Italy"],
            "code": [123, "ITA"],
            "hdi": [0.720, np.nan],
            "development": ["highly", "medium"],
        }
    ).to_csv(settings["paths"]["path_to_new_index"], index=False)
    assert ~dv.check_nan_values_in_index_dataset()
    os.remove(settings["paths"]["path_to_new_index"])
    pd.DataFrame(
        {
            "country": ["Spain", "Italy"],
            "code": ["ESP", "ITA"],
            "hdi": [0.720, 0.636],
            "development": ["highly", "medium"],
        }
    ).to_csv(settings["paths"]["path_to_new_index"], index=False)
    assert dv.check_nan_values_in_index_dataset()
    os.remove(settings["paths"]["path_to_new_index"])


def test_duplication_in_index_dataset():
    # INCORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Spain"],
            "code": ["ESP", "ESP"],
            "hdi": [0.720, 0.720],
            "development": ["highly", "highly"],
        }
    ).to_csv(settings["paths"]["path_to_new_index"], index=False)
    assert ~dv.check_duplication_in_index_dataset()
    os.remove(settings["paths"]["path_to_new_index"])
    pd.DataFrame(
        {
            "country": ["Spain", "Italy"],
            "code": ["ESP", "ITA"],
            "hdi": [0.720, 0.636],
            "development": ["highly", "medium"],
        }
    ).to_csv(settings["paths"]["path_to_new_index"], index=False)
    assert dv.check_duplication_in_index_dataset()
    os.remove(settings["paths"]["path_to_new_index"])


def test_code_in_death_and_index():
    # INCORRECT
    pd.DataFrame(
        {
            "country": ["Italy", "Italy"],
            "code": ["ITA", "ITA"],
            "year": [2017, 2018],
            "population": [60536.709, 60421.760],
            "d: Parkinson's disease": [5.941, 6.048],
            "d: Acute hepatitis": [0.08, 0.014],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    pd.DataFrame(
        {
            "country": ["Spain"],
            "code": ["ESP"],
            "hdi": [0.720],
            "development": ["highly"],
        }
    ).to_csv(settings["paths"]["path_to_new_index"], index=False)
    assert ~dv.check_code_in_death_and_index()
    os.remove(settings["paths"]["path_to_new_index"])
    # CORRECT
    pd.DataFrame(
        {
            "country": ["Spain", "Spain", "Italy", "Italy"],
            "code": ["ESP", "ESP", "ITA", "ITA"],
            "year": [2017, 2018, 2017, 2018],
            "population": [46593.236, 46797.754, 60536.709, 60421.760],
            "d: Parkinson's disease": [7.720, 8.036, 5.941, 6.048],
            "d: Acute hepatitis": [1.04, 2.04, 0.08, 0.014],
        }
    ).to_csv(settings["paths"]["path_to_new_death"], index=False)
    pd.DataFrame(
        {
            "country": ["Spain"],
            "code": ["ESP"],
            "hdi": [0.720],
            "development": ["highly"],
        }
    ).to_csv(settings["paths"]["path_to_new_index"], index=False)
    assert dv.check_code_in_death_and_index()
    os.remove(settings["paths"]["path_to_new_index"])
