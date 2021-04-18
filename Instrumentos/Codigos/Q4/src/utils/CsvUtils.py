import pandas as pd
import os

from src.models.Repo import Repo


def save_list_to_csv(items: list, path: str, mode='w'):
    data_frame = pd.DataFrame([item for item in items])

    header = True
    if mode == 'a' and os.path.exists(path):
        header = False

    data_frame.to_csv(path, mode=mode, header=header)


def read_repos_from_csv(csv: str, delimiter: str = ','):
    data_frame = pd.read_csv(csv, delimiter)

    return [Repo.from_dataframe(row) for index, row in data_frame.iterrows()]
