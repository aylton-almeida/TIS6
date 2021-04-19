def getIssueQuery(name: str, owner: str, cursor: str):
        return """
               query getIssues {
                 repository(name: "%(name)s", owner: "%(owner)s") {
                   issues(first: 100, %(cursor)s) {
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