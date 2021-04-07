from __future__ import annotations
from datetime import datetime


class Repo:

    cursor: str
    name_with_owner: str
    name: str
    url: str
    stargazer_count: str
    topic: str
    createdAt: str

    def __init__(self, data: dict) -> None:
        self.cursor = data.get('cursor')
        self.name_with_owner = data.get('nameWithOwner')
        self.name = data.get('name')
        self.url = data.get('url')
        self.stargazer_count = data.get('stargazerCount')
        self.topic = data.get('topic')
        self.createdAt = datetime.fromisoformat(
            data.get('createdAt').replace('Z', '+00:00'))

    @staticmethod
    def from_github(data: dict) -> Repo:
        node = data.get('node')

        return Repo({
            'cursor': data.get('cursor'),
            'nameWithOwner': node.get('nameWithOwner'),
            'name': node.get('name'),
            'url': node.get('url'),
            'stargazerCount': node.get('stargazerCount'),
            'topic': data.get('topic'),
            'createdAt': node.get('createdAt')
        })
