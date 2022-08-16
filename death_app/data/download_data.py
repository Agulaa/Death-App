from death_app.data.downloader import DataDownloader
from config import settings
from death_app.data.data_api_downloader import DataAPIDownloader
import pandas as pd
import sys


def download(new_death_datasets: bool = False) -> None:
    # Population dataset
    if new_death_datasets:
        death = pd.read_csv(settings["paths"]["path_death"], usecols=["Year"])
        DataAPIDownloader(
            year_start=min(death["Year"]),
            year_end=max(death["Year"]),
            path_to_save=settings["paths"]["path_save_population"],
            path_to_folder=settings["dirs"]["data_root"],
        )
    else:
        DataDownloader(
            url=settings["url"]["population"],
            path_to_save=settings["paths"]["path_population"],
            path_to_folder=settings["dirs"]["raw_data"],
        )
        # Death dataset
        DataDownloader(
            url=settings["url"]["death"],
            path_to_save=settings["paths"]["path_death"],
            path_to_folder=settings["dirs"]["raw_data"],
        )
    # Index dataset
    DataDownloader(
        url=settings["url"]["index"],
        path_to_save=settings["paths"]["path_index"],
        path_to_folder=settings["dirs"]["raw_data"],
    )


if __name__ == "__main__":
    if sys.argv[1] == "new":
        download(False)
    elif sys.argv[1] == "complete":
        download(True)
