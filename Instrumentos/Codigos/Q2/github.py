import os
import time

import requests
from dotenv import load_dotenv
from numpy import average
from requests.api import request

from pandas import *
from pandas.io import json
from src.query import getIssueQuery, getRepoInfoQuery

# Load env file
load_dotenv()


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

def getRepoRequest(name, owner):
  head = getHeader()
  try:
    return requests.post(url, json={'query': getRepoInfoQuery(name, owner)}, headers= head)
  except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

def getRepoInfo(repoNameWithOwner):
  nameWithOwner = repoNameWithOwner.split('/')
  try:
    json_data = json.loads(getRepoRequest(nameWithOwner[1], nameWithOwner[0]).text)
    if json_data is not None:
      repoData = {
        'name_with_owner': nameWithOwner,
        'stargazer_count': json_data['data']['repository']['stargazerCount'],
        'total_issues': json_data['data']['repository']['issues']['totalCount'],
        'closed_issues_with_participants' : getClosedIssuesWithParticipants(repoNameWithOwner, int(json_data['data']['repository']['issues']['totalCount'])),
      }
      if(int(repoData['closed_issues_with_participants']) > 0 & int(repoData['total_issues']) > 0):
        repoData['average_issues'] = round(int(repoData['closed_issues_with_participants'])/int(repoData['total_issues']),3)
      DataFrame([repoData]).to_csv('finalMiddle10repos.csv', mode='a', header=False, index=False)
  except:
    raise Exception('Erro ao obter repositório')
    



def getClosedIssuesWithParticipants(repoNameWithOwner, totalIssues):
    if(totalIssues == 0 ): return 0
    nameWithOwner = repoNameWithOwner.split('/')
    hasNextPage = True
    lastCursor = None
    closedIssues = 0
    print(nameWithOwner)

    while (hasNextPage):
        try:
            json_data = json.loads(getIssueRequest(nameWithOwner[1], nameWithOwner[0],lastCursor).text)
            if json_data is not None:
                issues = json_data['data']['repository']['issues']['edges']
                hasNextPage = json_data['data']['repository']['issues']['pageInfo']['hasNextPage']
                lastCursor = json_data['data']['repository']['issues']['pageInfo']['endCursor']
                totalClosedIssues = json_data['data']['repository']['issues']['totalCount']

                if(totalClosedIssues == 0 ): return 0
                
                for issue in issues: 
                    issueData = {
                        'cursor':issue['cursor'],
                        'participants': issue['node']['participants']['totalCount']
                    }
                    if int(issueData['participants']) > 1 :
                      closedIssues += 1

                time.sleep(5)
        except:
            raise Exception('Erro ao obter dado da issue')
    return closedIssues  

def getRepoNames(csvName: str):
    data = read_csv(csvName)
    nameWithOwner = data['name_with_owner'].tolist()
    return nameWithOwner

def main():
    namesWithOwner = getRepoNames('middle10repos.csv')

    for name in namesWithOwner:
        getRepoInfo(name)


main()
