import pandas as pd
from death_app.data.processor import DataProcessor

processor = DataProcessor()

df_example = pd.DataFrame(
    {
        "country": ["Spain", "Spain", "Italy", "Italy"],
        "code": ["ESP", "ESP", "ITA", "ITA"],
        "year": [2017, 2018, 2017, 2018],
        "population": [46593.236, 46797.754, 60536.709, 60421.760],
        "d: Parkinson's disease": [7.720, 8.036, 5.941, 6.048],
        "d: Acute hepatitis": [1.04, 2.04, 0.08, 0.014],
        "d: Digestive diseases": [4.14, 3.45, 2.2, 1.114],
        "d: Cardiovascular diseases": [6.14, 2.45, 7.2, 8.114],
    }
)


def test_get_top_causes_summed_by_range_of_year():
    """
    Test if dataprocessor prepare correct dataframe with correct number of countries and correct number of top causes
    in method get_top_causes_summed_by_range_of_year
    """
    # given
    top = 2
    list_of_countries = ["Spain", "Italy"]
    # when
    df_result = processor.get_top_causes_summed_by_range_of_year(df_example, top)

    # then
    # number of countries and top number
    assert (
        df_result.shape[0] == len(list_of_countries)
        and (df_result.iloc[:1, :] > 0).sum(axis=1).values == top
    )


def test_get_top_causes_in_each_year():
    """
    Test if dataprocessor prepare correct dataframe with correct name of columns
    in method get_top_causes_in_each_year()
    """
    # given
    top = 2

    # when
    df_result = processor.get_top_causes_in_each_year(df_example, top)

    # if result size is correct
    # year, country, causes of death, values
    assert sorted(list(df_result.columns)) == sorted(
        ["year", "country", "Causes of death", "values"]
    )


def test_get_trend_cause_in_each_year_in_countries():
    """
    Test if dataprocessor prepare correct dataframe with correct number of causes
    in method get_trend_cause_in_each_year_in_countries
    """
    cause = "Parkinson's disease"

    # when
    df_result = processor.get_trend_cause_in_each_year_in_countries(df_example, cause)
    # update causes name
    cause = f"d: {cause}"
    # then

    assert list(df_result.columns) == ["country", "year", cause]


def test_get_top_causes_summed_by_level_of_develop():
    """
    Test if dataprocessor prepare correct dataframe with correct number of death causes
    and correct number of level of development
    in method get_top_causes_summed_by_level_of_develop
    """
    # given
    top = 2
    list_of_development = ["highly", "medium"]
    df_example["development"] = ["highly", "highly", "medium", "medium"]

    # when
    df_result = processor.get_top_causes_summed_by_level_of_develop(df_example, top)
    df_example.drop(columns=["development"], axis=1, inplace=True)

    # then
    # top causes and number of levels
    assert sum((df_result.iloc[:, :] > 0).sum(axis=1).values) == top * len(
        list_of_development
    )


def test_get_top_causes_in_each_year_by_level_of_develop():
    """
    Test if dataprocessor prepare correct dataframe with correct name of columns
    in method get_top_causes_in_each_year_by_level_of_develop
    """
    # given
    df_example["development"] = ["highly", "highly", "medium", "medium"]
    top = 2

    # when
    df_result = processor.get_top_causes_in_each_year_by_level_of_develop(
        df_example, top
    )
    df_example.drop(columns=["development"], axis=1, inplace=True)

    assert sorted(list(df_result.columns)) == sorted(
        ["year", "development", "Causes of death", "values"]
    )


def test_get_trend_cause_in_each_year_by_level_of_develop():
    """
    Test if dataprocessor prepare correct dataframe with correct name of columns
    in method get_trend_cause_in_each_year_by_level_of_develop
    """
    cause = "Parkinson's disease"
    df_example["development"] = ["highly", "highly", "medium", "medium"]
    # when
    df_result = processor.get_trend_cause_in_each_year_by_level_of_develop(
        df_example, cause
    )
    # update causes name
    cause = f"d: {cause}"
    # then
    df_example.drop(columns=["development"], axis=1, inplace=True)
    assert list(df_result.columns) == ["year", "development", cause]
