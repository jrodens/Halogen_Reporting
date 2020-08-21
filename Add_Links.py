from jira import JIRA
import openpyxl, pprint
import pandas as pd
import json
import getpass
print('start')

username = input('Enter your user name: ')
password = getpass.getpass(prompt='Enter your password: ')
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

df = pd.read_excel('o:/LinkonAPI.xlsx')

for index, row in df.iterrows():
    summ= df.iloc[index,0]
    block = "NYCIO-3315"
    print('Issue {} is related to {}'.format(summ,block))
    #createoutput=json.dumps(strjson)
    #print(createoutput)

    #new_issue = jira.create_issue(fields=issue_list)
    #print(new_issue)
    #new_link = jira.create_issue_link('relates to', new_issue, block)
    new_link = jira.create_issue_link('relates to', summ, block)
    print(new_link)
    #jira.create_issue(output)
