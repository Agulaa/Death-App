from death_app.plots.plotter import Plotter
from config import settings
import os
import pandas as pd
from plotly.graph_objects import Figure


plotter = Plotter()
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


def test_plot_summed():
    """
    Test type in plot_summed()
    """
    # given
    top = 2
    years = (2017, 2018)

    # when
    fig = plotter.plot_summed(df_example, top, years)

    # then
    # type of return
    assert isinstance(fig, Figure)


def test_plot_in_each_year():
    """
    Test type in plot_in_each_year()
    """
    # given
    top = 2
    years = (2017, 2018)
    list_of_country = ["Spain"]
    # when
    fig = plotter.plot_in_each_year(df_example, top, years, list_of_country)

    # then
    # type of return
    assert isinstance(fig, Figure)


def test_plot_trend_cause_in_each_year():
    """
    Test type in plot_trend_cause_in_each_year()
    """
    # given
    cause = "Parkinson's disease"
    years = (2017, 2018)
    # when
    fig = plotter.plot_trend_cause_in_each_year(df_example, cause, years)
    # then
    # type of return
    assert isinstance(fig, Figure)


def test_plot_summed_development():
    """
    Test type in plot_summed_development()
    """
    # given
    top = 2
    years = (2017, 2018)
    df_example["development"] = ["highly", "highly", "medium", "medium"]

    # when
    fig = plotter.plot_summed_development(df_example, top, years)
    df_example.drop(columns=["development"], axis=1, inplace=True)
    # then
    # type of return
    assert isinstance(fig, Figure)


def test_plot_development_in_each_year():
    """
    Test type in plot_development_in_each_year()
    """
    # given
    years = (2017, 2018)
    df_example["development"] = ["highly", "highly", "medium", "medium"]
    top = 2

    # when
    fig = plotter.plot_development_in_each_year(df_example, top, years)
    df_example.drop(columns=["development"], axis=1, inplace=True)
    # then
    # type of return
    assert isinstance(fig, Figure)


def test_plot_trend_cause_by_development_by_year():
    """
    Test type in plot_trend_cause_by_development_by_year()
    """
    # given
    cause = "Parkinson's disease"
    df_example["development"] = ["highly", "highly", "medium", "medium"]
    years = (2017, 2018)
    # when
    fig = plotter.plot_trend_cause_by_development_by_year(df_example, cause, years)
    df_example.drop(columns=["development"], axis=1, inplace=True)
    # then
    # type of return
    assert isinstance(fig, Figure)


def test_save_fig():
    """
    Test if method remove_fig() correct saved file
    """
    # given
    df = pd.DataFrame({"a": [1, 3, 2], "b": [3, 2, 1]})
    fig = df.plot.barh(backend="plotly")

    # when
    file_name = "test_fig.png"
    plotter.save_fig(fig, file_name)

    # then
    assert os.path.exists(settings["paths"]["path_to_plots"] + f"/{file_name}")
    os.remove(settings["paths"]["path_to_plots"] + f"/{file_name}")


def test_remove_fig():
    """
    Test if method remove_fig() correct removed file
    """
    # given
    df = pd.DataFrame({"a": [1, 3, 2], "b": [3, 2, 1]})
    fig = df.plot.barh(backend="plotly")

    # when
    file_name = "test_fig.png"
    plotter.save_fig(fig, file_name)
    plotter.remove_fig(file_name)

    # then
    assert ~os.path.exists(settings["paths"]["path_to_plots"] + f"/{file_name}")
