import os
import pandas as pd


def search_package(name: str):
    os.system('npm search {} > result.csv'.format(name))

    df = pd.read_csv('result.csv', delimiter='|', error_bad_lines=False)
    df.columns = df.columns.str.strip()
    pkg_name = next(
        (row['NAME'] for index, row in df.iterrows() if name in row['NAME']), None)

    os.remove('result.csv')

    return pkg_name.strip() if pkg_name else None
