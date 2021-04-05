#Determine what status each of the linked attributes for a view is in
from jira import JIRA
import json
import requests
import getpass
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import datetime
import numpy as np

#Get User credentials for JIRA authorization
username = input('Enter your user name: ')
password = getpass.getpass(prompt="Enter Password")
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

#Utilize Jira search function to identify any views on the Analyst board that links to the Halogen View epic
datafromjson = jira.search_issues('project ="NYC-RIO-Surge-Transaction-Router-Testing"  AND issuetype = Defect', maxResults=1000)
testcasesfromjson = jira.search_issues('project = "NYCRSTRT" AND issuetype= "Story" AND status != "Rejected"', maxResults=1000)

#Class to give a string for comparing strings to string-like variables
class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1
teststatus = pd.DataFrame()

PTS = ['LaMotte, Julie', 'Kerner, Chris', 'Rooney, Matthew', 'McNulty, John', 'Yearly, Dorsey']
IL = ['Deaver, Daniel', 'Posey, Jessica', 'Rosenberger, Adam']
FA = ['Dull, Robin', 'Foard, Eric', 'Brummett, Andrea']

today = datetime.datetime.today().strftime("%A")

non=0
pts = 0
il = 0
fa = 0

Accepted = []
Dev = []
Quality = []
Blocked = []
Open=[]
Rejected = []
Accepted1 = []
Dev1 = []
Quality1 = []
Blocked1 = []
Open1=[]
Readyviews = []
BlockedReports = []
Notstarted = []
Inprog = []
Transaction = []
Entry=[]

graphbygroup = pd.DataFrame()
testdf = pd.DataFrame()

startdate = datetime.datetime(2020, 2, 12)

Dates = []
DefectCount = []
TestStatus = []
Group = []
Transtype = []
Story = []

for issue in testcasesfromjson:
    accepted = 0
    dev = 0
    QA = 0
    blocked = 0
    openitem = 0
    if S(issue.fields.status) == "Rejected":
        pass
    Transtype.append(S(issue.fields.customfield_23301))
    labels =  S(issue.fields.labels)
    if "il" in labels:
        group = "Investment Liaisons"
    elif "PTS" in labels:
        group = "Post Trade Services"
    elif "FA_OPs" in labels:
        group = "Fund Accounting Operations"
    else:
        group = "No Group Specified"
    Group.append(group)
    Story.append(issue.key)
    currentStatus = S(issue.fields.status)
    if "Accepted" in currentStatus:
        accepted = accepted +1
    elif "QA" in currentStatus:
        QA = QA + 1
    elif "Dev" in currentStatus:
        dev = dev + 1
    elif "Blocked" in currentStatus:
        blocked = blocked +1
    else:
        openitem= openitem +1
    Accepted1.append(accepted)
    Quality1.append(QA)
    Blocked1.append(blocked)
    Dev1.append(dev)
    Open1.append(openitem)
testdf.insert(0, "User Group", Group)
testdf.insert(1, "Transaction Type", Transtype)
testdf.insert(2,"Not Started",Open1)
testdf.insert(3,"In Development", Dev1)
testdf.insert(4,"Blocked", Blocked1)
testdf.insert(5,"QA", Quality1)
testdf.insert(6,"Accepted", Accepted1)


todaysdate = datetime.datetime.now()
yesterday = todaysdate - datetime.timedelta(1)
while (startdate <= yesterday):
    startdate = startdate + datetime.timedelta(1)
    if (datetime.datetime.strftime(startdate, '%A') != 'Saturday') and (datetime.datetime.strftime(startdate, '%A') != 'Sunday'):
        Dates.append(datetime.datetime.strftime(startdate, '%Y-%m-%d'))
        DefectCount.append(0)
#print(len(Dates))
#print(len(DefectCount))
#Components = []
print('Getting issues from JIRA')
#Parse the returned JSON
for issue in datafromjson:
    if S(issue.fields.status) == "Rejected":
        pass
    submitter = issue.fields.creator.displayName
    summ = issue.fields.summary
    currentStatus = S(issue.fields.status)
    currentID = issue.key
    transaction = S(issue.fields.customfield_23301)
    entry= S(issue.fields.customfield_23300)
    accepted = 0
    dev = 0
    QA = 0
    blocked = 0
    openitem = 0
    rejected = 0
    if submitter in PTS:
        pts =pts +1
    elif submitter in IL:
        il = il +1
    elif submitter in FA:
        fa = fa + 1
    else:
        non = non +1
    #Pass through the returned value to the comparison method
    if "Accepted" in currentStatus:
        accepted = accepted +1
    elif "QA" in currentStatus:
        QA = QA + 1
    elif "Dev" in currentStatus:
        dev = dev + 1
    elif "Blocked" in currentStatus:
        blocked = blocked +1
    elif "Rejected" in currentStatus:
        rejected = rejected +1
    else:
        openitem= openitem +1
    Rejected.append(rejected)
    Accepted.append(accepted)
    Quality.append(QA)
    Blocked.append(blocked)
    Dev.append(dev)
    Open.append(openitem)
    Transaction.append(transaction)
    Entry.append(entry)
