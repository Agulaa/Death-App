from death_app.data.data_validator import DataValidator
from config import settings
import os


def check_new_data(path_to_death_dataset, path_to_index_dataset):
    dv = DataValidator(path_to_death_dataset, path_to_index_dataset)
    is_correct = dv.check_pipeline()
    return is_correct


def replace_new_data_if_correct():
    path_to_death_dataset = settings["paths"]["path_to_new_death"]
    path_to_index_dataset = settings["paths"]["path_to_new_index"]
    if check_new_data(path_to_death_dataset, path_to_index_dataset):
        if not os.path.exists(settings["dirs"]["data_root"]):
            os.makedirs(settings["dirs"]["data_root"])

        # Death
        os.replace(path_to_death_dataset, settings["paths"]["path_to_save_input"])
        # Index
        os.replace(path_to_index_dataset, settings["paths"]["path_save_index"])


if __name__ == "__main__":
    replace_new_data_if_correct()
