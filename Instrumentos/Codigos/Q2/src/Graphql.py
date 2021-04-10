from src.models.GithubException import GithubException
import requests
import json

from requests.models import Response

# TODO: change issues and topic


def get_query(repos_per_request: int, cursor: str = None, stars: str = '>100'):
    return """
    query example {
      search(type: REPOSITORY, first: %(repos)i, query: "stars:%(stars)s topic:react-components", after: %(after)s) {
        edges {
          cursor  
          node {
            ... on Repository {
              nameWithOwner
              url
              stargazerCount
              issues(first: 1, states: CLOSED) {
                nodes {
                  ...on Issue {
                    createdAt
                    closedAt
                  }
                }
              }
            }
          }
        }
      }
    }
    """ % {'repos': repos_per_request, 'stars': stars, 'after': ('"{}"'.format(cursor) if cursor else 'null')}


def get_repos_data(url: str, query: str, token: str):
    response: Response = requests.post(url, json={'query': query}, headers={
        'Authorization': token
    })

    if response.status_code != 200 or 'errors' in response.text:
        print(response.text)
        raise GithubException(
            'There was an error while trying to make the request'
        )

    json_data: dict = json.loads(response.text)

    return json_data['data']['search']['edges']
