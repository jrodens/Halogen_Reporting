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
import matplotlib.patches as patches
import numpy as np
start = time.perf_counter()

#Get User credentials for JIRA authorization
username = input('Enter your user name: ')
password = getpass.getpass(prompt="Enter Password")
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

print('Getting issues from JIRA')
starttimetoload= time.perf_counter()

milestones = jira.project_versions('IDWH')

finishtimetoload= time.perf_counter()
print(f'Finished in loading milestones in {round(finishtimetoload-starttimetoload, 2)} seconds')



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
Milestonestart=[]
Milestoneend = []
Milestonename = []
Points = []
epickey = pd.DataFrame()
milestonereference = pd.DataFrame()
epic = jira.search_issues('project = idwh and issuetype = epic', maxResults=1000)
for feature in epic:
    key = S(feature.key)
    summary = feature.fields.summary
    Key.append(key)
    Epic.append(summary)
epickey.insert(0, "Key", Key)
epickey.insert(1, "Epic", Epic)
#epickey.to_excel('O:/epickey.xlsx')
for item in milestones:
    fix = S(item.name)
    id = S(item.id)
    m = S(item.name)
    milestoneurl = 'https://jira.troweprice.com/rest/api/latest/version/' + id
    milestonedata = requests.get(milestoneurl, auth=(username, password)).content
    milestonedata = pd.read_json(milestonedata, typ='series', orient='columns')
    milestonestart = milestonedata.startDate
    milestonestart = datetime.datetime.strptime(milestonestart[0:10], '%Y-%m-%d')
    milestoneend = milestonedata.releaseDate
    milestonend = datetime.datetime.strptime(milestoneend[0:10], '%Y-%m-%d')
    Milestonestart.append(milestonestart)
    Milestoneend.append(milestoneend)
    Milestonename.append(m)
    string = 'project = "IDW 2.0 – Hadron" and issuetype= story and issueFunction in linkedIssuesOfAll("fixVersion = ' + id + '")'
    story = jira.search_issues(string)
    for issue in story:
        if S(issue.fields.status) == 'Rejected':
            pass
        else:
            currentStatus = S(issue.fields.status)
            epic = S(issue.fields.customfield_10506)
            Fix.append(fix)
            CurrentStatus.append(currentStatus)
            Feature.append(epic)
            points = issue.fields.customfield_10502
            Points.append(points)
milestonereference.insert(0, "Milestone", Milestonename)
milestonereference.insert(1, "Start", Milestonestart)
milestonereference.insert(2, "End", Milestoneend)
milestone.insert(0,"Milestone", Fix)
milestone.insert(1, "Status", CurrentStatus)
milestone.insert(2, "Feature", Feature)
milestone.insert(3, "Points", Points)
milestone = milestone.replace(to_replace="Prioritized", value = "Not Started")
milestone = milestone.replace(to_replace="Ready For Prioritization", value = "Not Started")
milestone = milestone.replace(to_replace="Open", value= "Not Started")
milestone = pd.merge(milestone, epickey, left_on = 'Feature', right_on = 'Key', how = 'left')
#milestone = milestone[milestone['Status']
#pointcount[pointcount['Milestone'].str.contains(item)]
milestone= milestone.drop(['Feature', 'Key'], axis=1)
now = time.perf_counter()
milestone.to_excel('O:/IDW 2 Milestones.xlsx')
print(f'Finished in loading issues in {round(now-starttimetoload, 2)} seconds')
uniquemilestones = milestone.Milestone.unique()


tempdf=pd.DataFrame()
color_dict = {'Accepted':'#7030A0','Dev': '#4472C4', 'Prioritized': '#C00000', 'Ready For Prioritization': '#002060', 'Blocked':'#FFC000','In Progress':'#002060','Not Started':'#C00000','QA':'#548235','Rejected':'#808080'}

today= datetime.datetime(2020,10,16,0,0)

tempdf2 = pd.DataFrame()
i=0
today = datetime.datetime.today()
today = today.date()

for item in uniquemilestones:
    pointpercent = 0
    pointcount = pd.DataFrame()
    tempmilestone=pd.DataFrame()
    fig = plt.figure()
    ax1 = fig.add_subplot(121) #top and bottom left (large)
    ax2 = fig.add_subplot(222) # top right
    ax3 = fig.add_subplot(224) #bottom right
    notdone = milestone.groupby('Status').Points.agg(['sum'])
    tempdf = milestone
    tempdf2 = milestone
    pointcount = milestone
    tempdf = tempdf[tempdf['Milestone'].str.contains(item)]
    tempdf = tempdf.groupby(["Epic", "Status"]).size()
    tempdf = tempdf.unstack()
    pointcount = pointcount[pointcount['Milestone'].str.contains(item)]
    pointcount = pointcount.groupby(['Status']).sum()
    if 'Accepted' in pointcount.Points:
        pointpercent = pointcount.Points['Accepted']

    else:
        pointpercent = 0
    ax1.legend(["Not Started","In Progress","Blocked", "QA","Accepted"])
    ax1= tempdf.plot(ax=ax1, kind='bar',stacked=True, figsize=(20,10), color=[color_dict.get(x) for x in tempdf.columns], label = ["Not Started", "In Progress","Blocked","QA","Accepted"],title=item)
    tempdf2 = tempdf2[tempdf2['Milestone'].str.contains(item)]
    tempdf2 = tempdf2.groupby(['Status']).sum()
    tempdf2 = tempdf2.unstack()
    tempdf2 = tempdf2.unstack()
    ax2 = tempdf2.plot(ax=ax2, kind='barh', stacked=True, color=[color_dict.get(x) for x in tempdf.columns], legend = None, title="Milestone Status (by Story Points)")
    ax2.set_ylabel("")
    ax2.axis('off')
    ax2.axvline(x=pointpercent, ymin = .8, ymax = .2, color='black')
    tempmilestone = milestonereference[milestonereference['Milestone'].str.contains(item)]
#    ax3 = px.timeline(milestonereference, x_start=Milestonestart, x_end = Milestoneend, y=Milestonename)
    ax3.add_patch(
        patches.Rectangle(
            xy=(0, 1),  # point of origin.
            height=100,
            width= .85,
            linewidth=100,
            color='blue',
            fill=True
        )
    )
    s=tempmilestone.Start[i].strftime("%B %d, %Y")
    t=datetime.datetime.strptime(tempmilestone.End[i], '%Y-%m-%d')
    ttemp = t.date()
    stemp = tempmilestone.Start[i].date()
    t = t.strftime("%B %d, %Y")
    now = np.busday_count(stemp,today)
    days= np.busday_count(stemp, ttemp)
    print(now)
    print(stemp)
    print(ttemp)
    if now <0:
        percent = 0
    elif ttemp < today:
        percent = 0
    else:
        percent = now/days

    s=S(s)
    t=S(t)

    s= 'Milestone Start: ' + s
    t = 'Milestone End: ' + t
    ax3.text(0.05,.75, s, fontsize=7.5)
    ax3.axvline(x=0, ymin=.75, color='black')
    ax3.text(.67,.75, t, fontsize= 7.5)
    ax3.axvline(x=.95, ymin=.75, color='black')
    ax3.set_title('Time to Milestone Completion')
    ax3.axvline(x=percent,ymin=.8,color='black')
    i=i+1
    ax3.axis('off')
    fig.savefig('O:/' + item + '.pdf', orientation='landscape', bbox_inches='tight')
    plt.close()



now = time.perf_counter()
print(f'Finished process in {round(now-finishtimetoload, 2)} seconds')
print('done')
