import gdown
import os


class DataDownloader:
    """
    Class which download a files from Google Drive and save them to folder
    """

    def __init__(self, url: str, path_to_save: str, path_to_folder: str) -> None:
        self.url = url
        self.path_to_save = path_to_save
        self.path_to_folder = path_to_folder
        self.create_folder_if_not_exists()
        self.download_if_not_exists()

    def get_data_from_drive(self) -> None:
        gdown.download(url=self.url, output=self.path_to_save, fuzzy=True)

    def create_folder_if_not_exists(self) -> None:
        if not os.path.exists(self.path_to_folder):
            os.makedirs(self.path_to_folder)

    def download_if_not_exists(self) -> None:
        if not os.path.exists(self.path_to_save):
            self.get_data_from_drive()
