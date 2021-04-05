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
datafromjson = jira.search_issues('project ="Halogen User Testing"  AND issuetype = "Test Case"', maxResults=1000)

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
Transaction = []
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
        report = S(issue.fields.customfield_23500)
        currentIssue = str(issue.fields.status)
        transaction = S(issue.fields.customfield_22300)
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
        Report.append(report)
        Accepted.append(accepted)
        Quality.append(QA)
        Blocked.append(blocked)
        Dev.append(dev)
        Open.append(openitem)
        Components.append(component)
        Transaction.append(transaction)
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
newdata.insert(0,"Test Cases by Component", Transaction)
newdata.insert(1,"Not Started",Open)
newdata.insert(2,"In Progress", Dev)
newdata.insert(3,"Blocked", Blocked)
newdata.insert(4,"QA", Quality)
newdata.insert(5,"Accepted", Accepted)
newdata.insert(6, "Test Cases by Business Unit", Components)



print('Plotting data')
newdata.set_index('Test Cases by Component',inplace = True, drop=True)

isready=[]


'''
DETERMINE THE LIST OF UNIQUE BUSINESS UNITS
'''
uniquebus = []
for x in newdata["Test Cases by Business Unit"]:
    if x not in uniquebus:
        uniquebus.append(x)
print(uniquebus)

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
plotdata = plotdata.groupby('Test Cases by Component').sum()
ax2.legend(["Not Started", "In Progress","Blocked","QA","Accepted"])
ax2 = plotdata.plot(ax=ax2,kind='bar',stacked=True, figsize=(20,10),color=[color_dict.get(x) for x in plotdata.columns], label = ["Not Started", "In Progress","Blocked","QA","Accepted"],title="Test Case Status")
fig1.savefig('O:/Halogen Test Case Status.pdf', orientation='landscape', bbox_inches="tight")
plt.close()

for bu in uniquebus:
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plotdata = newdata[newdata['Test Cases by Business Unit'].str.contains(bu)]
    plotdata = plotdata.groupby('Test Cases by Component').sum()
    #plotdata.to_excel('O:/' + bu + '.xlsx')
    ax1.legend(["Not Started", "In Progress","Blocked","QA","Accepted"])
    ax1 = plotdata.plot(ax=ax1,kind='bar',stacked=True, figsize=(20,10),color=[color_dict.get(x) for x in plotdata.columns], label = ["Not Started", "In Progress","Blocked","QA","Accepted"],title=bu)
    fig.savefig('O:/' + bu + '.pdf', orientation='landscape', bbox_inches="tight")
    plt.close()

print("Done!")
