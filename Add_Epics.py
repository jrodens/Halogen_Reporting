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
df = pd.read_excel('o:/component.xlsx')
for index, row in df.iterrows():
    summ= df.iloc[index,0]
    #quartile=df.iloc[index,1]
    #link = df.iloc[index,2]
   # quartile = S(quartile)

    #synthesis=df.iloc[index,2]
    description = df.iloc[index,1]
    #epic=df.iloc[index,5]
    #acceptance = df.iloc[index,6]
    #desc = df.iloc[index,4]
    #linkto = df.iloc[index,1]
    component = df.iloc[index, 2]
    print(summ)
    #print(desc)
    #print(linkto)
    issue_list = {
    'project': {'key': 'IDWH'},
    'summary': summ,
    'customfield_10507':description,
    'issuetype': {'name': 'Epic'}
    }

    new_issue = jira.create_issue(fields=issue_list)
    print(new_issue)
    jira.issue(new_issue)
    existingComponents=[]
    for component in new_issue.fields.components:
        existingComponents.append({component : component.name})
    new_issue.update(fields={"components": existingComponents})
    print(new_issue)
"""
    if 'Q1' in quartile:
        new_issue.fields.labels.append(u'Q1')
    elif 'Q2' in quartile:
        new_issue.fields.labels.append(u'Q2')
    elif 'Q3' in quartile:
        new_issue.fields.labels.append(u'Q3')
    elif 'Q4' in quartile:
        new_issue.fields.labels.append(u'Q4')
    new_issue.update(fields={"labels": new_issue.fields.labels})
    new_link = jira.create_issue_link('relates to', new_issue, link)
    print(new_link)
    """
    #existingComponents=[]
    #existingComponents.append({"name": component})
    # link.append(new_issue)
    # new_link = jira.create_issue_link('relates to', new_issue, linkto)
    # print(new_link)
    #new_issue.update(fields={'components' : existingComponents})
#df.insert(6, "Issue #", new_issue)
#df.to_excel('o:/NYCRSATasks.xlsx')
print('Done')
