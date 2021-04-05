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

#Get User credentials for JIRA authorization
username = input('Enter your user name: ')
password = getpass.getpass(prompt="Enter Password")
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

print('Getting issues from JIRA')
starttimetoload= time.perf_counter()

milestones = jira.project_versions('IDWH')

finishtimetoload= time.perf_counter()
print(f'Finished in loading datafromjson in {round(finishtimetoload-starttimetoload, 2)} seconds')
now = time.perf_counter()

print(f'Finished in loading data in {round(now-starttimetoload, 2)} seconds')


#Class to give a string for comparing strings to string-like variables
class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1

#establishing variables for later usage
milestone = pd.DataFrame()
Fix = []
CurrentStatus = []
Components = []
Epic = []
Key = []
Feature = []
epickey = pd.DataFrame()
epic = jira.search_issues('project = idwh and issuetype = epic', maxResults=1000)
for feature in epic:
    key = S(feature.key)
    summary = feature.fields.summary
    Key.append(key)
    Epic.append(summary)
epickey.insert(0, "Key", Key)
epickey.insert(1, "Epic", Epic)
epickey.to_excel('O:/epickey.xlsx')
for item in milestones:
    fix = S(item.name)
    id = S(item.id)
    string = 'project = "IDW 2.0 – Hadron" and issuetype= story and issueFunction in linkedIssuesOfAll("fixVersion = ' + id + '")'
    story = jira.search_issues(string)
    for issue in story:
        currentStatus = S(issue.fields.status)
        epic = S(issue.fields.customfield_10506)
        Fix.append(fix)
        CurrentStatus.append(currentStatus)
        Feature.append(epic)
milestone.insert(0,"Milestone", Fix)
milestone.insert(1, "Status", CurrentStatus)
milestone.insert(2, "Feature", Feature)
milestone = pd.merge(milestone, epickey, left_on = 'Feature', right_on = 'Key', how = 'left')
milestone= milestone.drop(['Feature', 'Key'], axis=1)

uniquemilestones = milestone.Milestone.unique()

tempdf=pd.DataFrame()
color_dict = {'Accepted':'#7030A0','Dev': '#4472C4', 'Prioritized': '#C00000', 'Ready for Prioritization': '#002060', 'Blocked':'#FFC000','In Progress':'#002060','Open':'#656565','QA':'#548235','Rejected':'#808080'}

for item in uniquemilestones:
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    tempdf = milestone
    tempdf = tempdf[tempdf['Milestone'].str.contains(item)]
    tempdf = tempdf.groupby(["Epic", "Status"]).size()
    tempdf = tempdf.unstack()
    ax1.legend(["Open", "Ready for Prioritization","Prioritized","Needs More Info","Blocked","Dev","QA","Accepted"])
    ax1= tempdf.plot(ax=ax1, kind='bar',stacked=True, figsize=(20,10), color=[color_dict.get(x) for x in tempdf.columns], label = ["Not Started", "In Progress","Blocked","QA","Accepted"],title=item)
    fig.savefig('O:/' + item + '.pdf', orientation='landscape', bbox_inches='tight')
    plt.close()
now = time.perf_counter()
print(f'Finished process in {round(now-finishtimetoload, 2)} seconds')
print('done')
