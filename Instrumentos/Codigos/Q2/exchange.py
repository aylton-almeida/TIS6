import time
import progressbar
from src.models.Repo import Repo
from src import CliArgs, CsvUtils, Exchange
from dotenv import load_dotenv

# Load env file
load_dotenv()

# flush progress bar
progressbar.streams.flush()


def get_questions():

    # parse arguments
    args = CliArgs.get_args(initialrepo=('Initial repo index', 0), file=(
        'File in witch to save the results', 'repos_with_questions.csv'))

    initial_repo = int(args.initialrepo)
    file = args.file

    # read repos csv
    repo_list = CsvUtils.read_repos_from_csv('final_ui_repos.csv')

    trimmed_repos = repo_list[initial_repo:]

    print('Fetching questions...')

    repo_list: list[Repo] = []

    # extremely necessary progress bar for better user experience
    with progressbar.ProgressBar(max_value=len(trimmed_repos), redirect_stdout=True) as bar:
        for index in range(len(trimmed_repos)):
            repo = trimmed_repos[index]

            questions = None

            time.sleep(180)

            while questions is None:
                try:
                    questions = Exchange.get_questions_by_tag(repo.get_name())
                except:
                    time.sleep(600)

            repo.set_answered_questions(questions)

            if repo.answered_questions:
                CsvUtils.save_repos_to_csv(
                    [repo], file, mode='a', header=False)
            else:
                CsvUtils.save_repos_to_csv(
                    [repo], 'no_questions_found.csv', mode='a', header=False)

            bar.update(index)


if __name__ == '__main__':
    get_questions()
