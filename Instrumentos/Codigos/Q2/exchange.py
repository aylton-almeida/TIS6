import time
from datetime import datetime
from time import sleep

from stackapi import StackAPI

from pandas import *
from src.models.Question import Question

csvName = "bottom10repos.csv"
data = read_csv(csvName)
names = data['name'].tolist()

for name in names:
    print(name)
    exchange = StackAPI('stackoverflow', key='6XxpO5wC8dfXJGRVwV8qWA((')
    exchange.page_size = 100
    exchange.max_pages = 10
    raw_questions = exchange.fetch('questions', tagged=name,
                                   fromdate=datetime(2020, 1, 1), todate=datetime(2020, 12, 31))

    questions = [Question(question) for question in raw_questions['items']]

    print(
        '{}/{}'.format(len([question for question in questions if question.is_answered]), len(questions)))
    data={'name': name, 'is_answered':len([question for question in questions if question.is_answered]), 'questions': len(questions) }
    if(data.get('is_answered') > 0 & data.get('questions') > 0):
        data['average'] = (data.get('is_answered') / data.get('questions'))
    DataFrame([data]).to_csv('bottom10stackoverflow.csv', mode='a', header=False, index=False)
    time.sleep(5)
