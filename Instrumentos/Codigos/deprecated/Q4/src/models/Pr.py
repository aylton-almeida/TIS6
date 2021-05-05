from __future__ import annotations

from pandas.core import series


class Pr:

    cursor: str
    id: str
    state: str
    body: str
    labels: list[str]

    def __init__(self, data: dict) -> None:
        self.cursor = data.get('cursor')
        self.id = data.get('id')
        self.state = data.get('state')
        self.body = data.get('body')
        self.labels = data.get('labels')

    @staticmethod
    def from_github(data: dict) -> Pr:
        node = data.get('node')

        return Pr({
            'cursor': data.get('cursor'),
            'id': node.get('id'),
            'state': node.get('state'),
            'body': node.get('body'),
            'labels': [item.get('name') for item in node.get('labels').get('nodes')]
        })

    @staticmethod
    def from_dataframe(data: series) -> Pr:
        return Pr({
            'cursor': data['cursor'],
            'id': data['id'],
            'state': data['state'],
        })
