from jira import JIRA
import openpyxl, pprint
import pandas as pd
import json
import getpass
print('start')

username = input('Enter your user name: ')
password = getpass.getpass(prompt='Enter password: ')
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

newissue=[]
class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1

link=[]
df = pd.read_excel('o:/newepic.xlsx')
for index, row in df.iterrows():
    summ= df.iloc[index,0]
    description = df.iloc[index,1]
    component = df.iloc[index, 2]
    print(summ)
    issue_list = {
    'project': {'key': 'IDWH'},
    'summary': summ,
    'customfield_10507':description,
    'issuetype': {'name': 'Epic'}
    }

    new_issue = jira.create_issue(fields=issue_list)
    print(new_issue)
    issue = jira.issue(new_issue)
    assigncomponent = [{'name':component}]
    issue.update(fields = {"components": assigncomponent})
    print(new_issue)

print('Done')
