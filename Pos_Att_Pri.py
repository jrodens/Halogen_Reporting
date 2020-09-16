#Determine what status each of the linked attributes for a view is in
from jira import JIRA
import json
import requests
import getpass
import pandas as pd
from pandas.io.json import json_normalize
import time

start = time.perf_counter()

#Get User credentials for JIRA authorization
username = input('Enter your user name: ')
password = getpass.getpass(prompt="Enter Password")
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})
print('Getting issues from JIRA')
#Utilize Jira search function to identify any views on the Analyst board that links to the Halogen View epic
starttimetoload= time.perf_counter()
datafromjson = jira.search_issues('project = NYC-RIO-Surge-Halogen-Analysis and "Epic Link" = NYCRSA-993', maxResults=1000,fields="summary, issuelinks, labels")
finishtimetoload= time.perf_counter()
print(f'Finished in loading datafromjson in {round(finishtimetoload-starttimetoload, 2)} seconds')
datafromjson2 = requests.get('https://jira.troweprice.com/rest/api/2/search?jql=project%20=%20NYC-RIO-Surge-Halogen%20and%20component%20=%20%22Positions%20Domain%22&maxResults=1000&fields=status', auth=(username, password)).content
now = time.perf_counter()
print(f'Finished in loading datafromjson2 in {round(now-finishtimetoload, 2)} seconds')
print(f'Finished in loading data in {round(now-starttimetoload, 2)} seconds')
datafromjson2 = pd.read_json(datafromjson2, typ='series', orient='columns')
datafromjson2=json_normalize(datafromjson2['issues'],meta=['fields.status.name'])
#Class to give a string for comparing strings to string-like variables
class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1

Labels = []
Summary = []
Link = []
Item=[]
Status=[]

q1=pd.DataFrame()
q2=pd.DataFrame()
q3=pd.DataFrame()
q4=pd.DataFrame()

#Parse the returned JSON
for issue in datafromjson:
    summ = issue.fields.summary
    #currentStatus = issue.fields.status
    currentID = issue.key
    label= issue.fields.labels
    label=S(label)
    #Iterate through each linked item
    for link in issue.fields.issuelinks:
        if hasattr(link, "outwardIssue"):
            outwardIssue = link.outwardIssue
            #Include the NYCRS as a comparison key to ensure we're only returning attributes
            if "NYCRS" in outwardIssue.key and outwardIssue.key[5] != 'A':
                Link.append(outwardIssue.key)
                #Item.append(issue.key)
                Item.append(summ)
                Labels.append(label)
        elif hasattr(link, "inwardIssue"):
            inwardIssue = link.inwardIssue
            #Include the NYCRS as a comparison key to ensure we're only returning attributes
            if "NYCRS" in inwardIssue.key and inwardIssue.key[5] != 'A':
                Link.append(inwardIssue.key)
                #Item.append(issue.key)
                Item.append(summ)
                Labels.append(label)
q1.insert(0,"Story",Item)
q1.insert(1,"Link",Link)
q1.insert(2,"Label",Labels)
#datafromjson2.to_excel('O:/df2.xlsx')

newdata = pd.merge(q1,datafromjson2,how = 'left', left_on='Link', right_on='key')

newdata= newdata.drop(['fields.status.statusCategory.name', 'fields.status.statusCategory.colorName', 'fields.status.statusCategory.key','fields.status.statusCategory.id','fields.status.statusCategory.self','fields.status.id',  'fields.status.iconUrl', 'fields.status.description', 'fields.status.self', 'self', 'id', 'expand','Link'], axis=1)
newdata.rename(columns={'fields.status.name':'Status', 'key':'Attribute'}, inplace = True)
newdata=newdata.replace(to_replace="Prioritized", value="Not Started")
newdata=newdata.replace(to_replace="Open", value="Not Started")
newdata=newdata.replace(to_replace="Ready For Prioritization", value= "Not Started")
newdata=newdata.replace(to_replace="Dev", value="In Development")
#newdata.to_excel('O:/df3.xlsx', index=False)



q1 = newdata[newdata['Label'].str.contains("Q1")]
q2 = newdata[newdata['Label'].str.contains("Q2")]
q3 = newdata[newdata['Label'].str.contains("Q3")]
q4 = newdata[newdata['Label'].str.contains("Q4")]

q1=q1.drop(columns='Label')
q2=q2.drop(columns='Label')
q3=q3.drop(columns='Label')
q4=q4.drop(columns='Label')

#q1 = q1.groupby(['Story','Status']).size()
#q2 = q2.groupby(['Story','Status']).size()
#q3 = q3.groupby(['Story','Status']).size()
#q4 = q4.groupby(['Story','Status']).size()

q1.to_excel('O:/df.xlsx')

print(f'Total time: {round(time.perf_counter()-start, 2)} seconds')
print('done')
