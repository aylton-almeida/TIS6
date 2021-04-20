from datetime import datetime

from stackapi import StackAPI

from pandas import *
from src.models.Question import Question

csvName = "final_ui_repos.csv"
data = read_csv(csvName)
names = data['name'].tolist()

for name in names:
    exchange = StackAPI('stackoverflow')
    exchange.page_size = 100
    exchange.max_pages = 10
    raw_questions = exchange.fetch('questions', tagged='material-ui',
                                   fromdate=datetime(2020, 1, 1), todate=datetime(2020, 12, 31))

    questions = [Question(question) for question in raw_questions['items']]

    print(
        '{}/{}'.format(len([question for question in questions if question.is_answered]), len(questions)))
    data={'name': name, 'is_answered':len([question for question in questions if question.is_answered]) }
    if(len([question for question in questions if question.is_answered]) > 0 & len(questions) > 0):
        data['average'] = (len([question for question in questions if question.is_answered]) / len(questions))
    DataFrame([data]).to_csv('stackoverflow.csv', mode='a', header=False, index=False)
