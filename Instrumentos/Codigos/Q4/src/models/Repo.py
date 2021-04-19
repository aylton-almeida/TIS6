from __future__ import annotations
from datetime import datetime
import time
from src.models.AuthToken import AuthToken
from src.models.Issue import Issue
from src.utils.BundlePhobia import measure_pkg
from src.utils.Node import search_package

from pandas.core import series

from src.utils.Graphql import Graphql
from src.utils.TimeCountdown import sleep


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
    issue_ratio: float

    def __init__(self, data: dict) -> None:
        self.cursor = data.get('cursor')
        self.name_with_owner = data.get('nameWithOwner')
        self.url = data.get('url')
        self.stargazer_count = data.get('stargazerCount')
        self.topic = data.get('topic')
        self.create_at = data.get('createdAt')

    def get_owner_and_name(self) -> tuple[str, str]:
        return self.name_with_owner.split('/')

    def set_bug_issues(self, graphql: Graphql, token: AuthToken):
        owner, name = self.get_owner_and_name()

        # get bug or error labels
        labels_query = graphql.get_labels_query(owner, name)
        labels = graphql.get_labels_data(labels_query, token.get_token())

        # get issues
        issues: list[Issue] = []
        has_next_page = True
        while has_next_page:
            try:
                # get query
                issue_query = graphql.get_issues_query(owner, name, labels)

                # fetch issues
                new_issues, has_next_page = graphql.get_issues_data(
                    issue_query, token.get_token())

                # add issues to list
                issues += [Issue.from_github(issue) for issue in new_issues]

                # sleep a bit
                time.sleep(1)
            except Exception as err:
                print(err)
                sleep(600)
                token.next_token()

        # calculate issue ratio
        if issues:
            self.issue_ratio = len(
                [issue for issue in issues if issue.state == 'OPEN']) / len(issues)
        else:
            self.issue_ratio = 0

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
