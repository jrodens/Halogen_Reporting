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
df = pd.read_excel('o:/sprint25.xlsx')
for index, row in df.iterrows():
    summ= df.iloc[index,0]

    #desc = df.iloc[index,4]
    #linkto = df.iloc[index,1]
    print(summ)
    issue = jira.issue(summ)
    issue.fields.labels.append(u'priority2')
    issue.update(fields={"labels": issue.fields.labels})

print('Done')
