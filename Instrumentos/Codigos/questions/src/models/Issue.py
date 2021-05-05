from __future__ import annotations
from datetime import datetime


class Issue:

    cursor: str
    closed: bool
    participantTotalCount: str

    def __init__(self, data: dict) -> None:
        self.cursor = data.get('cursor')
        self.closed = data['closed']
        self.participantTotalCount = data.get('totalCount')

    @staticmethod
    def from_github(data: dict) -> Issue:
        node = data.get('node')

        return Issue({
            'cursor': data.get('cursor'),
            'closed': node['closed'],
            'participantTotalCount': node['participants']['totalCount'],
        })
