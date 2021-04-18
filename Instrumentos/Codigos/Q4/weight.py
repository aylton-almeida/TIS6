import os
import time
import src.utils.CsvUtils as CsvUtils
from src.utils.Graphql import Graphql
from src.utils import CliArgs

from src.models.AuthToken import AuthToken
from dotenv import load_dotenv

# Load env file
load_dotenv()


def measure_repos():

    # parse arguments
    args = CliArgs.get_args(initialrepo=('Initial repo index', 0))

    # Get env variables
    url = os.getenv('API_URL')
    token = AuthToken(os.getenv('AUTH_TOKENS').split(','))

    initial_repo = int(args.initialrepo)

    graphql = Graphql(url, 100)

    # read repos csv
    repo_list = CsvUtils.read_repos_from_csv('final_ui_repos.csv')

    trimmed_repos = repo_list[initial_repo:]

    print('Fetching repos...')

    for index in range(len(trimmed_repos)):
        repo = trimmed_repos[index]

        print('Fetching PRs for Repo {}, index {}'.format(
            repo.name_with_owner, initial_repo + index))

        # get repo weight
        repo.set_weight(graphql, token.get_token())

        CsvUtils.save_list_to_csv(
            [repo.__dict__], 'repos_with_weight.csv', mode='a')

        time.sleep(1)


if __name__ == "__main__":
    measure_repos()
