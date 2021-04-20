import requests
import os
import json
import pandas
import sys
import time
from datetime import datetime
import queries
from queries import getQ3V2, getRepoInfo
import statistics

from dotenv import load_dotenv
load_dotenv()

headerIndex = 0

url='https://api.github.com/graphql'

def getHeader():
  global headerIndex
  if headerIndex == 0:
    headerIndex = 1
    return {'Authorization':  'Bearer ' + os.getenv('GITHUB_AUTH_TOKEN')}
  else:
    headerIndex = 0
    return {'Authorization':  'Bearer ' + os.getenv('GITHUB_AUTH_TOKEN_2')}

def getYearFromDate(date):
  return datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').year

def getTimeInDays(createdAt, mergedAt):
  createdAt = datetime.strptime(createdAt, '%Y-%m-%dT%H:%M:%SZ')
  mergedAt = datetime.strptime(mergedAt, '%Y-%m-%dT%H:%M:%SZ')
  return round(((mergedAt - createdAt).days), 2)

def getTimeInYears(date1, date2):
  date1 = datetime.strptime(createdAt, '%Y-%m-%dT%H:%M:%SZ')
  date2 = datetime.strptime(mergedAt, '%Y-%m-%dT%H:%M:%SZ')
  return round(((date2 - date1).days / 365), 2)

def getRepoAgeInYears(createdAt):
  createdAt = datetime.strptime(createdAt, '%Y-%m-%dT%H:%M:%SZ')
  today = datetime.now() 
  return round(((today - createdAt).days / 365), 2)

repos = []

#deprecated
def getData():
  cont = 0  
  while (cont < 5):
    try:
      cursor = repos[-1]['cursor'] if len(repos) > 0 else None
      json_data = json.loads(doApiRequest(cursor).text)

      repos.extend(json_data['data']['search']['edges'])

      cont += 100
    except:
      raise Exception("erro") 

#deprecated
def getReleasesNumberFromYear(releases, year):
  totalReleasesCount = 0
  formattedReleases = list(map(lambda item: {
    "publishedAt": item.get('node').get('publishedAt'),
    "cursor": item.get('cursor'),
    "isFrom2020": getYearFromDate(item.get('node').get('publishedAt')) == year
  }, releases))
  for release in formattedReleases:
    if (release['isFrom2020'] == True):
      totalReleasesCount += 1
  return totalReleasesCount

def getAverageTimeForMergePR(pullRequests):
  timeForMerge = []
  for index, row in [*pullRequests.iterrows()]:
    timeForMerge.append(getTimeInDays(row['createdAt'], row['mergedAt']))
  if len(timeForMerge) == 0:
    return 0;
  else:
    return round(sum(timeForMerge) / len(timeForMerge))

def doApiRequestGetPRs(name, owner, cursor = None):
  head = getHeader()
  try:
    print('Current header: %s' % head)
    return requests.post(url, json={'query': getQ3V2(name, owner, cursor)}, headers=head)
  except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

def doApiRequestGetRepoInfo(name, owner):
  head = getHeader()
  try:
    print('Current header: %s' % head)
    return requests.post(url, json={'query': getRepoInfo(name, owner)}, headers=head)
  except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

def formatDataInfo(fileName, nameWithOwner):
  formattedNameWithOwner = nameWithOwner.split("/");
  try:
    json_data = json.loads(doApiRequestGetRepoInfo(formattedNameWithOwner[1], formattedNameWithOwner[0]).text)
    df = pandas.read_csv('./%s' % fileName)
    df.to_csv('formatted_file.csv', header=['cursor', 'nameWithOwner', 'createdAt', 'mergedAt'])
    df2 = pandas.read_csv('formatted_file.csv')
    repoData = {
      'nameWithOwner': nameWithOwner,
      'createdAt': json_data['data']['repository']['createdAt'],
      'releasesByRepoAge': round(json_data['data']['repository']['releases']['totalCount'] / getRepoAgeInYears(json_data['data']['repository']['createdAt']), 2),
      'averageTimeForMergePR': getAverageTimeForMergePR(df2)
    }
    pandas.DataFrame([repoData]).to_csv('final_results.csv', mode='a', header=False, index=False)
    os.remove('%s_prs.csv' % formattedNameWithOwner[1])
    os.remove('formatted_file.csv')
  except Exception as e:
    raise Exception("Erro ao obter dados do repositório: %s" % e) 

def analyzeUIRepos():
  df = pandas.read_csv('../InitialDataset/final_ui_repos.csv')
  lastCursor = int(sys.argv[1])
  for index, row in [*df.iterrows()][lastCursor:]:
    nameWithOwner = row['name_with_owner'].split("/");
    hasNextPage = True
    lastCursor = None
    repoIsNotEmpty = False
    while (hasNextPage):
      try:
        json_data = json.loads(doApiRequestGetPRs(nameWithOwner[1], nameWithOwner[0], lastCursor).text)
        prs = json_data['data']['repository']['pullRequests']['edges']
        hasNextPage = json_data['data']['repository']['pullRequests']['pageInfo']['hasNextPage']
        lastCursor = json_data['data']['repository']['pullRequests']['pageInfo']['endCursor']
        if len(prs) > 0:
          for pr in prs:
            prData = {
              'cursor': pr['cursor'],
              'nameWithOwner': row['name_with_owner'],
              'createdAt': pr['node']['createdAt'],
              'mergedAt': pr['node']['mergedAt'],
            }
            pandas.DataFrame([prData]).to_csv('%s_prs.csv' % nameWithOwner[1], mode='a', header=False, index=False)
            time.sleep(2)
          else:
            repoIsNotEmpty = True
      except:
        raise Exception("Erro ao obter dados do repositório!") 
    if repoIsNotEmpty:
      formatDataInfo('%s_prs.csv' % nameWithOwner[1], row['name_with_owner'])
      
def main():
  analyzeUIRepos()

main()