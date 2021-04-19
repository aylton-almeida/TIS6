from __future__ import annotations

from pandas.core import series


class Issue:

    cursor: str
    id: str
    state: str

    def __init__(self, data: dict) -> None:
        self.cursor = data.get('cursor')
        self.id = data.get('id')
        self.state = data.get('state')

    @staticmethod
    def from_github(data: dict) -> Issue:
        node = data.get('node')

        return Issue({
            'cursor': data.get('cursor'),
            'id': node.get('id'),
            'state': node.get('state'),
        })

    @staticmethod
    def from_dataframe(data: series) -> Issue:
        return Issue({
            'cursor': data['cursor'],
            'id': data['id'],
            'state': data['state'],
        })
