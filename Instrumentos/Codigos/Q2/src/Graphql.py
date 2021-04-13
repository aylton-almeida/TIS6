from src.models.GithubException import GithubException
import requests
import json

from requests.models import Response


class Graphql:

    url: str
    items_per_request: int
    cursor = None

    def __init__(self, url: str, items_per_request: int) -> None:
        self.url = url
        self.items_per_request = items_per_request

    def get_issues_query(self, owner: str, name: str):
        return """
               query {
                 repository(owner: "%(owner)s", name: "%(name)s") {
                   issues(first: %(issues)i, states: [CLOSED], after: %(after)s) {
                     pageInfo {
                       hasNextPage
                     }
                     edges {
                       cursor
                       node {
                         ... on Issue {
                           createdAt
                           closedAt
                         }
                       }
                     }
                   }
                 }
               }
               """ % {
            'owner': owner,
            'name': name,
            'issues': self.items_per_request,
            'after': ('"{}"'.format(self.cursor) if self.cursor else 'null')
        }

    def _fetch_data(self, query: str, token: str) -> dict:
        response: Response = requests.post(self.url, json={'query': query}, headers={
            'Authorization': token
        })

        if response.status_code != 200:
            raise GithubException(
                'There was an error while trying to make the request'
            )

        return json.loads(response.text)

    def get_issues_data(self, query: str, token: str):

        json_data = self._fetch_data(query, token)

        issues = json_data['data']['repository']['issues']

        has_next_page = issues['pageInfo']['hasNextPage']
        edges: list = issues['edges']

        if not has_next_page:
            self.cursor = None
        else:
            self.cursor = edges[-1]['cursor']

        return edges, has_next_page
