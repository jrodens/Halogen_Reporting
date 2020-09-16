#Determine what status each of the linked attributes for a view is in
from jira import JIRA
import json
import requests
import getpass
import pandas as pd
from collections import deque
#Get User credentials for JIRA authorization
username = input('Enter your user name: ')
password = getpass.getpass(prompt="Enter Password")
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

#Utilize Jira search function to identify any views on the Analyst board that links to the Halogen View epic
datafromjson = jira.search_issues('project = NYC-IO-Surge-Testing', maxResults=1000)

class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1

def window(seq, n=3):
    it = iter(seq)
    win = deque((next(it, None) for _ in xrange(n-1)), maxlen=n)
    for e in it:
        win.append(e)
        yield tuple(win)

def sorted_grams(doc, n=3):
    counts = {}
    for ngram in window(doc, n):
        counts[ngram] = counts.get(ngram, 0) + 1

    return sorted(((v,k) for k,v in counts.items()), reverse=True)

summary = ""
description = ""
for issue in datafromjson:
    summary = summary + " " + S(issue.fields.summary)
    description = description + " " + S(issue.fields.description)
example_doc = 'it is a small world after all it is a small world after all'
for s in sorted_grams(summary.split(), 3):
    print ("summary:")
    print (s)
for d in sorted_grams(description.split(), 3):
    print("description")
    print (d)
