import pandas as pd
from death_app.data.processor import DataProcessor
from config import settings
import os
from plotly.graph_objects import Figure
import plotly.express as px


class Plotter:
    """
    Class which plotting data and enable save this plot
    """

    def __init__(self) -> None:
        self.data_processor = DataProcessor()

    def plot_summed(self, df: pd.DataFrame, top: int, years: tuple) -> Figure:
        """
        Shows top N causes of death in a given countries, summed across specified date range
        :param df: dataframe with specific countries and data range
        :param top: number of causes
        :param years: data range
        :return: plots
        """
        # get processed data
        result = self.data_processor.get_top_causes_summed_by_range_of_year(df, top)
        # if is only one country plot will be grouped else stacked
        # interactive plot bar horizontal

        causes = "causes" if top > 1 else "cause"
        if result.shape[0] == 1:
            fig = result.plot.barh(
                title=f"Top {top} most common {causes} of death summed from {years[0]} to "
                f"{years[1]}",
                barmode="group",
                backend="plotly",
                labels={"variable": "Causes of death"},
            )
        else:
            fig = result.plot.barh(
                title=f"Top {top} most common {causes} of death summed from {years[0]} to "
                f"{years[1]}",
                backend="plotly",
                labels={"variable": "Causes of death"},
            )
        # fig settings
        fig.update_layout(
            autosize=False,
            width=1300,
            height=800,
            font_color="#2b2828",
            title_font_color="#325aa8",
            title_font_size=20,
            title_x=0.5,
            xaxis=dict(title="Number of death per 10 000 inhabitants"),
            yaxis=dict(title="Countries"),
        )
        # New names of legend (without "d: ")
        labels = {name: name[3:] for name in list(result.columns)}
        fig.for_each_trace(
            lambda t: t.update(
                name=labels[t.name],
                legendgroup=labels[t.name],
                hovertemplate=t.hovertemplate.replace(t.name, labels[t.name]),
            )
        )

        return fig

    @staticmethod
    def save_fig(fig: Figure, file_name: str) -> None:
        """
        Saved fig to file if not exist folder - create folder
        :param fig: plots
        :param file_name: name of file which will be saved
        """
        if not os.path.exists(settings["paths"]["path_to_plots"]):
            os.makedirs(settings["paths"]["path_to_plots"])
        fig.write_image(settings["paths"]["path_to_plots"] + f"/{file_name}")

    @staticmethod
    def remove_fig(file_name: str) -> None:
        """
        Removed file
        :param file_name: name of file which will be removed
        """
        if os.path.exists(settings["paths"]["path_to_plots"] + f"/{file_name}"):
            os.remove(settings["paths"]["path_to_plots"] + f"/{file_name}")

    def plot_in_each_year(
        self, df: pd.DataFrame, top: int, years: tuple, list_of_countries: list[str]
    ) -> Figure:
        """
        Shows top N causes of death in a set of countries, in each year from a specified date range.'
        :param df: dataframe with specific countries and data range
        :param top: number of causes
        :param years: data range
        :param list_of_countries: list with countries name
        :return: plots
        """
        # get processed data
        result = self.data_processor.get_top_causes_in_each_year(df, top)
        countries = " ".join(
            [
                name + " and" if idx < len(list_of_countries) - 1 else name
                for idx, name in enumerate(list_of_countries)
            ]
        )
        causes = "causes" if top > 1 else "cause"
        fig = px.scatter(
            result,
            x="year",
            y="values",
            color="Causes of death",
            facet_col="country",
            title=f"Top {top} most common {causes} of death in {countries} in each year, from "
            f"{years[0]} to {years[1]}",
            labels={"year": "Years"},
        )
        fig.update_layout(
            autosize=False,
            width=1300,
            height=800,
            font_color="#2b2828",
            title_font_color="#325aa8",
            title_font_size=20,
            title_x=0.5,
            yaxis=dict(title="Number of death per 10 000 inhabitants"),
        )

        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig.update_annotations(font_size=15)
        # New names of legend (without "d:")
        fig.for_each_trace(
            lambda t: t.update(
                name=t.name.replace("d: ", ""),
                legendgroup=t.name.replace("d: ", ""),
                hovertemplate=t.hovertemplate.replace(
                    t.name,
                    t.name.replace("d: ", ""),
                ),
            )
        )
        return fig

    def plot_trend_cause_in_each_year(
        self, df: pd.DataFrame, cause: str, years: tuple
    ) -> Figure:
        """

        :param df:
        :param cause:
        :param years:
        :return:
        """
        result = self.data_processor.get_trend_cause_in_each_year_in_countries(
            df, cause
        )
        fig = px.line(
            result,
            x="year",
            y=f"d: {cause}",
            color="country",
            markers=True,
            title=f"{cause} death rate from {years[0]} to {years[1]}",
        )
        # plot settings
        fig.update_layout(
            autosize=False,
            width=1300,
            height=800,
            font_color="#2b2828",
            title_font_color="#325aa8",
            title_font_size=20,
            title_x=0.5,
            xaxis=dict(title="Years"),
            yaxis=dict(title="Number of death per 10 000 inhabitants"),
        )
        return fig

    def plot_summed_development(
        self, df: pd.DataFrame, top: int, years: tuple
    ) -> Figure:
        """
        Shows top N causes of death by the level of development, summed across specified date range
        :param df: dataframe with specific level of development and data range
        :param top: number of causes
        :param years: data range
        :return: plots
        """
        # get processed data
        result = self.data_processor.get_top_causes_summed_by_level_of_develop(df, top)
        # if is only one level of development - plot will be grouped else stacked
        # interactive plot bar horizontal
        causes = "causes" if top > 1 else "cause"
        if result.shape[0] == 1:
            fig = result.plot.barh(
                title=f"Top {top} most common {causes} of death by the level of development, summed from "
                f"{years[0]} to {years[1]}",
                barmode="group",
                backend="plotly",
                labels={"variable": "Causes of death"},
            )
        else:
            fig = result.plot.barh(
                title=f"Top {top} most common {causes} of death by the level of development, summed from "
                f"{years[0]} to {years[1]}",
                backend="plotly",
                labels={"variable": "Causes of death"},
            )

        # plot settings
        fig.update_layout(
            autosize=False,
            width=1300,
            height=800,
            font_color="#2b2828",
            title_font_color="#325aa8",
            title_font_size=20,
            title_x=0.5,
            xaxis=dict(title="Number of death per 100 000 inhabitants"),
            yaxis=dict(title="Level of development"),
        )
        # New names of legend (without "d:")
        fig.for_each_trace(
            lambda t: t.update(
                name=t.name.replace("d: ", ""),
                legendgroup=t.name.replace("d: ", ""),
                hovertemplate=t.hovertemplate.replace(
                    t.name,
                    t.name.replace("d: ", ""),
                ),
            )
        )

        return fig

    def plot_development_in_each_year(self, df: pd.DataFrame, top: int, years: tuple):
        """
        Shows top N causes of death by the level of development, summed across specified date range
        :param df: dataframe with specific level of development and data range
        :param top: number of causes
        :param years: data range
        :return: plots
        """
        # get processed data
        result = self.data_processor.get_top_causes_in_each_year_by_level_of_develop(
            df, top
        )
        causes = "causes" if top > 1 else "cause"
        fig = px.scatter(
            result,
            x="year",
            y="values",
            color="Causes of death",
            facet_col="development",
            title=f"Top {top} most common {causes} of death in each year from "
            f"{years[0]} to {years[1]}",
            labels={"year": "Years"},
        )
        fig.update_layout(
            autosize=False,
            width=1300,
            height=800,
            font_color="#2b2828",
            title_font_color="#325aa8",
            title_font_size=20,
            title_x=0.5,
            yaxis=dict(title="Number of death per 10 000 inhabitants"),
        )
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig.update_annotations(font_size=15)
        # New names of legend (without "d:")
        fig.for_each_trace(
            lambda t: t.update(
                name=t.name.replace("d: ", ""),
                legendgroup=t.name.replace("d: ", ""),
                hovertemplate=t.hovertemplate.replace(
                    t.name,
                    t.name.replace("d: ", ""),
                ),
            )
        )
        return fig

    def plot_trend_cause_by_development_by_year(
        self, df: pd.DataFrame, cause: str, years: tuple
    ):
        """
        Shows top N causes of death by the level of development, summed across specified date range
        :param df: dataframe with specific level of development and data range
        :param cause: number of causes
        :param years: data range
        :return: plots
        """
        # get processed data
        result = self.data_processor.get_trend_cause_in_each_year_by_level_of_develop(
            df, cause
        )
        fig = px.line(
            result,
            x="year",
            y=f"d: {cause}",
            color="development",
            markers=True,
            title=f"{cause} death rate from {years[0]} to {years[1]}",
        )
        fig.update_layout(
            autosize=True,
            width=1300,
            height=800,
            font_color="#2b2828",
            title_font_color="#325aa8",
            title_font_size=20,
            title_x=0.5,
            xaxis=dict(title="Years"),
            yaxis=dict(title="Number of death per 100 000 inhabitants"),
        )
        return fig
