from datetime import datetime
from stackapi import StackAPI

from src.models.Question import Question

exchange = StackAPI('stackoverflow')
exchange.page_size = 100
exchange.max_pages = 10


def get_questions_by_tag(tag: str):
    raw_questions = exchange.fetch('questions', tagged=tag,
                                   fromdate=datetime(2020, 1, 1), todate=datetime(2020, 12, 31))

    return [Question(question) for question in raw_questions['items']]
