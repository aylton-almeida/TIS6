import pandas as pd

from src.models.Issue import Issue


def save_repos_to_csv(issues: list, path: str, mode='w', header=True):
    data_frame = pd.DataFrame([issue.__dict__ for issue in issues])

    data_frame.to_csv(path, mode=mode, header=header)
