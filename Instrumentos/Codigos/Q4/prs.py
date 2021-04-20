import os

from dotenv import load_dotenv

import src.utils.CsvUtils as CsvUtils
from src.models.AuthToken import AuthToken
from src.models.Repo import Repo
from src.utils import CliArgs
from src.utils.Graphql import Graphql

# Load env file
load_dotenv()


def get_commits_ratio():

    # parse arguments
    args = CliArgs.get_args(initialrepo=('Initial repo index', 0))

    # Get env variables
    url = os.getenv('API_URL')
    token = AuthToken(os.getenv('AUTH_TOKENS').split(','))

    initial_repo = int(args.initialrepo)

    graphql = Graphql(url, 100)

    # read repos csv
    repo_list = CsvUtils.read_repos_from_csv('final_ui_repos.csv')

    trimmed_repos: list[Repo] = repo_list[initial_repo:]

    print('Fetching repos...')

    for index in range(len(trimmed_repos)):
        repo = trimmed_repos[index]

        print('Fetching Prs for Repo {}, index {}'.format(
            repo.name_with_owner, initial_repo + index))

        # reset cursor
        graphql.cursor = None

        repo.set_bug_prs(graphql, token)

        CsvUtils.save_list_to_csv(
            [repo.__dict__], 'repos_with_prs2.csv', mode='a')


if __name__ == "__main__":
    get_commits_ratio()
