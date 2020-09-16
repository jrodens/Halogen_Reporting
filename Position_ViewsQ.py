#Determine what status each of the linked attributes for a view is in
from jira import JIRA
import json
import requests
import getpass
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

#Get User credentials for JIRA authorization
username = input('Enter your user name: ')
password = getpass.getpass(prompt="Enter Password")
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

#Utilize Jira search function to identify any views on the Analyst board that links to the Halogen View epic
datafromjson = jira.search_issues('project = NYC-RIO-Surge-Halogen-Analysis and "Epic Link" = NYCRSA-993', maxResults=1000)

#Class to give a string for comparing strings to string-like variables
class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1
q1 = pd.DataFrame()
q2=pd.DataFrame()
q3= pd.DataFrame()
q4=pd.DataFrame()

Accepted = []
Dev = []
Quality = []
Blocked = []
Report = []
Open=[]
Readyviews = []
BlockedReports = []
Notstarted = []
Inprog = []
Labels = []
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
    label= issue.fields.labels
    label=S(label)
    #Iterate through each linked item
    for link in issue.fields.issuelinks:
        if hasattr(link, "outwardIssue"):
            outwardIssue = link.outwardIssue
            #Include the NYCRS as a comparison key to ensure we're only returning attributes
            if "NYCRS" in outwardIssue.key and outwardIssue.key[5] != 'A':
                issue = jira.issue(outwardIssue.key)
                currentIssue = str(issue.fields.status)
                s = S(currentIssue)
                d = S(currentStatus)
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
        elif hasattr(link, "inwardIssue"):
            inwardIssue = link.inwardIssue
            #Include the NYCRS as a comparison key to ensure we're only returning attributes
            if "NYCRS" in inwardIssue.key and inwardIssue.key[5] != 'A':
                issue = jira.issue(inwardIssue.key)
                currentIssue = str(issue.fields.status)
                s = S(currentIssue)
                d = S(currentStatus)
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
    Report.append(summ)
    Accepted.append(accepted)
    Quality.append(QA)
    Blocked.append(blocked)
    Dev.append(dev)
    Open.append(openitem)
    Labels.append(label)
    if blocked == 0 and dev == 0 and QA == 0 and openitem == 0:
        Readyviews.append(summ)
    elif dev == 0 and QA == 0 and openitem == 0 and blocked > 0:
        BlockedReports.append(summ)
    elif dev == 0 and QA == 0 and accepted == 0 and openitem > 0:
        Notstarted.append(summ)
    elif openitem > 0 and blocked == 0:
        Inprog.append(summ)
    #For each view, print the number of open, aceepted, QA, blocked and dev dependencies along with the view name
    #print('{} has {} open items, {} accepted items, {} items in QA, {} blocked and {} in development'.format(summ, openitem, accepted, QA, blocked, dev))
print('Finished grabbing data; traisitioning to dataframe')
print(f"Views with all attributes completed: {Readyviews}")
print(f"Views blocked: {BlockedReports}")
print(f"Ready for Development: {len(Readyviews)}")
print(f"Blocked: {len(BlockedReports)}")
print(f"Not Started: {len(Notstarted)}")
print(f"In Progress: {len(Inprog)}")
newdata=pd.DataFrame()
newdata.insert(0,"Position View", Report)
newdata.insert(1,"Not Started",Open)
newdata.insert(2,"In Development", Dev)
newdata.insert(3,"Blocked", Blocked)
newdata.insert(4,"QA", Quality)
newdata.insert(5,"Accepted", Accepted)
newdata.insert(6, "Labels", Labels)

#newdata.to_excel('O:/Position Attribute Data.xlsx')

print('Plotting data')
newdata.set_index('Position View',inplace = True, drop=True)
q1 = newdata[newdata['Labels'].str.contains("Q1")]
q2 = newdata[newdata['Labels'].str.contains("Q2")]
q3 = newdata[newdata['Labels'].str.contains("Q3")]
q4 = newdata[newdata['Labels'].str.contains("Q4")]
isready=[]
for index, row in newdata.iterrows():
    if row['Not Started']==0 and row['In Development']==0 and row['Blocked']==0 and row['QA']==0:
        isready.append(0)
    else:
        isready.append(1)
newdata.insert(5,"Sortby", isready)
newdata= newdata.sort_values(by='Sortby', ascending=True)
newdata=newdata.drop(['Sortby'], axis=1)

q1=q1.drop(columns='Labels')
q2=q2.drop(columns='Labels')
q3=q3.drop(columns='Labels')
q4=q4.drop(columns='Labels')

pdf = PdfPages('O:/PositionAttributesQ.pdf')
fig = plt.figure()
fig2 = plt.figure()
fig3 = plt.figure()
fig4 = plt.figure()

with PdfPages('O:/PositionAttributesQ.pdf') as pdf:
    ax1=fig.add_subplot(111)
    ax1=q1.plot(ax=ax1,kind='bar',stacked=True, figsize=(20,10),color=['#C00000','#002060','#FFC000','#548235','#7030A0'], title="Q1 Position Views")

    ax2=fig2.add_subplot(111)
    q2.plot(ax=ax2,kind='bar',stacked=True, figsize=(20,10),color=['#C00000','#002060','#FFC000','#548235','#7030A0'], title="Q2 Position Views")

    #fig.savefig('O:/Position AttributesQ1.pdf', orientation='landscape', bbox_inches="tight")
    
    ax3=fig3.add_subplot(111)
    q3.plot(ax=ax3,kind='bar',stacked=True, figsize=(20,10),color=['#C00000','#002060','#FFC000','#548235','#7030A0'], title="Q3 Position Views")

    ax4=fig4.add_subplot(111)
    q4.plot(ax=ax4,kind='bar',stacked=True, figsize=(20,10),color=['#C00000','#002060','#FFC000','#548235','#7030A0'], title="Q4 Position Views")

    pdf.savefig(fig, orientation='landscape', bbox_inches="tight")
    pdf.savefig(fig2, orientation='landscape', bbox_inches="tight")
    pdf.savefig(fig3, orientation='landscape', bbox_inches="tight")
    pdf.savefig(fig4, orientation='landscape', bbox_inches="tight")
    
#newdata.plot.bar(stacked=True, figsize=(20,10), color=['#C00000','#002060','#FFC000','#548235','#7030A0'])
#plt.show()
#plt.savefig('O:/Position AttributesB.pdf', orientation='landscape', bbox_inches="tight")

#newdata.to_excel('O:/Position Attribute Data.xlsx')
print("Done!")
