import os
from src.models.Repo import Repo
import src.utils.CsvUtils as CsvUtils
from src.utils.Graphql import Graphql
from src.utils import CliArgs

from src.models.AuthToken import AuthToken
from dotenv import load_dotenv

# Load env file
load_dotenv()


def get_issue_ratio():

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

        print('Fetching Issues for Repo {}, index {}'.format(
            repo.name_with_owner, initial_repo + index))

        # reset cursor
        graphql.cursor = None

        repo.set_bug_issues(graphql, token)

        CsvUtils.save_list_to_csv(
            [repo.__dict__], 'repos_with_issues.csv', mode='a')


if __name__ == "__main__":
    get_issue_ratio()
