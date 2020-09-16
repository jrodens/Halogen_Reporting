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
import matplotlib.ticker as ticker
from matplotlib.dates import DateFormatter

#Get User credentials for JIRA authorization
username = input('Enter your user name: ')
password = getpass.getpass(prompt="Enter Password")
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

#Utilize Jira search function to identify any views on the Analyst board that links to the Halogen View epic
datafromjson = jira.search_issues('project ="NYC-RIO-Surge-Transaction-Router-Testing"  AND issuetype = Defect', maxResults=1000)
testcasesfromjson = jira.search_issues('project = "NYCRSTRT" AND issuetype= "Story" AND status != "Rejected" AND "Epic Link" = NYCRSTRT-147', maxResults=1000)

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

History = pd.DataFrame()
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
    if "IL" in labels:
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
    TestStatus.append(currentStatus)
testdf.insert(0, "User Group", Group)
testdf.insert(1, "Transaction Type", Transtype)
testdf.insert(2, "Status", TestStatus)
testdf = testdf.replace(to_replace="Open", value="Not Started")
testdf = testdf.replace(to_replace="Dev", value="In Progress")
testdf = testdf.replace(to_replace="None", value= "Non-Transaction Type*")

todaysdate = datetime.datetime.now()
yesterday = todaysdate - datetime.timedelta(1)
while (startdate <= yesterday):
    startdate = startdate + datetime.timedelta(1)
    if (datetime.datetime.strftime(startdate, '%A') != 'Saturday') and (datetime.datetime.strftime(startdate, '%A') != 'Sunday'):
        Dates.append(datetime.datetime.strftime(startdate, '%Y-%m-%d'))
        DefectCount.append(0)

print('Getting issues from JIRA')
#Parse the returned JSON
Ticketstatus=[]
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
    Ticketstatus.append(currentStatus)
    if blocked == 0 and dev == 0 and QA == 0 and openitem == 0:
        Readyviews.append(summ)
    elif dev == 0 and QA == 0 and openitem == 0 and blocked > 0:
        BlockedReports.append(summ)
    elif dev == 0 and QA == 0 and accepted == 0 and openitem > 0:
        Notstarted.append(summ)
    elif openitem > 0 and blocked == 0:
        Inprog.append(summ)

    issuefromjson = jira.issue(currentID, expand='changelog')
    changelog = issuefromjson.changelog
    createdate = datetime.datetime.strptime(issue.fields.created[0:10], '%Y-%m-%d')
    acceptdate =  startdate
    for history in changelog.histories:
        for item in history.items:
            dated = datetime.datetime.strptime(history.created[0:10], '%Y-%m-%d')
            if (item.field == "status") & ((S(item.toString) == "Accepted") or (S(item.toString) == "Rejected")):
                acceptdate = dated
    vardate = datetime.datetime(2020, 2, 12)
    i=-1
    while (acceptdate>=vardate):
        if (vardate < createdate):
            vardate = vardate + datetime.timedelta(1)
            if (datetime.datetime.strftime(vardate, '%A') != 'Saturday') and (datetime.datetime.strftime(vardate, '%A') != 'Sunday'):
                i=i+1
        else:
            if (datetime.datetime.strftime(vardate, '%A') != 'Saturday') and (datetime.datetime.strftime(vardate, '%A') != 'Sunday'):
                #print(f'{currentID},{vardate}')
                DefectCount[i] = DefectCount[i] + 1
                i=i+1
            else:
                pass

            vardate = vardate + datetime.timedelta(1)

print('Finished grabbing data; traisitioning to dataframe')
#open = newdata[(newdata.Status!='Accepted')&(newdata.Status!='Rejected')]

metricsdf = pd.DataFrame()
metricsdf = testdf[testdf['Status']=='Accepted']
print('Accepted:')
print(metricsdf.groupby(['User Group']).size())
print("")

metricsdf = pd.DataFrame()
metricsdf = testdf[testdf['Status']=='Blocked']
print('Blocked:')
print(metricsdf.groupby(['User Group']).size())
print("")

metricsdf = pd.DataFrame()
metricsdf=testdf
print('Total:')
print(metricsdf.groupby(['User Group']).size())
print("")

newdata=pd.DataFrame()
newdata.insert(0,"Defects by Transaction Type", Transaction)
newdata.insert(1, "Status", Ticketstatus)
newdata = newdata.replace(to_replace="Open", value="Not Started")
newdata = newdata.replace(to_replace="Dev", value="In Progress")
newdata = newdata.replace(to_replace="Prioritized", value="Not Started")
color_dict = {'Accepted':'#7030A0','Blocked':'#FFC000','In Progress':'#002060','Not Started':'#C00000','QA':'#548235','Rejected':'#808080'}
output = 'C:\\Users\\' + username + '\\OneDrive - TRowePrice\\Transaction Router User Functionality Test Metrics-'+ str(datetime.datetime.today().strftime('%Y%m%d')) +'.pdf'

