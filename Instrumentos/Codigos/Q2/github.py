import os
from src.models.GithubException import GithubException
import src.CsvUtils as CsvUtils
import time
import src.CliArgs as CLI
import progressbar

from src.models.AuthToken import AuthToken
from src.models.Repo import Repo
from dotenv import load_dotenv
from src.Graphql import Graphql

# Load env file
load_dotenv()

# flush progress bar
progressbar.streams.flush()


def mine_repos():

    # Parse arguments
    args = CLI.get_args()

    # Get env variables
    url = os.getenv('API_URL')
    token = AuthToken(os.getenv('AUTH_TOKENS').split(','))
    topics = ['react-components', 'vue-components', 'material-components',
              'material-design', 'ui-design', 'ui-components']

    total_repos = int(args.total)
    repos_per_request = int(args.per_request)

    graphql = Graphql(url, repos_per_request, topics)

    if total_repos % repos_per_request != 0:
        raise Exception(
            'Repos per request should be divisible by total repos number')

    repo_list: list[Repo] = []

    print('Fetching repos...')

    current_cursor = args.cursor

    for _i in progressbar.progressbar(range(total_repos // repos_per_request), redirect_stdout=True):
        try:
            print('Fetching cursor: {}'.format(current_cursor))
            print('Current token: {}'.format(token.get_token()))

            # Build query
            query = graphql.get_query(current_cursor)

            # Get repos
            repo_data = graphql.get_repos_data(query, token.get_token())

            # add to list
            repo_list = [*repo_list, *
                         [Repo.from_github(repo) for repo in repo_data]]

            # break if total was reach
            if len(repo_list) == total_repos:
                break

            # set next cursor
            current_cursor = repo_list[-1].cursor if len(
                repo_list) > 0 else None

        except GithubException:
            time.sleep(len(repo_list) * 2)
            token.next_token()

    CsvUtils.save_repos_to_csv(repo_list, 'repos.csv')


if __name__ == "__main__":
    mine_repos()
