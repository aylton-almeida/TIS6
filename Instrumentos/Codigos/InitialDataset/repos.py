import os
import time
import progressbar
from src import CliArgs
from src.models.AuthToken import AuthToken
from src.Graphql import Graphql
from dotenv import load_dotenv
from src.models.RepoWithCreateAt import RepoWithCreateAt
from src.models.GithubException import GithubException
from src import CsvUtils




# Load env file
load_dotenv()

# flush progress bar
# progressbar.streams.flush()


def mine_repos():

    # parse arguments
    args = CliArgs.get_args(total=('Total repos to be fetch', 1000),
                            perrequest=('Number of repos per request', 100))

    # Get env variables
    url = os.getenv('API_URL')
    token = AuthToken(os.getenv('AUTH_TOKENS').split(','))

    total_repos = int(args.total)
    repos_per_request = int(args.perrequest)

    graphql = Graphql(url, repos_per_request)

    if total_repos % repos_per_request != 0:
        raise Exception(
            'Repos per request should be divisible by total repos number')

    repo_list = []

    print('Fetching repos...')

    
    while len(repo_list) < total_repos:
        try:
            print('Current token: {}'.format(token.get_token()))
            # Build query
            query = graphql.get_repo_query()
            # Get repos
            repo_data = graphql.get_repos_data(query, token.get_token())
            # add to list
            for repo in [RepoWithCreateAt.from_github(repo) for repo in repo_data]:
                CsvUtils.save_repos_to_csv([repo], 'tempCsv', mode='a', header=False)
                if len(repo_list) == total_repos:
                    break
                elif not next((r for r in repo_list if r.name_with_owner == repo.name_with_owner), None):
                    repo_list.append(repo)
            # break if total was reach
            if len(repo_list) == total_repos:
                break
        except GithubException:
            time.sleep(len(repo_list) * 2)
            token.next_token()

    CsvUtils.save_repos_to_csv(repo_list, 'repos.csv')


if __name__ == '__main__':
    mine_repos()
