from stackapi import StackAPI
from src.models.Question import Question
from datetime import datetime

exchange = StackAPI('stackoverflow')
exchange.page_size = 100
exchange.max_pages = 10
raw_questions = exchange.fetch('questions', tagged='material-ui',
                               fromdate=datetime(2020, 1, 1), todate=datetime(2020, 12, 31))

questions = [Question(question) for question in raw_questions['items']]

print(
    '{}/{}'.format(len([question for question in questions if question.is_answered]), len(questions)))
