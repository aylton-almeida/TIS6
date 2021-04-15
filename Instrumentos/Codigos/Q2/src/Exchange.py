from datetime import datetime
import os
from stackapi import StackAPI
from TimeCountdown import sleep

from src.models.Question import Question

from dotenv import load_dotenv

load_dotenv()

exchange = StackAPI('stackoverflow', key=os.getenv('EXCHANGE_SECRET'))
exchange.page_size = 100
exchange.max_pages = 10


def get_questions_by_tag(filter: str):
    raw_questions = exchange.fetch('questions', filter=filter,
                                   fromdate=datetime(2020, 1, 1), todate=datetime(2020, 12, 31))

    quota_remaining = int(raw_questions['quota_remaining'])

    if quota_remaining < 100:
        print('Waiting for quota to be back...')
        sleep(600)

    return [Question(question) for question in raw_questions['items']]
