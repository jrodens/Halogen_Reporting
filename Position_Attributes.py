#Determine what status each of the linked attributes for a view is in
from jira import JIRA
import json
import requests
import getpass
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
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
df = pd.DataFrame()
stories = pd.DataFrame()

Labels = []
Summary = []
Link = []
Item=[]
Status=[]

#Parse the returned JSON
for issue in datafromjson:
    summ = issue.fields.summary
    #currentStatus = issue.fields.status
    currentID = issue.key
    label= issue.fields.labels
    label=S(label)
    if 'Q1' in label:
        label = 'Q1'
    elif 'Q2' in label:
        label = 'Q2'
    elif 'Q3' in label:
        label = 'Q3'
    elif 'Q4' in label:
        label = 'Q4'
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
df.insert(0,"Story",Item)
df.insert(1,"Link",Link)
df.insert(2,"Label",Labels)
#stories.insert(0,"Story", Item)
#datafromjson2.to_excel('O:/df2.xlsx')

newdata = pd.merge(df,datafromjson2,how = 'left', left_on='Link', right_on='key')


newdata= newdata.drop(['fields.status.statusCategory.name', 'fields.status.statusCategory.colorName', 'fields.status.statusCategory.key','fields.status.statusCategory.id','fields.status.statusCategory.self','fields.status.id',  'fields.status.iconUrl', 'fields.status.description', 'fields.status.self',  'self', 'id', 'expand','Link'], axis=1)
newdata.rename(columns={'fields.status.name':'Status'}, inplace = True)
newdata=newdata.replace(to_replace="Open", value="Not Started")
newdata=newdata.replace(to_replace="Ready For Prioritization", value= "Not Started")
newdata=newdata.replace(to_replace="Prioritized", value = "Not Started")


newdata = newdata[newdata.Status=='Not Started']
newdata['counts']= newdata.groupby('Story').Status.transform(lambda x:x.count())
newdata = newdata.sort_values(by=['counts','Label','Story'], ascending = True)
newdata = newdata.drop_duplicates(subset='key')
newdata = newdata.rename({'key':'Attribute', 'Story':'View', 'counts':'Count of Not Started Attributes'}, axis='columns')
control = pd.merge(datafromjson2, newdata,how='outer', right_on='Attribute', left_on='key', indicator=True)
control = control[(control['fields.status.name']=='Open')|(control['fields.status.name']=='Prioritized')|(control['fields.status.name']=='Ready For Prioritization')]
control = control[control['_merge']=='left_only']
control = control['key']
validationcount=control.count()
if validationcount > 0:
    print(f'The following {validationcount} attributes  require further analysis: ')
    print(control.values)
    control.to_excel('O:/Controlfile.xlsx', index=False)
newdata.to_excel('O:/attributes.xlsx', index=False)
#newdata = newdata.sort_values(by=newdata['Story'].value_counts())

#newdata.to_excel('O:/attributes.xlsx')



print(f'Total time: {round(time.perf_counter()-start, 2)} seconds')
print('done')
