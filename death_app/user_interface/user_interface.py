import numpy as np
import streamlit as st
from death_app.data.data_loader import DataLoader
from config import settings
from death_app.plots.plotter import Plotter
from plotly.graph_objects import Figure


class UserInterface:
    """
    Displays user interface with logo, title and selected type of analysis.
    After user selects type of analysis, the app shows required input data to make analysis and plot result.
    Enables saving the plot to the folder.
    """

    def __init__(self):
        self.type_of_analysis = [
            "Shows top N causes of death in a set of countries, summed across specified date range.",
            "Shows top N causes of death in a set of countries, in each year, from a specified date range.",
            "Shows trend in cause of death in set of countries, in each year, from a specified date range.",
            "Shows top N causes of death, by the level of development, summed across specified date range.",
            "Shows top N causes of death, by the level of development, in each year, from a specified date range.",
            "Show trend in cause of death, by level of development from a specified date range.",
        ]
        self.data_loader = DataLoader(
            path_to_dataset=settings["paths"]["path_to_save_input"],
            path_to_index=settings["paths"]["path_save_index"],
        )
        self.plotter = Plotter()

    def app_window(self) -> None:
        """
        Main application window
        """
        st.set_page_config(
            page_title="Death-App",
            page_icon=settings["paths"]["path_logo"],
            layout="wide",
        )
        _, col2 = st.columns([1, 5])
        with col2:
            st.subheader("Welcome to Death application")
        _, col2, _ = st.columns([1, 4, 1])
        with col2:
            analysis = st.selectbox(
                label="Select type of analysis", options=self.type_of_analysis
            )
            if analysis == self.type_of_analysis[0]:
                self.shows_top_summed_data_range()
            elif analysis == self.type_of_analysis[1]:
                self.shows_top_by_years()
            elif analysis == self.type_of_analysis[2]:
                self.shows_causes_in_countries_by_years()
            elif analysis == self.type_of_analysis[3]:
                self.show_top_development()
            elif analysis == self.type_of_analysis[4]:
                self.show_causes_by_development_by_year()
            elif analysis == self.type_of_analysis[5]:
                self.show_trend_cause_by_development_by_year()

    @staticmethod
    def prepare_file_name_countries(
        list_of_countries: list[str], top_n: int, years: tuple
    ) -> str:
        """
        Generate name of the file from list of countries, top N and range years
        :param list_of_countries: list with countries name
        :param top_n: number
        :param years: tuple with min and max years
        :return: file name
        """
        name = (
            "_".join(["_".join(name.split()) for name in list_of_countries])
            + f"_top_ {str(top_n)}_death_causes_from_{str(years[0])}_to_{str(years[1])}.png"
        )
        if len(name) > 255:  # maximum character
            name = (
                f"Top_ {str(top_n)}_death_causes_from_{str(years[0])}_to_{str(years[1])}_in_"
                f"{str(len(list_of_countries))}_countries.png"
            )

        return name

    @staticmethod
    def prepare_file_name_development(
        cause: str, years: tuple, list_of_level: list[str]
    ):
        """
        Generate name of the file from cause's name, list of development levels and range years
        :param cause: name of death cause
        :param years: tuple with min and max years
        :param list_of_level: list with levels of development
        :return: file name
        """
        cause = "_".join(cause.replace("/", " ").split())
        levels = "_".join(list_of_level)
        return f"{cause}_death_rate__from_{str(years[0])}_to_{str(years[1])}_in_{levels}_level_of_development.png"

    def shows_top_summed_data_range(self) -> None:
        """
        Get input from user and shows top N causes of death in a set of countries, summed across specified date range.
        """
        list_of_countries = st.multiselect(
            "Choose countries (max 60)", self.data_loader.get_list_of_countries()
        )
        if len(list_of_countries) > 60:
            st.warning(
                "Maximum number to choose from is **60**, you have to reduce the number of selected countries."
            )
        top_n = st.slider(
            "Top number of death causes",
            1,
            self.data_loader.get_number_of_death_causes(),
        )
        if (len(list_of_countries) > 0) and (len(list_of_countries) <= 60):
            min_year, max_year = self.data_loader.get_range_years_for_country(
                list_of_countries
            )
            years = st.select_slider(
                "Range of years",
                options=np.arange(min_year, max_year + 1),
                value=[min_year, max_year],
            )

            df = self.data_loader.get_data_from_specific_countries_and_year(
                countries=list_of_countries, year_start=years[0], year_end=years[1]
            )
            fig = self.plotter.plot_summed(df, top_n, years)

            file_name = self.prepare_file_name_countries(
                list_of_countries, top_n, years
            )

            self.download_button(
                fig, settings["paths"]["path_to_plots"] + f"/{file_name}", file_name
            )
            st.plotly_chart(fig, use_container_width=True)

    def shows_top_by_years(self) -> None:
        """
        Get input from user and shows top N causes of death in a set of countries,
        in each year from a specified date range.'
        """
        list_of_countries = st.multiselect(
            "Choose countries (max 3)", self.data_loader.get_list_of_countries()
        )
        if len(list_of_countries) > 3:
            st.warning(
                "Maximum number to choose from is **3**, you have to reduce the number of selected countries."
            )
        top_n = st.slider(
            "Top number of death causes",
            1,
            min(5, self.data_loader.get_number_of_death_causes()),
        )
        if (len(list_of_countries) > 0) and (len(list_of_countries) <= 3):
            min_year, max_year = self.data_loader.get_range_years_for_country(
                list_of_countries
            )
            years = st.select_slider(
                "Range of years",
                options=np.arange(min_year, max_year + 1),
                value=[min_year, max_year],
            )
            df = self.data_loader.get_data_from_specific_countries_and_year(
                countries=list_of_countries, year_start=years[0], year_end=years[1]
            )
            fig = self.plotter.plot_in_each_year(df, top_n, years, list_of_countries)

            file_name = self.prepare_file_name_countries(
                list_of_countries, top_n, years
            )

            self.download_button(
                fig, settings["paths"]["path_to_plots"] + f"/{file_name}", file_name
            )
            st.plotly_chart(fig, use_container_width=True)

    def shows_causes_in_countries_by_years(self) -> None:
        """
        Get input from user and shows cause of death by countries,
        in each year across specified date range.
        """
        list_of_countries = st.multiselect(
            "Choose countries (max 25)", self.data_loader.get_list_of_countries()
        )
        if len(list_of_countries) > 25:
            st.warning(
                "Maximum number to choose from is **25**, you have to reduce the number of selected countries."
            )
        cause = st.selectbox(
            "Choose one cause of death", self.data_loader.get_death_causes()
        )

        if (len(list_of_countries) > 0) and (len(list_of_countries) <= 25) and cause:
            min_year, max_year = self.data_loader.get_range_years_for_country(
                list_of_countries
            )
            years = st.select_slider(
                "Range of years",
                options=np.arange(min_year, max_year + 1),
                value=[min_year, max_year],
            )

            df = self.data_loader.get_data_from_specific_countries_and_year(
                countries=list_of_countries, year_start=years[0], year_end=years[1]
            )

            fig = self.plotter.plot_trend_cause_in_each_year(df, cause, years)

            file_name = (
                f"{'_'.join(cause.replace('/', ' ').split())}_death_rate_in_countries_from_{str(years[0])}_to_"
                f"{str(years[1])}.png"
            )
            self.download_button(
                fig, settings["paths"]["path_to_plots"] + f"/{file_name}", file_name
            )
            st.plotly_chart(fig, use_container_width=True)

    def show_top_development(self) -> None:
        """
        Get input from user and shows top N causes of death by the level of development,
        summed across specified date range.
        """
        list_of_level = st.multiselect(
            "Choose type of development", self.data_loader.get_types_of_development()
        )
        top_n = st.slider(
            "Top number of death causes",
            1,
            self.data_loader.get_number_of_death_causes(),
        )
        min_year, max_year = self.data_loader.get_range_of_years_for_development()
        if len(list_of_level) > 0:
            years = st.select_slider(
                "Range of years",
                options=np.arange(min_year, max_year + 1),
                value=[min_year, max_year],
            )
            if len(list_of_level) > 0:

                df = self.data_loader.get_data_by_level_of_development(
                    development=list_of_level, year_start=years[0], year_end=years[1]
                )

                fig = self.plotter.plot_summed_development(df, top_n, years)

                file_name = (
                    f"top_{str(top_n)}_death_causes_from_{str(years[0])}_to_{str(years[1])}_in_"
                    f"{'_'.join(list_of_level)}_level_of_development.png"
                )

                self.download_button(
                    fig, settings["paths"]["path_to_plots"] + f"/{file_name}", file_name
                )
                st.plotly_chart(fig, use_container_width=True)

    def download_button(self, fig: Figure, path_to_fig: str, name_file: str) -> None:
        """
        User can download analysis
        :param fig: plot to save and after download remove
        :param path_to_fig: path to saved file in folder
        :param name_file: name file which will be downloaded
        """
        self.plotter.save_fig(fig, name_file)
        with open(path_to_fig, "rb") as file:
            st.download_button(
                label="Download analysis",
                data=file,
                file_name=name_file,
            )
        self.plotter.remove_fig(name_file)

    def show_causes_by_development_by_year(self):
        """
        Get input from user and shows causes of death by the level of development,
        in each year across specified date range.
        """
        list_of_level = st.multiselect(
            "Choose type of development", self.data_loader.get_types_of_development()
        )
        top_n = st.slider(
            "Top number of death causes",
            1,
            min(5, self.data_loader.get_number_of_death_causes()),
        )

        min_year, max_year = self.data_loader.get_range_of_years_for_development()
        if len(list_of_level) > 0:
            years = st.select_slider(
                "Range of years",
                options=np.arange(min_year, max_year + 1),
                value=[min_year, max_year],
            )

            df = self.data_loader.get_data_by_level_of_development(
                development=list_of_level, year_start=years[0], year_end=years[1]
            )

            fig = self.plotter.plot_development_in_each_year(df, top_n, years)

            file_name = (
                f"Top_ {str(top_n)}_death_causes_from_{str(years[0])}_to_{str(years[1])}_in_"
                f"{str(len(list_of_level))}_level_of_development.png"
            )
            self.download_button(
                fig, settings["paths"]["path_to_plots"] + f"/{file_name}", file_name
            )
            st.plotly_chart(fig, use_container_width=True)

    def show_trend_cause_by_development_by_year(self):
        """ """
        list_of_level = st.multiselect(
            "Choose type of development", self.data_loader.get_types_of_development()
        )
        cause = st.selectbox(
            "Choose one cause of death", self.data_loader.get_death_causes()
        )
        min_year, max_year = self.data_loader.get_range_of_years_for_development()
        if (len(list_of_level) > 0) and cause:
            years = st.select_slider(
                "Range of years",
                options=np.arange(min_year, max_year + 1),
                value=[min_year, max_year],
            )

            df = self.data_loader.get_data_by_level_of_development(
                development=list_of_level, year_start=years[0], year_end=years[1]
            )

            fig = self.plotter.plot_trend_cause_by_development_by_year(df, cause, years)

            file_name = self.prepare_file_name_development(cause, years, list_of_level)
            self.download_button(
                fig, settings["paths"]["path_to_plots"] + f"/{file_name}", file_name
            )
            st.plotly_chart(fig, use_container_width=True)
