from __future__ import annotations

from pandas.core import series


class Pr:

    cursor: str
    id: str
    state: str

    def __init__(self, data: dict) -> None:
        self.cursor = data.get('cursor')
        self.id = data.get('id')
        self.state = data.get('state')

    @staticmethod
    def from_github(data: dict) -> Pr:
        node = data.get('node')

        return Pr({
            'cursor': data.get('cursor'),
            'id': node.get('id'),
            'state': node.get('state'),
        })

    @staticmethod
    def from_dataframe(data: series) -> Pr:
        return Pr({
            'cursor': data['cursor'],
            'id': data['id'],
            'state': data['state'],
        })
