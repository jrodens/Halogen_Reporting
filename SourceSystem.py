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
datafromjson = jira.search_issues('project = NYC-IO-Surge-Testing AND (issueFunction in linkedIssuesOf("project=eag") OR summary ~ HiNet OR Summary ~ Eagle) AND status != Rejected AND created > startOfYear()', maxResults=1000)
datafromjson2= jira.search_issues('project = NYC-IO-Surge-Testing AND (issueFunction in linkedIssuesOf("project=ihcc") OR summary ~ HiNet OR Summary ~ Eagle) AND status != Rejected AND created > startOfYear()', maxResults=1000)
datafromjson3= jira.search_issues('project = NYC-IO-Surge-Testing AND not (issueFunction in linkedIssuesOf("project=EAG") OR issueFunction in linkedIssuesOf("project=IHCC") OR summary ~ HiNet OR Summary ~ Eagle) AND status != Rejected AND created > startOfYear()', maxResults=1000)
#testcasesfromjson = jira.search_issues('project = "NYCRHT" AND issuetype= "Task" AND status != "Rejected"', maxResults=1000)

#Class to give a string for comparing strings to string-like variables
class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1

eagle = pd.DataFrame()
hinet = pd.DataFrame()
Ticket = []
Failed = []
print('Eagle')
acceptdate = datetime.datetime(2020, 1, 1)
for issue in datafromjson:
    currentID = issue.key
    issuefromjson = jira.issue(currentID, expand='changelog')
    changelog = issuefromjson.changelog
    failed = 0
    timeopen=0
    createdate = datetime.datetime.strptime(issue.fields.created[0:10], '%Y-%m-%d')
    for history in changelog.histories:
        for item in history.items:
            if (item.field == "status") & ((S(item.toString) =="Accepted")):
                acceptdate = datetime.datetime.strptime(history.created[0:10], '%Y-%m-%d')
                timeopen = acceptdate-createdate
            if (item.field == "status") & ((S(item.toString) == "QA Failed")):
                failed += 1
    print(f'{currentID}, {failed}, Eagle, {timeopen}')
    Ticket.append(currentID)
    Failed.append(failed)

    #eagle.insert(0,"Key", Ticket)
    #eagle.insert(1, "Failed", Failed)
print('HiNet')
for issue in datafromjson2:
    currentID = issue.key
    issuefromjson = jira.issue(currentID, expand='changelog')
    changelog = issuefromjson.changelog
    createdate = datetime.datetime.strptime(issue.fields.created[0:10], '%Y-%m-%d')
    failed = 0
    timeopen = 0
    for history in changelog.histories:
        for item in history.items:
            if (item.field == "status") & ((S(item.toString) =="Accepted")):
                acceptdate = datetime.datetime.strptime(history.created[0:10], '%Y-%m-%d')
                timeopen = acceptdate-createdate
            if (item.field == "status") & ((S(item.toString) == "QA Failed")):
                failed += 1
    print(f'{currentID}, {failed}, HiNet, {timeopen}')
    Ticket.append(currentID)
    Failed.append(failed)
print('IDW')
for issue in datafromjson3:
    currentID = issue.key
    issuefromjson = jira.issue(currentID, expand='changelog')
    changelog = issuefromjson.changelog
    createdate = datetime.datetime.strptime(issue.fields.created[0:10], '%Y-%m-%d')
    failed = 0
    for history in changelog.histories:
        for item in history.items:
            if (item.field == "status") & ((S(item.toString) =="Accepted")):
                acceptdate = datetime.datetime.strptime(history.created[0:10], '%Y-%m-%d')
                timeopen = acceptdate-createdate
            if (item.field == "status") & ((S(item.toString) == "QA Failed")):
                failed += 1
    print(f'{currentID}, {failed}, IDW, {timeopen}')
    Ticket.append(currentID)
    Failed.append(failed)
    #hinet.insert(0,"Key", Ticket)
    #hinet.insert(1, "Failed", Failed)

#eagle.to_excel('O:/eagle.xlsx')
#hinet.to_excel('O:/hinet.xlsx')


print("Done!  Your ouput has been saved at {output}")
