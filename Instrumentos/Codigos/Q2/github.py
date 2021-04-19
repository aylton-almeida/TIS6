import os
import time
import requests
from pandas.io import json
# from src import CliArgs
from src.models.AuthToken import AuthToken
from src.Graphql import Graphql
from dotenv import load_dotenv
from src.models.Issue import Issue
from src.models.GithubException import GithubException
from src import CsvUtils
from pandas import *
from src.query import getIssueQuery




# Load env file
load_dotenv()

# flush progress bar
# progressbar.streams.flush()

headerIndex = 0

def getHeader():
  global headerIndex
  if headerIndex == 0:
    headerIndex = 1
    return {'Authorization':  'Bearer ' + os.getenv('AUTH_TOKEN1')}
  else:
    headerIndex = 0
    return {'Authorization':  'Bearer ' + os.getenv('AUTH_TOKEN2')}

url='https://api.github.com/graphql'

def getIssueRequest(name, owner, cursor = None):
  head = getHeader()
  try:
    print('Current header: %s' % head)
    return requests.post(url, json={'query': getIssueQuery(name, owner, cursor)}, headers=head)
  except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

def getIssues(repoNameWithOwner):
    nameWithOwner = repoNameWithOwner.split('/')
    hasNextPage = True
    lastCursor = None

    while (hasNextPage):
        try:
            json_data = json.loads(getIssueRequest(nameWithOwner[1], nameWithOwner[0],lastCursor).text)
            if json_data is not None:
                issues = json_data['data']['repository']['issues']['edges']
                hasNextPage = json_data['data']['repository']['issues']['pageInfo']['hasNextPage']
                lastCursor = json_data['data']['repository']['issues']['pageInfo']['endCursor']
                print(len(issues))
                
                for issue in issues: 
                    issueData = {
                        'cursor':issue['cursor'],
                        'closed': issue['node']['closed'],
                        'participants': issue['node']['participants']['totalCount']
                    }
                    if issueData['participants'] > 2 :
                        DataFrame([issueData]).to_csv('issues.csv', mode='a', header=False, index=False)

                time.sleep(10)
        except:
            raise Exception('Erro ao obter dado da issue')

def getRepoNames(csvName: str):
    data = read_csv(csvName)
    nameWithOwner = data['name_with_owner'].tolist()
    return nameWithOwner

def main():
    # getIssues('mui-org/material-ui')
    getRepoNames('final_ui_repos.csv')
    print(len(getRepoNames('final_ui_repos.csv')))

main()
