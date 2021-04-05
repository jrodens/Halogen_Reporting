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

#Get User credentials for JIRA authorization
username = input('Enter your user name: ')
password = getpass.getpass(prompt="Enter Password")
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

#Utilize Jira search function to identify any views on the Analyst board that links to the Halogen View epic
datafromjson = jira.search_issues('project ="HUT"  AND issuetype = Defect', maxResults=1000)
#testcasesfromjson = jira.search_issues('project = "NYCRHT" AND issuetype= "Task" AND status != "Rejected"', maxResults=1000)

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
    transaction = S(issue.fields.customfield_22300)
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
                #print(f'{currentID}:{acceptdate}')
    vardate = datetime.datetime(2020, 2, 12)
    i=-1
    while (acceptdate>=vardate):
        if (vardate < createdate):
            vardate = vardate + datetime.timedelta(1)
            if (datetime.datetime.strftime(vardate, '%A') != 'Saturday') and (datetime.datetime.strftime(vardate, '%A') != 'Sunday'):
                i=i+1
        else:
            if (datetime.datetime.strftime(vardate, '%A') != 'Saturday') and (datetime.datetime.strftime(vardate, '%A') != 'Sunday'):
                DefectCount[i] = DefectCount[i] + 1
                i=i+1
            else:
                pass

            vardate = vardate + datetime.timedelta(1)

print('Finished grabbing data; traisitioning to dataframe')
print(DefectCount)
#open = newdata[(newdata.Status!='Accepted')&(newdata.Status!='Rejected')]


newdata=pd.DataFrame()
newdata.insert(0,"Defects by Transaction Type", Transaction)
newdata.insert(1, "Status", Ticketstatus)
newdata = newdata.replace(to_replace="Open", value="Not Started")
newdata = newdata.replace(to_replace="Dev", value="In Progress")
newdata = newdata.replace(to_replace="Prioritized", value="Not Started")
color_dict = {'Accepted':'#7030A0','Blocked':'#FFC000','In Progress':'#002060','Not Started':'#C00000','QA':'#548235','Rejected':'#808080'}
output = 'C:\\Users\\' + username + '\\OneDrive - TRowePrice\\Halogen Test Metrics-'+ str(datetime.datetime.today().strftime('%Y%m%d')) +'.pdf'

tempdf= pd.DataFrame()
#fig1= plt.figure()

fig2 = plt.figure()
with PdfPages(output) as pdf:


    ax4 = fig2.add_subplot(121)
    ax5 = fig2.add_subplot(122)

    newdata = newdata.groupby(["Defects by Transaction Type", "Status"]).size()
    newdata = newdata.unstack()
    ax4 = newdata.plot(ax = ax4, kind='bar',stacked=True, color=[color_dict.get(x) for x in newdata.columns],label = ["Not Started", "In Progress","Blocked","QA","Accepted"],title="Defects by Transaction and Status")
    for axis in [ax4.yaxis, ax5.yaxis]:
        axis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax4.legend(fontsize='xx-small', frameon=False)
    ax4.set_ylabel("Defect Count", fontsize=6)
    ax4.set_xlabel("Domain", fontsize=6)
    ax4.set_title("Defects by Domain", fontsize=7)
    ax4.tick_params(axis='x', labelsize=5)
    ax4.tick_params(axis='y', labelsize=5)


    ax5 = plt.plot(Dates, DefectCount)
    plt.xlabel("Date",labelpad = 6,fontsize=6)
    plt.ylabel("Number of Open Defects", fontsize=6)
    plt.title("Open Defects by Date",fontsize=7)
    plt.tick_params(axis='x', rotation=70, labelsize=5)
    plt.tick_params(axis='y', labelsize=5)
  #'''  for label in plt.xaxis.get_ticklabels()[::5]:
#         labels.set_visible(False)'''
    fig2.tight_layout()


    pdf.savefig(fig2, orientation='landscape', bbox_inches="tight")

print(f"Done!  Your ouput has been saved at {output}")
