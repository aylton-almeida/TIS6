from __future__ import annotations


class RepoWithCreateAt:

    cursor: str
    name_with_owner: str
    url: str
    createdAt: str

    def __init__(self, data: dict) -> None:
        self.cursor = data.get('cursor')
        self.name_with_owner = data.get('nameWithOwner')
        self.url = data.get('url')
        self.createdAt = data.get('createdAt')

    @staticmethod
    def from_github(data: dict) -> RepoWithCreateAt:
        node = data.get('node')

        return RepoWithCreateAt({
            'cursor': data.get('cursor'),
            'nameWithOwner': node.get('nameWithOwner'),
            'url': node.get('url'),
            'createdAt': node.get('createdAt')
        })
