from jira import JIRA
import pandas as pd
import getpass

username = input('Enter your user name: ')
password = getpass.getpass(prompt='Enter your password: ')
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})
    
df=pd.read_excel('O:/Pri1.xlsx', sheet_name='Sheet1') 
for index, row in df.iterrows():   
    summ= df.iloc[index,0]
    issue=jira.issue(summ)
    issue.fields.labels.append(u'Cash_Component')    
    issue.update(fields={"labels": issue.fields.labels})
    print(summ)
print('done')

