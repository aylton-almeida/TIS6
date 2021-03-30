def getQ3(cursor=None):
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