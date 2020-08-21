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
df = pd.read_excel('o:/ForUpload.xlsx')
#df.fillna("", inplace=True)
for index, row in df.iterrows():
    summ= df.iloc[index,0]
    #quartile=df.iloc[index,1]
    #link = df.iloc[index,2]
   # quartile = S(quartile)
    #acceptance = ""
    #acceptance = df.iloc[index,27]
    points=0
    points= df.iloc[index,4]
    points = int(points)
    #synthesis=df.iloc[index,2]
    #description = df.iloc[index,8]
    #epic=df.iloc[index,5]
    #acceptance = df.iloc[index,6]
    desc = df.iloc[index,3]
    component=df.iloc[index,1]
    quartile = df.iloc[index,2]
    #linkto = df.iloc[index,1]
    #print(summ)
    #print(desc)
    #print(linkto)
    issue_list = {
    'project': {'key': 'NYCRSA'},
    'summary': summ,
    'issuetype': {'name': 'Story'},
    'description': desc,
    'customfield_10502': points,
    }
    
    new_issue = jira.create_issue(fields=issue_list)
    print(new_issue)
    #new_issue.update(labels=[label])
    #new_issue.update(fields={"components": component})
    

    if 'Halogen Account Reference View Build' in quartile:
        new_issue.fields.labels.append(u'Halogen_Account_Reference_View_Build')
    elif 'Halogen Account Reference View Linkage' in quartile:
        new_issue.fields.labels.append(u'Halogen_Account_Reference_View_Linkage')
    elif 'Halogen Account Reference View Validation' in quartile:
        new_issue.fields.labels.append(u'Halogen_Account_Reference_View_Validation')
    elif 'Halogen Security Reference View Build' in quartile:
        new_issue.fields.labels.append(u'Halogen_Security_Reference_View_Build')
    elif 'Halogen Security Reference View Validation' in quartile:
        new_issue.fields.labels.append(u'Halogen_Security_Reference_View_Validation')
    elif 'Halogen BNYM_Other View Build' in quartile:
        new_issue.fields.labels.append(u'Halogen_BNYM_Other_View_Build')
    elif 'Halogen BNYM_Other View Linkage' in quartile:
        new_issue.fields.labels.append(u'Halogen_BNYM_Other_View_Linkage')
    elif 'Halogen BNYM_Other View Validation' in quartile:
        new_issue.fields.labels.append(u'Halogen_BNYM_Other_View_Validation')
    elif 'Halogen Performance View Linkage' in quartile:
        new_issue.fields.labels.append(u'Halogen_Performance_View_Linkage')
    elif 'Halogen Performance View Validation' in quartile:
        new_issue.fields.labels.append(u'Halogen_Performance_View_Validation')
    elif 'Halogen Mixed Domain View Linkage' in quartile:
        new_issue.fields.labels.append(u'Halogen_Mixed_Domain_View_Linkage')
    elif 'Halogen Mixed Domain View Validation' in quartile:
        new_issue.fields.labels.append(u'Halogen_Mixed_Domain_View_Validation')
        
    new_issue.update(fields={"labels": new_issue.fields.labels})
    #new_link = jira.create_issue_link('relates to', new_issue, link)
    #print(new_link)
print('Done')
