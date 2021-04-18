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

    def get_disk_usage_query(self, owner: str, name: str):
        return """
               query {
                 repository(owner: "%(owner)s", name: "%(name)s") {
                   diskUsage
                 }
               }
               """ % {
            'owner': owner,
            'name': name,
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

    def get_disk_usage_data(self, query: str, token: str):

        json_data = self._fetch_data(query, token)

        disk_usage = json_data['data']['repository']['diskUsage']

        return disk_usage
