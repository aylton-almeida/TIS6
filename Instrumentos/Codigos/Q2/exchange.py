from stackapi import StackAPI

exchange = StackAPI('stackoverflow')
comments = exchange.fetch('questions')
print(comments)
