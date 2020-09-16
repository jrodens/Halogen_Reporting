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
datafromjson = jira.search_issues('project ="Halogen User Testing"  AND issuetype = Task', maxResults=1000)

#Class to give a string for comparing strings to string-like variables
class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1
teststatus = pd.DataFrame()


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
Components = []
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

    if issue.fields.issuetype.name == "Task":
        for components in issue.fields.components:
            component = components.name
        component =S(component)
        report = S(issue.fields.customfield_22500)
        print(report)
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

        print(f'The component is {component}')
        Report.append(report)
        Accepted.append(accepted)
        Quality.append(QA)
        Blocked.append(blocked)
        Dev.append(dev)
        Open.append(openitem)
        Components.append(component)
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
newdata.insert(0,"Test Cases by Views", Report)
newdata.insert(1,"Not Started",Open)
newdata.insert(2,"In Progress", Dev)
newdata.insert(3,"Blocked", Blocked)
newdata.insert(4,"QA", Quality)
newdata.insert(5,"Accepted", Accepted)
newdata.insert(6, "Test Cases by Business Unit", Components)



print('Plotting data')
newdata.set_index('Test Cases by Views',inplace = True, drop=True)

isready=[]

uniquebus = []
for x in newdata["Test Cases by Business Unit"]:
    if x not in uniquebus:
        uniquebus.append(x)
print(uniquebus)

for index, row in newdata.iterrows():
    if row['Not Started']==0 and row['In Progress']==0 and row['Blocked']==0 and row['QA']==0:
        isready.append(0)
    else:
        isready.append(1)
newdata.insert(5,"Sortby", isready)
newdata= newdata.sort_values(by='Sortby', ascending=True)
newdata=newdata.drop(['Sortby'], axis=1)

'''
newdata.plot.bar(stacked=True, figsize=(20,10), color=['#C00000','#002060','#FFC000','#548235','#7030A0'])
#plt.show()
plt.savefig('O:/Test Cases Grouped.pdf', orientation='landscape', bbox_inches="tight")



#newdata.groupby('Test Cases by Business Unit').sum().plot(kind='bar',stacked=True, color=['#C00000','#002060','#FFC000','#548235','#7030A0'])
#plt.savefig('O:/Testcases.pdf', orientation='landscape', bbox_inches="tight")
#newdata.to_excel('O:/TestCases.xlsx')

q1=q1.drop(columns='Labels')
q2=q2.drop(columns='Labels')
q3=q3.drop(columns='Labels')
q4=q4.drop(columns='Labels')

pdf = PdfPages('O:/PositionAttributesQ.pdf')
fig = plt.figure()
fig2 = plt.figure()
fig3 = plt.figure()
fig4 = plt.figure()
'''

#with PdfPages() as pdf:
for bu in uniquebus:
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plotdata = newdata[newdata['Test Cases by Business Unit'].str.contains(bu)]
    plotdata = plotdata.groupby('Test Cases by Views').sum()
    #plotdata.to_excel('O:/' + bu + '.xlsx')
    ax1.legend(["Not Started", "In Progress","Blocked","QA","Accepted"])
    ax1 = plotdata.plot(ax=ax1,kind='bar',stacked=True, figsize=(20,10),color=['#C00000','#002060','#FFC000','#548235','#7030A0'], label = ["Not Started", "In Progress","Blocked","QA","Accepted"],title=bu)
    fig.savefig('O:/' + bu + '.pdf', orientation='landscape', bbox_inches="tight")
    plt.close()

#newdata.plot.bar(stacked=True, figsize=(20,10), color=['#C00000','#002060','#FFC000','#548235','#7030A0'])
#plt.savefig('O:/User Testing.pdf', orientation='landscape', bbox_inches="tight")
#newdata.plot.bar(stacked=True, figsize=(20,10), color=['#C00000','#002060','#FFC000','#548235','#7030A0'])
#plt.show()
#plt.savefig('O:/Position AttributesB.pdf', orientation='landscape', bbox_inches="tight")

#newdata.to_excel('O:/Position Attribute Data.xlsx')
print("Done!")
