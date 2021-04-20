def getIssueQuery(name: str, owner: str, cursor: str):
        return """
               query getIssues {
                 repository(name: "%(name)s", owner: "%(owner)s") {
                   issues(states: CLOSED, first: 100, %(cursor)s) {
                     totalCount
                   edges {
                     cursor
                     node {
                       closed
                       participants {
                         totalCount
                       }
                     }
                   }
                   pageInfo{
                       hasNextPage
                       endCursor
                   }
                   }
                   }
                 }
               """ % {
            'name': name,
            'owner': owner,
            'cursor': """ after:"%s" """ % cursor if (cursor != None) else 'after: null'
        }



def getRepoInfoQuery(name: str, owner: str):
  return """
  query repoInfo {
  repository(name: "%(name)s", owner: "%(owner)s") {
    issues {
      totalCount
    }
    stargazerCount
  }
}
  """ % {
            'name': name,
            'owner': owner,
        }
