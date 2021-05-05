def getQ3V2(name, owner, cursor = None):
  return """
      query {
        repository(name: "%(name)s", owner: "%(owner)s") {
          pullRequests(first: 50, states: MERGED, %(cursor)s) {
            pageInfo {
              hasNextPage
              endCursor
            }
            edges {
              cursor
              node {
                createdAt
                mergedAt
              }
            }
          }
        }
      } 
  """ % {
    'name': name, 
    'owner': owner,
    'cursor': """ after:"%s" """ % cursor if (cursor != None) else 'after: null'
  }

def getRepoInfo(name, owner):
  return """
      query {
        repository(name: "%(name)s", owner: "%(owner)s") {
          createdAt
          releases {
            totalCount
          }
        }
      } 
  """ % {
    'name': name, 
    'owner': owner,
  }

#deprecated
def getQ3V1(cursor=None):
  if cursor is None:
    return """
      query {
        search(query: "stars:>100 language:javascript topic:ui", type: REPOSITORY, first: 5) {
          edges {
            cursor
            node {
              ... on Repository {
                nameWithOwner
                url
                createdAt
                releases(first: 100, orderBy: {field: CREATED_AT, direction: DESC}) {
                  edges {
                    node {
                      publishedAt
                    }
                    cursor
                  }
                }
                pullRequests(last: 100, states: MERGED) {
                  edges {
                    node {
                      mergedAt
                      createdAt
                    }
                    cursor
                  }
                }
              }
            }
          }
        }
      } """
  else:
    return """
    query {
      search(query: "stars:>100 language:javascript topic:ui", type: REPOSITORY, first: 5, after: "%s") {
        edges {
          cursor
          node {
            ... on Repository {
              nameWithOwner
              url
              createdAt
              releases(first: 100, orderBy: {field: CREATED_AT, direction: DESC}) {
                edges {
                  node {
                    publishedAt
                  }
                  cursor
                }
              }
              pullRequests(last: 100, states: MERGED) {
                edges {
                  node {
                    mergedAt
                    createdAt
                  }
                  cursor
                }
              }
            }
          }
        }
      }
    }  """ % cursor