from jira import JIRA
import openpyxl, pprint
import pandas as pd
import json
import getpass
print('start')

username = input('Enter your user name: ')
password = getpass.getpass(prompt='Enter password: ')
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

link=[]

Issue = 2183

while Issue < 2193:
    summ = "NYCRSA-" + str(Issue)
    issue = jira.issue(summ)
    print(issue)
    summary = issue.fields.summary
    summary = summary.replace(" Max","")
    issue.update(summary=summary)
    Issue=Issue+1

print('Done')
