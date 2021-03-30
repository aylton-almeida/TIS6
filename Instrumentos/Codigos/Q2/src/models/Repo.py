from __future__ import annotations
from datetime import datetime
from statistics import median


class Repo:

    cursor: str
    name_with_owner: str
    url: str
    stargazer_count: str
    issue_close_median: float

    def __init__(self, data: dict) -> None:
        self.cursor = data.get('cursor')
        self.name_with_owner = data.get('nameWithOwner')
        self.url = data.get('url')
        self.stargazer_count = data.get('stargazerCount')
        self.issue_close_median = data.get('issueCloseMedian')

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
