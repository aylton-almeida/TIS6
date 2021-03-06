import os
import time

import progressbar
from dotenv import load_dotenv

from src import CliArgs, CsvUtils
from src.Graphql import Graphql
from src.models.AuthToken import AuthToken
from src.models.GithubException import GithubException
from src.models.Repo import Repo

# Load env file
load_dotenv()

# flush progress bar
progressbar.streams.flush()


def mine_repos():

    # parse arguments
    args = CliArgs.get_args(total=('Total repos to be fetch', 300),
                            perrequest=('Number of repos per request', 100))

    # Get env variables
    url = os.getenv('API_URL')
    token = AuthToken(os.getenv('AUTH_TOKENS').split(','))
    topics = ['react-components', 'react-component', 'vue-components', 'vue-component',
              'ui-components', 'component-library', 'components', 'webcomponents']

    total_repos = int(args.total)
    repos_per_request = int(args.perrequest)

    graphql = Graphql(url, repos_per_request, topics)

    if total_repos % repos_per_request != 0:
        raise Exception(
            'Repos per request should be divisible by total repos number')

    repo_list: list[Repo] = []

    print('Fetching repos...')

    with progressbar.ProgressBar(max_value=total_repos, redirect_stdout=True) as bar:
        while len(repo_list) < total_repos:
            try:
                print('Fetching topic: {}'.format(graphql.get_current_topic()))
                print('Fetching cursor: {}'.format(graphql.cursor))
                print('Current token: {}'.format(token.get_token()))

                # Build query
                query = graphql.get_query()

                # Get repos
                repo_data = graphql.get_repos_data(query, token.get_token())

                # add to list
                for repo in [Repo.from_github(repo) for repo in repo_data]:
                    if len(repo_list) == total_repos:
                        break
                    elif not next((r for r in repo_list if r.name_with_owner == repo.name_with_owner), None):
                        repo_list.append(repo)

                # break if total was reach
                if len(repo_list) == total_repos:
                    break

                bar.update(len(repo_list))

            except GithubException:
                time.sleep(len(repo_list) * 2)
                token.next_token()

    CsvUtils.save_repos_to_csv(repo_list, 'repos.csv')


if __name__ == '__main__':
    mine_repos()
