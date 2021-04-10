from src.models.GithubException import GithubException
import requests
import json

from requests.models import Response


class Graphql:

    url: str
    repos_per_request: int
    cursor = None
    createdAt: str

    def __init__(self, url: str, repos_per_request: int) -> None:
        self.url = url
        self.repos_per_request = repos_per_request

    def get_repo_query(self, stars: str = '>100'):
        return """
               query example {
                 search(type: REPOSITORY, first: %(repos)i, query: "stars:%(stars)s language:%(language)s created:2020-01-01..2020-12-31", after: %(after)s) {
                   edges {
                     cursor  
                     node {
                       ... on Repository {
                         nameWithOwner
                         url
                         createdAt
                       }
                     }
                   }
                 }
               }
               """ % {
            'repos': self.repos_per_request,
            'stars': stars,
            'after': ('"{}"'.format(self.cursor) if self.cursor else 'null'),
            'language': 'javascript'
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

        edges = [{**edge}
                 for edge in edges]



        return edges
