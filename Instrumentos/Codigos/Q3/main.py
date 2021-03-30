import requests
import os
import json
import pandas
from datetime import datetime
import queries
from queries import getQ3

from dotenv import load_dotenv
load_dotenv()

head={'Authorization':  'Bearer ' + os.getenv('GITHUB_AUTH_TOKEN')}
url='https://api.github.com/graphql'

def getYearFromDate(date):
  return datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').year

def getTimeInDays(createdAt, mergedAt):
  createdAt = datetime.strptime(createdAt, '%Y-%m-%dT%H:%M:%SZ')
  mergedAt = datetime.strptime(mergedAt, '%Y-%m-%dT%H:%M:%SZ')
  return round(((mergedAt - createdAt).days), 2)

repos = []

def doApiRequest(cursor = None):
  try:
    return requests.post(url, json={'query': getQ3(cursor)}, headers=head)
  except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

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
  formattedPullRequests = list(map(lambda item: {
    "createdAt": item.get('node').get('createdAt'),
    "mergedAt": item.get('node').get('mergedAt'),
    "cursor": item.get('cursor'),
    "timeForMergePRinDays": getTimeInDays(item.get('node').get('createdAt'), item.get('node').get('mergedAt'))
  }, pullRequests))
  return round(sum(pr['timeForMergePRinDays'] for pr in formattedPullRequests) / len(formattedPullRequests))

def main():
  getData()
  df = pandas.DataFrame(list(map(lambda item: {
    "nameWithOwner": item.get('node').get('nameWithOwner'),
    "url": item.get('node').get('url'),
    "createdAt": item.get('node').get("createdAt"),
    "releasesIn2020": getReleasesNumberFromYear(item.get('node').get('releases').get('edges'), 2020) if item.get('node').get('releases').get('edges') else 0,
    "averageTimeForMergePRInDays": getAverageTimeForMergePR(item.get('node').get('pullRequests').get('edges')) if item.get('node').get('pullRequests').get('edges') else 0,
  }, repos)))
  df.to_csv('results.csv')
  print(df)

main()