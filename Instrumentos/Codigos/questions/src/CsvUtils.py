import pandas as pd

from src.models.Issue import Issue


def save_repos_to_csv(issues: list, path: str, mode='w', header=True):
    data_frame = pd.DataFrame([issue.__dict__ for issue in issues])

    data_frame.to_csv(path, mode=mode, header=header)


def read_repos_from_csv(csv: str, delimiter: str = ','):
    data_frame = pd.read_csv(csv, delimiter)

    return [Repo.from_dataframe(row) for index, row in data_frame.iterrows()]


def read_issues_from_csv(csv: str, delimiter: str = ','):
    data_frame = pd.read_csv(csv, delimiter)

    return [{'createdAt': row['createdAt'], 'closedAt':  row['closedAt']} for index, row in data_frame.iterrows()]

def create_header_file(csv: str, header: list):
    with open(csv, 'w') as file:
        file.write(','.join(header + ['\n']))
