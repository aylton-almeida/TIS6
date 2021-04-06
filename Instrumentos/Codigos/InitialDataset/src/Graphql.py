from src.models.GithubException import GithubException
import requests
import json

from requests.models import Response


class Graphql:

    url: str
    repos_per_request: int
    topics: list[str]
    current_topic = 0
    cursor = None

    def __init__(self, url: str, repos_per_request: int, topics: list[str]) -> None:
        self.url = url
        self.repos_per_request = repos_per_request
        self.topics = topics

    def get_current_topic(self):
        return self.topics[self.current_topic]

    def get_query(self, stars: str = '>100'):
        return """
               query example {
                 search(type: REPOSITORY, first: %(repos)i, query: "stars:%(stars)s topic:%(topic)s", after: %(after)s) {
                   edges {
                     cursor  
                     node {
                       ... on Repository {
                         nameWithOwner
                         name
                         url
                         stargazerCount
                       }
                     }
                   }
                 }
               }
               """ % {
            'repos': self.repos_per_request,
            'stars': stars,
            'after': ('"{}"'.format(self.cursor) if self.cursor else 'null'),
            'topic': self.get_current_topic()
        }

    def get_repos_data(self, query: str, token: str):
        response: Response = requests.post(self.url, json={'query': query}, headers={
            'Authorization': token
        })

        if response.status_code != 200 or 'errors' in response.text:
            print(response.text)
            raise GithubException(
                'There was an error while trying to make the request'
            )

        json_data: dict = json.loads(response.text)

        edges: list = json_data['data']['search']['edges']

        edges = [{**edge, 'topic': self.get_current_topic()}
                 for edge in edges]

        if len(edges) < self.repos_per_request:
            self.cursor = None

            if self.current_topic < (len(self.topics) - 1):
                self.current_topic += 1

        else:
            self.cursor = edges[-1]['cursor']

        return edges
