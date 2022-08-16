import os
from death_app.data.downloader import DataDownloader
from config import settings

# Death dataset
death = DataDownloader(
    url=settings["url"]["death"],
    path_to_save=settings["paths"]["path_death"],
    path_to_folder=settings["dirs"]["raw_data"],
)
# Population dataset
population = DataDownloader(
    url=settings["url"]["population"],
    path_to_save=settings["paths"]["path_population"],
    path_to_folder=settings["dirs"]["raw_data"],
)
# Index dataset
index = DataDownloader(
    url=settings["url"]["index"],
    path_to_save=settings["paths"]["path_index"],
    path_to_folder=settings["dirs"]["raw_data"],
)


def test_if_dataset_folder_exists():
    assert os.path.exists(settings["dirs"]["raw_data"])


def test_if_death_dataset_exists():
    assert os.path.isfile(settings["paths"]["path_death"])


def test_if_population_dataset_exists():
    assert os.path.isfile(settings["paths"]["path_population"])


def test_if_index_dataset_exists():
    assert os.path.isfile(settings["paths"]["path_index"])
