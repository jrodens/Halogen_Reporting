from jira import JIRA
import pandas as pd
import json
import getpass
print('start')

username = input('Enter your user name: ')
password = getpass.getpass(prompt='Enter your password: ')
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

df = pd.read_excel('o:/storylink.xlsx')
for index, row in df.iterrows():
    summ= df.iloc[index,0]
    block = df.iloc[index,1]
    print('Issue {} is related to {}'.format(summ,block))
    new_link = jira.create_issue_link('relates to', summ, block)
    print(new_link)
