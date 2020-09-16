from jira import JIRA
import pandas as pd
import getpass

username = input('Enter your user name: ')
password = getpass.getpass(prompt="Enter Password")
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

ifu = pd.read_excel('O:/pri1.xlsx', sheet_name='Sheet1')

class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1

for index,row in ifu.iterrows():
    summ = ifu.iloc[index,0]
    label=ifu.iloc[index,9]
    issue =jira.issue(summ)
    print(summ)
    if 'priority1' in issue.fields.labels:
        pass
    else:
        print('launch')
        if 'priority1' in label:
            issue.fields.labels.append(u'priority1')
        elif 'priority2' in label:
            issue.fields.labels.append(u'priority2')
        elif 'priority3' in label:
            issue.fields.labels.append(u'priority3')
        issue.update(fields={"labels": issue.fields.labels})
print('done')
