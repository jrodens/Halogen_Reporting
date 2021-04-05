#Determine what status each of the linked attributes for a view is in
from jira import JIRA
import json
import requests
import getpass
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import math

#Get User credentials for JIRA authorization
username = input('Enter your user name: ')
password = getpass.getpass(prompt="Enter Password")
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

#Utilize Jira search function to identify any views on the Analyst board that links to the Halogen View epic
datafromjson = jira.search_issues('project ="Halogen User Testing"  AND issuetype = "Test Case" AND "Business Unit (HUT)" = "Data Entitlement"', maxResults=1000)

#Class to give a string for comparing strings to string-like variables
class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1
teststatus = pd.DataFrame()
View=[]
Group = []
Accepted = []
Dev = []
Quality = []
Blocked = []
Open=[]
Readyviews = []
BlockedReports = []
Notstarted = []
Inprog = []
print('Getting issues from JIRA')
#Parse the returned JSON
for issue in datafromjson:
    summ = issue.fields.summary
    currentStatus = issue.fields.status
    currentID = issue.key
    accepted = 0
    dev = 0
    QA = 0
    blocked = 0
    openitem = 0
    group = S(issue.fields.customfield_25001)
    view = S(issue.fields.customfield_22700)
    currentIssue = str(issue.fields.status)
    s = S(currentIssue)
    for link in issue.fields.issuelinks:
        if hasattr(link, "outwardIssue"):
            outwardIssue = link.outwardIssue
            output= jira.issue(outwardIssue.key)
            string = 'key = ' + S(output)
            findissue = jira.search_issues(string)
            if "NYCRS" in outwardIssue.key or "NYCRSA" in outwardIssue.key:
                for item in findissue:
                    s = S(item.fields.status)
                    print(string)
        elif hasattr(link, "inwardIssue"):
            inwardIssue = link.inwardIssue
            output = jira.issue(inwardIssue.key)
            string = 'key = ' + S(output)
            if "NYCRS" in inwardIssue.key or "NYCRSA" in inwardIssue.key:
                for item in findissue:
                    s = S(item.fields.status)
                    print(string)
    #Pass through the returned value to the comparison method
    if "Accepted" in s:
        accepted = accepted +1
    elif "QA" in s:
        QA = QA + 1
    elif "Dev" in s:
        dev = dev + 1
    elif "Blocked" in s:
        blocked = blocked +1
    else:
        openitem= openitem +1
    Accepted.append(accepted)
    Quality.append(QA)
    Blocked.append(blocked)
    Dev.append(dev)
    Open.append(openitem)
    View.append(view)
    Group.append(group)
    if blocked == 0 and dev == 0 and QA == 0 and openitem == 0:
        Readyviews.append(summ)
    elif dev == 0 and QA == 0 and openitem == 0 and blocked > 0:
        BlockedReports.append(summ)
    elif dev == 0 and QA == 0 and accepted == 0 and openitem > 0:
        Notstarted.append(summ)
    elif openitem > 0 and blocked == 0:
        Inprog.append(summ)

print('Finished grabbing data; traisitioning to dataframe')

newdata=pd.DataFrame()
newdata.insert(0,"View", View)
newdata.insert(1,"Not Started",Open)
newdata.insert(2,"In Progress", Dev)
newdata.insert(3,"Blocked", Blocked)
newdata.insert(4,"QA", Quality)
newdata.insert(5,"Accepted", Accepted)
newdata.insert(6, "Group", Group)



print('Plotting data')
#newdata.set_index('Test Cases by Component',inplace = True, drop=True)

isready=[]

uniquebus = ["1", "2", "3"]
'''
DETERMINE THE LIST OF UNIQUE BUSINESS UNITS


for x in newdata["Test Cases by Business Unit"]:
    if x not in uniquebus:
        uniquebus.append(x)
print(uniquebus)

'''
'''
SORTING TO MAKE FINISHED VIEWS APPEAR FIRST
'''
for index, row in newdata.iterrows():
    if row['Not Started']==0 and row['In Progress']==0 and row['Blocked']==0 and row['QA']==0:
        isready.append(0)
    else:
        isready.append(1)
newdata.insert(5,"Sortby", isready)
newdata= newdata.sort_values(by='Sortby', ascending=True)
newdata=newdata.drop(['Sortby'], axis=1)



'''
PLOT DATA FOR EACH BUSINESS UNIT SAVE AS PDF
'''
color_dict = {'Accepted':'#7030A0','Blocked':'#FFC000','In Progress':'#002060','Not Started':'#C00000','QA':'#548235','Rejected':'#808080'}
fig1 = plt.figure()
ax2= fig1.add_subplot(111)
plotdata = newdata
plotdata = plotdata.groupby('View').sum()
ax2.legend(["Not Started", "In Progress","Blocked","QA","Accepted"])
ax2 = plotdata.plot(ax=ax2,kind='bar',stacked=True, figsize=(20,10),color=[color_dict.get(x) for x in plotdata.columns], label = ["Not Started", "In Progress","Blocked","QA","Accepted"],title="Test Case Status")
fig1.savefig('O:/Halogen Test Case Status.pdf', orientation='landscape', bbox_inches="tight")
plt.close()

for bu in uniquebus:
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plotdata = newdata[newdata['Group'].str.contains(bu)]
    plotdata = plotdata.groupby('View').sum()
    #plotdata.to_excel('O:/' + bu + '.xlsx')
    ax1.legend(["Not Started", "In Progress","Blocked","QA","Accepted"])
    ax1 = plotdata.plot(ax=ax1,kind='bar',stacked=True, figsize=(20,10),color=[color_dict.get(x) for x in plotdata.columns], label = ["Not Started", "In Progress","Blocked","QA","Accepted"],title=bu)
    fig.savefig('O:/' + bu + '.pdf', orientation='landscape', bbox_inches="tight")
    plt.close()

print("Done!")