#    Components.append(component)
    if blocked == 0 and dev == 0 and QA == 0 and openitem == 0:
        Readyviews.append(summ)
    elif dev == 0 and QA == 0 and openitem == 0 and blocked > 0:
        BlockedReports.append(summ)
    elif dev == 0 and QA == 0 and accepted == 0 and openitem > 0:
        Notstarted.append(summ)
    elif openitem > 0 and blocked == 0:
        Inprog.append(summ)
    #url = 'https://jira.troweprice.com/rest/api/2/issue' + currentID + '?expand=changelog'
    issuefromjson = jira.issue(currentID, expand='changelog')
    changelog = issuefromjson.changelog
    createdate = datetime.datetime.strptime(issue.fields.created[0:10], '%Y-%m-%d')
    acceptdate =  startdate
    for history in changelog.histories:
        for item in history.items:
            dated = datetime.datetime.strptime(history.created[0:10], '%Y-%m-%d')
            if (item.field == "status") & ((S(item.toString) == "Accepted") or (S(item.toString) == "Rejected")):
                #print(item)
                acceptdate = dated
    vardate = datetime.datetime(2020, 2, 12)
    i=-1
    while (acceptdate>=vardate):
        if (vardate < createdate):
            #print(f'For {currentID}, the accepted date is {acceptdate}, the vardate is {vardate} and the createdate is {createdate} and i equals {i}')
            #print(DefectCount)
            vardate = vardate + datetime.timedelta(1)
            if (datetime.datetime.strftime(vardate, '%A') != 'Saturday') and (datetime.datetime.strftime(vardate, '%A') != 'Sunday'):
                i=i+1
        else:
            if (datetime.datetime.strftime(vardate, '%A') != 'Saturday') and (datetime.datetime.strftime(vardate, '%A') != 'Sunday'):
                #print(i)
                DefectCount[i] = DefectCount[i] + 1
                #print(f'For {currentID}, the accepted date is {acceptdate}, the vardate is {vardate} and the createdate is {createdate} and i equals {i}.  Add 1')
                #print(DefectCount)
                i=i+1
            else:
                pass

            vardate = vardate + datetime.timedelta(1)
    #For each view, print the number of open, aceepted, QA, blocked and dev dependencies along with the view name
    #print('{} has {} open items, {} accepted items, {} items in QA, {} blocked and {} in development'.format(summ, openitem, accepted, QA, blocked, dev))
print('Finished grabbing data; traisitioning to dataframe')
print(f'Post Trade Services has {pts} items submitted')
print(f'Investment Liasions has {il} items submitted')
print(f'Fund Accounting has {fa} items submitted')
print(f'There are {non} items not assigned to a team')
newdata=pd.DataFrame()
newdata.insert(0,"Defects by Transaction Type", Transaction)
newdata.insert(1,"Not Started",Open)
newdata.insert(2,"In Development", Dev)
newdata.insert(3,"Blocked", Blocked)
newdata.insert(4,"QA", Quality)
newdata.insert(5,"Accepted", Accepted)
newdata.insert(6,"Rejected", Rejected)
#newdata.insert(6, "Test Cases by Business Unit", Components)

#newdata.to_excel('O:/Position Attribute Data.xlsx')

print('Plotting data')
newdata.set_index('Defects by Transaction Type',inplace = True, drop=True)

isready=[]

for index, row in newdata.iterrows():
    if row['Not Started']==0 and row['In Development']==0 and row['Blocked']==0 and row['QA']==0:
        isready.append(0)
    else:
        isready.append(1)
newdata.insert(5,"Sortby", isready)
newdata= newdata.sort_values(by='Sortby', ascending=True)
newdata=newdata.drop(['Sortby'], axis=1)

#ax.xaxis.set_major_locator(MaxNLocator(integer=True))
color_dict = {'Accepted':'#7030A0','Blocked':'#FFC000','In Development':'#002060','Not Started':'#C00000','QA':'#548235','Rejected':'#808080'}
output = 'C:\\Users\\' + username + '\\OneDrive - TRowePrice\\Transaction Router Defects by Transaction-'+ str(datetime.datetime.today().strftime('%Y%m%d')) +'.pdf'
newdata.groupby('Defects by Transaction Type').sum().plot(kind='bar',stacked=True, color=[color_dict.get(x) for x in newdata.columns])
plt.savefig(output, orientation='landscape', bbox_inches="tight")

output2 = 'C:\\Users\\' + username + '\\OneDrive - TRowePrice\\Transaction Router Open Defects by Date-'+ str(datetime.datetime.today().strftime('%Y%m%d')) +'.pdf'
output3 = 'C:\\Users\\' + username + '\\OneDrive - TRowePrice\\User Test Cases by Status-'+ str(datetime.datetime.today().strftime('%Y%m%d')) +'.pdf'
fig, ax = plt.subplots(tight_layout=True)
#plt.figure()
plt.plot(Dates, DefectCount)
plt.xlabel("Date")
plt.ylabel("Number of Open Defects")
ax.set_title("Open Defects by Date")
ax.tick_params(axis='x', rotation=70)
plt.savefig(output2, orientation='landscape')

uniquebus = []
for x in testdf["User Group"]:
    if x not in uniquebus:
        uniquebus.append(x)

for bu in uniquebus:
    fig= plt.figure()
    ax1=fig.add_subplot(111)
    plotdata = testdf[testdf['User Group'].str.contains(bu)]
    plotdata=plotdata.groupby('Transaction Type').sum()
    ax1.legend(["Not Started", "In Progress","Blocked","QA","Accepted"])
    ax1= plotdata.plot(ax=ax1,kind='bar',stacked=True, figsize=(20,10), color=[color_dict.get(x) for x in plotdata.columns], label = ["Not Started", "In Progress","Blocked","QA","Accepted"],title=bu)
    fig.savefig('O:/' + bu + '.pdf', orientation='landscape', bbox_inches="tight")
    plt.close()
#testdf.set_index('User Group', inplace = True, drop = True)
#testdf.groupby('User Group').count().plot(kind='bar', stacked=True, color=[color_dict.get(x) for x in testdf.columns])
#plt.savefig(output3, orientation= 'landscape', bbox_inches='tight')
print(f"Done!  Your ouput has been saved in {output}")
