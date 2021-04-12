from __future__ import annotations
from datetime import datetime
from statistics import median

from pandas.core import series

from src.models.Question import Question


class Repo:

    cursor: str
    name_with_owner: str
    url: str
    stargazer_count: str
    issue_close_median: float
    answered_questions: float

    def __init__(self, data: dict) -> None:
        self.cursor = data.get('cursor')
        self.name_with_owner = data.get('nameWithOwner')
        self.url = data.get('url')
        self.stargazer_count = data.get('stargazerCount')
        self.issue_close_median = data.get('issueCloseMedian')
        self.answered_questions = data.get('answeredQuestions')

    def get_name(self):
        return self.name_with_owner.split('/')[1]

    def set_answered_questions(self, questions: list[Question]):
        if len(questions):
            self.answered_questions = len(
                [question for question in questions if question.is_answered]) / len(questions)
        else:
            self.answered_questions = 0

    @staticmethod
    def from_github(data: dict) -> Repo:
        node = data.get('node')

        issue_median = None
        if issues := node.get('issues').get('nodes'):
            issue_median = median([
                int((datetime.fromisoformat(issue['closedAt'].replace('Z', '+00:00'))
                     - datetime.fromisoformat(issue['createdAt'].replace('Z', '+00:00'))).days) * 24
                for issue in issues
            ])

        return Repo({
            'cursor': data.get('cursor'),
            'nameWithOwner': node.get('nameWithOwner'),
            'url': node.get('url'),
            'stargazerCount': node.get('stargazerCount'),
            'issueCloseMedian': issue_median
        })

    @staticmethod
    def from_dataframe(data: series) -> Repo:
        return Repo({
            'cursor': data['cursor'],
            'nameWithOwner': data['name_with_owner'],
            'url': data['url'],
            'stargazerCount': data['stargazer_count'],
        })
