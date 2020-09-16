from jira import JIRA
import pandas as pd
import getpass

username = input('Enter your user name: ')
password = getpass.getpass(prompt='Enter your password: ')
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

newissue=[]
class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1
    
df=pd.read_excel('O:/PositionPriJira.xlsx', sheet_name='Sheet1') 
for index, row in df.iterrows():   
    story = df.iloc[index,0]
    summ= df.iloc[index,1]
    #desc = df.iloc[index,1]
    #labels=df.iloc[index,3]
    quartile = df.iloc[index,2]
    gcir = df.iloc[index,3]
    quartile = S(quartile)
    issue=jira.issue(story)
    if 'Q1' in quartile:
        issue.fields.labels.append(u'Q1')
    elif 'Q2' in quartile:
        issue.fields.labels.append(u'Q2')
    elif 'Q3' in quartile:
        issue.fields.labels.append(u'Q3')
    elif 'Q4' in quartile:
        issue.fields.labels.append(u'Q4')
    issue.update(fields={"labels": issue.fields.labels})



    
