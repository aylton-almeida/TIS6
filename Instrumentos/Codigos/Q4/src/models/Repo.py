from __future__ import annotations
from datetime import datetime
from src.utils.BundlePhobia import measure_pkg
from src.utils.Node import search_package

from pandas.core import series

from src.utils.Graphql import Graphql


class Repo:

    cursor: str
    name_with_owner: str
    url: str
    stargazer_count: str
    topic: str
    created_at: datetime
    dependencies: int
    weight: float
    gzipped: float

    def __init__(self, data: dict) -> None:
        self.cursor = data.get('cursor')
        self.name_with_owner = data.get('nameWithOwner')
        self.url = data.get('url')
        self.stargazer_count = data.get('stargazerCount')
        self.topic = data.get('topic')
        self.create_at = data.get('createdAt')

    def get_owner_and_name(self) -> tuple[str, str]:
        return self.name_with_owner.split('/')

    def set_weight(self, graphql: Graphql, token: str):
        # get npm package name
        owner, name = self.get_owner_and_name()
        pkg_name = search_package(name)

        if not pkg_name:
            pkg_name = name.lower()

        dependencies, weight, gzipped = measure_pkg(pkg_name)

        if not dependencies and not weight and not gzipped:
            query = graphql.get_disk_usage_query(owner, name)
            usage = graphql.get_disk_usage_data(query, token)
            weight = usage
            dependencies = -1
            gzipped = -1

        self.dependencies = int(dependencies)
        self.weight = float(weight)
        self.gzipped = float(gzipped)

    @staticmethod
    def from_dataframe(data: series) -> Repo:
        return Repo({
            'cursor': data['cursor'],
            'nameWithOwner': data['name_with_owner'],
            'url': data['url'],
            'stargazerCount': data['stargazer_count'],
            'topic': data['topic'],
            'createdAt': datetime.fromisoformat(data['createdAt'])
        })
