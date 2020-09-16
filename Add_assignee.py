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
df = pd.read_excel('o:/Addassignee.xlsx')
for index, row in df.iterrows():
    summ= df.iloc[index,0]
    assignee1 = df.iloc[index,1]
    #acceptor1=df.iloc[index,2]
    #desc = df.iloc[index,4]
    #linkto = df.iloc[index,1]
    print(summ)
    issue = jira.issue(summ)
    
    issue.update(assignee={'name': assignee1})
    #issue.update(customfield_11622={'displayName':acceptor1})
print('Done')
