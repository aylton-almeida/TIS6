import os
from src.models.GithubException import GithubException
import src.CsvUtils as CsvUtils
import time
from src.Graphql import Graphql
from src import CliArgs
import progressbar

from src.models.AuthToken import AuthToken
from dotenv import load_dotenv
import shutil

# Load env file
load_dotenv()

# flush progress bar
progressbar.streams.flush()


def get_issue_ratio():

    # parse arguments
    args = CliArgs.get_args(initialrepo=(
        'Initial repo index', 0), cursor=('Current cursor', None))

    # Get env variables
    url = os.getenv('API_URL')
    token = AuthToken(os.getenv('AUTH_TOKENS').split(','))

    initial_repo = int(args.initialrepo)

    graphql = Graphql(url, 100)

    # read repos csv
    repo_list = CsvUtils.read_repos_from_csv('final_ui_repos.csv')

    trimmed_repos = repo_list[initial_repo:]

    print('Fetching repos...')

    issue_list: list[dict] = []

    # extremely necessary progress bar for better user experience
    with progressbar.ProgressBar(max_value=len(trimmed_repos), redirect_stdout=True) as bar:
        for index in range(len(trimmed_repos)):
            repo = trimmed_repos[index]

            print('Fetching PRs for Repo {}, index {}'.format(
                repo.name_with_owner, index))

            # reset cursor
            graphql.cursor = args.cursor

            temp_issues_list = []

            owner, name = repo.name_with_owner.split('/')
            repo_csv = '{}_{}.csv'.format(owner, name)
            CsvUtils.create_header_file(
                repo_csv, ['index', 'createdAt', 'closedAt', 'cursor'])

            has_next_page = True
            while has_next_page:
                try:
                    print('Fetching cursor: {}'.format(graphql.cursor))

                    # get query
                    owner, name = repo.name_with_owner.split('/')
                    query = graphql.get_issues_query(owner, name)

                    # fetch prs
                    issues, has_next_page = graphql.get_issues_data(
                        query, token.get_token())

                    # sleep sometime
                    temp_issues_list += issues
                    if len(temp_issues_list) > 0 and len(temp_issues_list) % 1000 == 0:
                        time.sleep(60)

                    # add issues to list and save
                    parsed_issues = [{'createdAt': item.get('node').get(
                        'createdAt'), 'closedAt':  item.get('node').get('closedAt'), 'cursor': graphql.cursor} for item in issues]
                    issue_list += parsed_issues
                    CsvUtils.save_list_to_csv(
                        parsed_issues, repo_csv, mode='a', header=False)

                except Exception as err:
                    time.sleep(600)
                    token.next_token()

            time.sleep(180)

            # read issues csv
            # issues = CsvUtils.read_issues_from_csv(repo_csv)

            # # calculate issues and save
            # repo.calculate_issue_median(issues)

            # CsvUtils.save_list_to_csv(
            #     [repo.__dict__], 'repos_with_issues.csv', mode='a', header=False)

            # mv issues to folder
            shutil.move(repo_csv, 'issues')

            bar.update(index)


if __name__ == "__main__":
    get_issue_ratio()
