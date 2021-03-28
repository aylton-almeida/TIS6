from stackapi import StackAPI

exchange = StackAPI('stackoverflow')
comments = exchange.fetch('comments')
print(comments)
