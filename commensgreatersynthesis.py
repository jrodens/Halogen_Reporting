from jira import JIRA
import json
import requests
import getpass
import pandas as pd
import datetime
import numpy as np


username = input('Enter your user name: ')
password = getpass.getpass(prompt="Enter Password")
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

priority = jira.search_issues('filter = 43915 and status not in (Accepted, rejected, qa) AND Synthesis is not EMPTY AND issueFunction in hasComments()')

class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1
string = 'key in ('
for issue in priority:
    currentID = issue.key
    status = S(issue.fields.status)
    issuefromjson = jira.issue(currentID, expand='changelog')
    results = issuefromjson.fields.comment.maxResults -1
    c = issuefromjson.fields.comment.comments[results]
    lastcomment = c.created
    changelog = issuefromjson.changelog
    for history in changelog.histories:
        for item in history.items:
            if (item.field == "Synthesis"):
                date2 = history.created
    if lastcomment > date2:
        string = string + currentID + ','
string = string[:-1]
string=string + ')'
print(string)
jira.update_filter(48014, jql=string)
print('done')
