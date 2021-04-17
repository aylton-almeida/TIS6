import time
from src.models.Repo import Repo
from src import CliArgs, CsvUtils, Exchange
from dotenv import load_dotenv

# Load env file
load_dotenv()


def get_questions():

    # parse arguments
    args = CliArgs.get_args(initialrepo=('Initial repo index', 0), out=(
        'File in where to save the results', 'repos_with_questions.csv'), input=(
        'File from where to read the repos', 'final_ui_repos.csv'))

    initial_repo = int(args.initialrepo)
    out = args.out
    input = args.input

    # read repos csv
    repo_list = CsvUtils.read_repos_from_csv(input)

    trimmed_repos = repo_list[initial_repo:]

    print('Fetching questions...')

    repo_list: list[Repo] = []

    for index in range(len(trimmed_repos)):
        repo = trimmed_repos[index]

        questions = None

        time.sleep(1)

        print('Fetching repo {}...'.format(repo.name_with_owner))

        while questions is None:
            try:
                questions = Exchange.get_questions_by_tag(repo.get_name())
            except:
                time.sleep(180)

        repo.set_answered_questions(questions)

        if repo.answered_questions:
            CsvUtils.save_list_to_csv(
                [repo.__dict__], out, mode='a', header=False)
        else:
            CsvUtils.save_list_to_csv(
                [repo.__dict__], 'no_questions_found.csv', mode='a', header=False)


if __name__ == '__main__':
    get_questions()
