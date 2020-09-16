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
import datetime

start = time.perf_counter()
'''
The design of this report is to take two data sets, the attributes on the dev board (nycrs) and the views on the analysis board (nycrsa) and joining the two together.
The result is aggergated and sized by quartile for graphing within a pdf
'''
#Get User credentials for JIRA authorization
username = input('Enter your user name: ')
password = getpass.getpass(prompt="Enter Password")
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

starttimetoload= time.perf_counter()
#Utilize Jira search function to identify any views on the Analyst board that links to the Halogen View epic
datafromjson = jira.search_issues('project = NYC-RIO-Surge-Halogen-Analysis and "Epic Link" = NYCRSA-1566', maxResults=300)
finishtimetoload= time.perf_counter()
print(f'Finished in loading datafromjson in {round(finishtimetoload-starttimetoload, 2)} seconds')
datafromjson2 = requests.get('https://jira.troweprice.com/rest/api/2/search?jql=project%20=%20NYC-RIO-Surge-Halogen%20and%20component%20=%20%22party%20Domain%22&maxResults=1000&fields=status', auth=(username, password)).content
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

newdata=pd.DataFrame()
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
    #Iterate through each linked item
    for link in issue.fields.issuelinks:
        if hasattr(link, "outwardIssue"):
            outwardIssue = link.outwardIssue
            #Include the NYCRS as a comparison key to ensure we're only returning attributes
            if "NYCRS" in outwardIssue.key and outwardIssue.key[5] != 'A':
                Link.append(outwardIssue.key)
                #Item.append(issue.key)
                Item.append(summ)
        elif hasattr(link, "inwardIssue"):
            inwardIssue = link.inwardIssue
            #Include the NYCRS as a comparison key to ensure we're only returning attributes
            if "NYCRS" in inwardIssue.key and inwardIssue.key[5] != 'A':
                Link.append(inwardIssue.key)
                Item.append(summ)
newdata.insert(0,"Story",Item)
newdata.insert(1,"Link",Link)
#joins the dataframes to get correct status for each attribute relating to the view
newdata = pd.merge(newdata,datafromjson2,how = 'left', left_on='Link', right_on='key')

#data cleans: drop not needed fields and align statuses
newdata= newdata.drop(['fields.status.statusCategory.name', 'fields.status.statusCategory.colorName', 'fields.status.statusCategory.key','fields.status.statusCategory.id','fields.status.statusCategory.self','fields.status.id',  'fields.status.iconUrl', 'fields.status.description', 'fields.status.self', 'key', 'self', 'id', 'expand','Link'], axis=1)
newdata.rename(columns={'fields.status.name':'Status'}, inplace = True)
newdata=newdata.replace(to_replace="Prioritized", value="Not Started")
newdata=newdata.replace(to_replace="Open", value="Not Started")
newdata=newdata.replace(to_replace="Ready For Prioritization", value= "Not Started")
newdata=newdata.replace(to_replace="Dev", value="In Development")

newdata = newdata.groupby(['Story','Status']).size()

color_dict = {'Accepted':'#7030A0','Blocked':'#FFC000','In Development':'#002060','Not Started':'#C00000','QA':'#548235','Rejected':'#808080'}
output = 'C:\\Users\\' + username + '\\OneDrive - TRowePrice\\PartyAttributes-'+ str(datetime.datetime.today().strftime('%Y%m%d')) +'.pdf'
#output = 'O:/TransactionAttributes.pdf'
pdf = PdfPages('O:/Party.pdf')
fig1 = plt.figure()

with PdfPages(output) as pdf:
    ax1=fig1.add_subplot(111)
    newdata=newdata.unstack()
    newdata.plot(ax=ax1,kind='bar',stacked=True, figsize=(20,10),color=[color_dict.get(x) for x in newdata.columns], title="Party")

    pdf.savefig(fig1, orientation='landscape', bbox_inches="tight")

print(f'Total time: {round(time.perf_counter()-start, 2)} seconds')
print(f'Your pdf has been saved in {output}')
print("Done!")
