#import libraries
import pandas as pd
from jira import JIRA
import getpass
import datetime
import matplotlib.pyplot as plt
from openpyxl.styles import Alignment
import requests
from pandas.io.json import json_normalize
import json
import pprint

#setting up lists for entries

now = datetime.datetime.now()

#prompt user for authorization and authorize user
username = input('Enter your user name: ')
password = getpass.getpass(prompt='Enter your password: ')
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

#print(jira.project_components('HP'))

class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1

df = pd.read_excel('o:/Hadron Upload.xlsx')
for index, row in df.iterrows():
    summ= df.iloc[index,0]
    component = S(df.iloc[index,1])
    tdd = S(df.iloc[index,2])
    epic_link = df.iloc[index,3]

    issue_list = {
    'project': {'key': 'HP'},
    'summary': summ,
    'components':[{'id':component}],
    'customfield_21501':tdd,
    'issuetype': {'name': 'Story'}
    }
    new_issue=jira.create_issue(fields=issue_list)
    print(new_issue)
    epic_list = []
    epic_list.append(S(new_issue))
    jira.add_issues_to_epic(epic_link, epic_list)
print('Done!')