tempdf= pd.DataFrame()
#fig1= plt.figure()
fig1, (ax1,ax2,ax3) = plt.subplots(1,3, sharey=True, sharex= False)
fig2 = plt.figure()
fig3 = plt.figure()
with PdfPages(output) as pdf:
    tempdf = testdf[testdf['User Group'].str.contains("Post Trade Services")]
    tempdf = tempdf.groupby(["Transaction Type", "Status"]).size()
    tempdf =tempdf.unstack()
    ax1= tempdf.plot(ax=ax1,kind='bar',stacked=True, figsize=(20,10), color=[color_dict.get(x) for x in tempdf.columns], label = ["Not Started", "In Progress","Blocked","QA","Accepted"],title="Post Trade Services")
    ax1.set_ylabel("Test Case Count")
    ax1.legend(frameon = False)
    ax1.set_xlabel("")
    ax1.text(0, -4.1, "* Non-transaction type items are not correlated with a single transaction type (i.e. UI test cases)", fontsize = 6.5)
    tempdf = testdf[testdf['User Group'].str.contains("Investment Liaisons")]
    tempdf = tempdf.groupby(["Transaction Type", "Status"]).size()
    tempdf =tempdf.unstack()
    fig1.text(0.5,0.02,'Transaction Type', ha='center', fontsize=12)

    ax2= tempdf.plot(ax=ax2,kind='bar',stacked=True, figsize=(20,10), color=[color_dict.get(x) for x in tempdf.columns], label = ["Not Started", "In Progress","Blocked","QA","Accepted"],title="Investment Liaisons")
    ax2.legend(frameon=False)
    ax2.set_xlabel("")
    tempdf = testdf[testdf['User Group'].str.contains("Fund Accounting Operations")]
    tempdf = tempdf.groupby(["Transaction Type", "Status"]).size()
    tempdf =tempdf.unstack()
    ax3= tempdf.plot(ax=ax3, kind='bar',stacked=True, figsize=(20,10), color=[color_dict.get(x) for x in tempdf.columns], label = ["Not Started", "In Progress","Blocked","QA","Accepted"],title="Fund Accounting Operations")
    ax3.legend(frameon=False)
    ax3.set_xlabel("")
    fig1.suptitle("Test Case Status by Business Unit", fontsize=14, y=1.05, fontweight='bold')
    fig1.tight_layout()

    ax4 = fig2.add_subplot(111)
    ax5 = fig3.add_subplot(111)

    newdata = newdata.groupby(["Defects by Transaction Type", "Status"]).size()
    newdata = newdata.unstack()
    ax4 = newdata.plot(ax = ax4, kind='bar',stacked=True, color=[color_dict.get(x) for x in newdata.columns],label = ["Not Started", "In Progress","Blocked","QA","Accepted"],title="Defects by Transaction and Status")
    for axis in [ax4.xaxis, ax4.yaxis]:
        axis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax4.legend(fontsize='xx-small', frameon=False)
    ax4.set_ylabel("Defect Count", fontsize=6)
    ax4.set_xlabel("Transaction Type", fontsize=6)
    ax4.set_title("Defects by Transaction Type", fontsize=7)
    ax4.tick_params(axis='x', labelsize=5)
    ax4.tick_params(axis='y', labelsize=5)

    ax5 = plt.plot(ax=ax5, Dates, DefectCount)
    plt.xlabel("Date",labelpad = 23,fontsize=6)
    plt.ylabel("Number of Open Defects", fontsize=6)
    plt.title("Open Defects by Date",fontsize=7)
    plt.tick_params(axis='x', rotation=70, labelsize=5)
    plt.tick_params(axis='y', labelsize=5)
    #date_form = DateFormatter("%m-%d")
    for axis in [ax5.xaxis]:
        axis.set_major_formatter(date_form)
        axis.set_major_locator(mdates.WeekdayLocator(interval=1))
    #for label in ax5.xaxis.get_ticklabels()[::3]:
    #    label.set_visible(False)
    #ax5.xaxis.set_major_locator(plt.MaxNLocator(10))
    fig2.tight_layout()

    pdf.savefig(fig1, orientation='landscape', bbox_inches="tight")
    pdf.savefig(fig2, orientation='landscape', bbox_inches="tight")
    pdf.savefig(fig3, orientation='landscape', bbox_inches="tight")
print(f"Done!  Your ouput has been saved at {output}")
