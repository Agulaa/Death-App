from death_app.data.data_preprocessing_pipeline import DataPreprocessingPipeline
from config import settings
import sys


def make(population_from_api):
    dp = DataPreprocessingPipeline(
        path_death=settings["paths"]["path_death"],
        path_population=settings["paths"]["path_population"],
        path_index=settings["paths"]["path_index"],
        path_save_death=settings["paths"]["path_save_death"],
        path_save_population=settings["paths"]["path_save_population"],
        population_from_api=population_from_api,
        path_save_index=settings["paths"]["path_save_index"],
        path_to_save_input=settings["paths"]["path_to_save_input"],
    )
    dp.preprocess_data()
    dp.save_preprocessed_dataset()


if __name__ == "__main__":
    if sys.argv[1] == "true":
        make(True)
    elif sys.argv[1] == "false":
        make(False)
