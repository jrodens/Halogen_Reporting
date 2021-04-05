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
datafromjson = jira.search_issues('project = NYC-IO-Surge-Testing and "Consumer Application (NYCTT)" = lens', maxResults=1000)

class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1
today = datetime.datetime.today()
hinet = pd.DataFrame()
Open=[]
Intriage=[]
RFP=[]
Dev=[]
QAfail=[]
QA=[]
Blocked=[]
Needinfo=[]
Prioritized=[]
Ticket=[]
Service = []
Source =[]
Consumer = []
Project = []
for issue in datafromjson:
    currentID = issue.key
    status = S(issue.fields.status)
    issuefromjson = jira.issue(currentID, expand='changelog')
    changelog = issuefromjson.changelog
    date1 = datetime.datetime.strptime(issue.fields.created[0:10], '%Y-%m-%d')
    #service = issue.fields.customfield_21800.value
    #consumer = issue.fields.customfield_23201.value
    #project = issue.fields.customfield_21202.value
    project = issue.fields.customfield_10506
    timeopen = 0
    open = 0
    intriage = 0
    rfp = 0
    dev = 0
    qafail = 0
    qa = 0
    blocked = 0
    needinfo = 0
    prioritized = 0
    for history in changelog.histories:
        for item in history.items:
            if (item.field == "status"):
                date2 = datetime.datetime.strptime(history.created[0:10], '%Y-%m-%d')
                timeopen = date2-date1
                if S(item.fromString) == 'Open':
                    open =  open + timeopen.days
                if S(item.fromString) == 'In Triage':
                    intriage = intriage + timeopen.days
                if S(item.fromString) == 'Ready For Prioritization':
                    rfp = rfp+  timeopen.days
                if S(item.fromString) == 'Dev':
                    dev = dev + timeopen.days
                if S(item.fromString) == 'QA Failed':
                    qafail =  qafail + timeopen.days
                if S(item.fromString) == 'QA':
                    qa = qa + timeopen.days
                if S(item.fromString) == 'Blocked':
                    blocked = blocked + timeopen.days
                if S(item.fromString) == 'Needs more Info':
                    needinfo += timeopen.days
                if S(item.fromString) == 'Prioritized':
                    prioritized += timeopen.days
                date1=date2
    if status != 'Accepted' and status != 'Rejected':
        timeopen = today-date1
        if status == 'Open':
            open =  open + timeopen.days
        if status == 'In Triage':
            intriage = intriage + timeopen.days
        if status == 'Ready For Prioritization':
            rfp = rfp+  timeopen.days
        if status == 'Dev':
            dev = dev + timeopen.days
        if status == 'QA Failed':
            qafail =  qafail + timeopen.days
        if status == 'QA':
            qa = qa + timeopen.days
        if status == 'Blocked':
            blocked = blocked + timeopen.days
        if status == 'Needs More Information':
            needinfo += timeopen.days
        if status == 'Prioritized':
            prioritized += timeopen.days
    Open.append(open)
    Intriage.append(intriage)
    RFP.append(rfp)
    Dev.append(dev)
    QAfail.append(qafail)
    QA.append(qa)
    Blocked.append(blocked)
    Needinfo.append(needinfo)
    Prioritized.append(prioritized)
    Ticket.append(currentID)
    #Service.append(service)
    #Consumer.append(consumer)
    Project.append(project)
hinet.insert(0, "Ticket", Ticket)
hinet.insert(1, "Open", Open)
hinet.insert(2, "In Triage", Intriage)
hinet.insert(3, "Ready for Prioritization", RFP)
hinet.insert(4,"Prioritized", Prioritized)
hinet.insert(5,"Development", Dev)
hinet.insert(6,"QA", QA)
hinet.insert(7,"QA Failed", QAfail)
hinet.insert(8,"Blocked", Blocked)
hinet.insert(9,"Need More Information", Needinfo)
#hinet.insert(10,"Service", Service)
#hinet.insert(11,"Consumer", Consumer)
hinet.insert(10,"Project", Project)
hinet.to_excel('O:/timespent.xlsx')
print("Done!  Your ouput has been saved at {output}")
