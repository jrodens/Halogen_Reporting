
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
from pandas.tseries.offsets import BDay
from apscheduler.schedulers.blocking import BlockingScheduler
start = time.perf_counter()

#Get User credentials for JIRA authorization
username = input('Enter your user name: ')
password = getpass.getpass(prompt="Enter Password")
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

badList=[]
warningList=[]
def targetdatealert():
    today = datetime.date.today()
    priority = jira.search_issues('filter = 48302')
    for issue in priority:
        currentID = issue.key
        targetdelivery = datetime.datetime.strptime(issue.fields.customfield_21501, '%Y-%m-%d')
        days = np.busday_count(today, targetdelivery.date())
        pointsAvailable = days * 2
        pointsOutstanding = 0
        for link in issue.fields.issuelinks:
            if hasattr(link, "outwardIssue"):
                outwardIssue = link.outwardIssue
                if "NYCIO" in outwardIssue.key:
                    if (outwardIssue.fields.status.name not in 'QA' and outwardIssue.fields.status.name not in 'Accepted' and outwardIssue.fields.status.name not in 'Rejected' and outwardIssue.fields.status.name not in 'Released'):
                        link = jira.issue(outwardIssue.key)
                        if link.fields.customfield_10502 is not None:
                            pointsOutstanding = pointsOutstanding + link.fields.customfield_10502
            elif hasattr(link, "inwardIssue"):
                inwardIssue = link.inwardIssue
                if "NYCIO" in inwardIssue.key:
                    if (inwardIssue.fields.status.name not in 'QA' and inwardIssue.fields.status.name not in 'Accepted' and inwardIssue.fields.status.name not in 'Rejected' and inwardIssue.fields.status.name not in 'Released'):
                        link = jira.issue(inwardIssue.key)
                        if link.fields.customfield_10502 is not None:
                            pointsOutstanding = pointsOutstanding + link.fields.customfield_10502
        print(f'Key: {currentID} Points Available: {pointsAvailable} Points Outstanding: {pointsOutstanding}')
        if (pointsOutstanding > pointsAvailable and currentID not in badList):
            badList.append(currentID)
            files = {
            "message": '<messageML> !!!!ALERT!!!: '+currentID +' is NOT projected to meet delivery date!  Points Outstanding: ' + str(pointsOutstanding)+' Capacity Availble:'+str(pointsAvailable)+' </messageML>'
            }
            url = 'https://prodsymib.troweprice.com/integration/v1/whi/simpleWebHookIntegration/5948074ce4b00855c258bcaa/602ffcc998ace369120dfbc2'
            #print(files)
            r = requests.post(url, files=files,  verify=False)
        if (pointsAvailable > 0 and pointsOutstanding-pointsAvailable > 0 and pointsOutstanding-pointsAvailable < 5 and currentID not in warningList):
            warningList.append(currentID)
            files = {
            "message": '<messageML> Warning: ticket '+currentID +' is at risk for meeting projected delivery date!!!  Points Outstanding: ' + str(pointsOutstanding)+' Capacity Availble:'+str(pointsAvailable)+' </messageML>'
            }
            url = 'https://prodsymib.troweprice.com/integration/v1/whi/simpleWebHookIntegration/5948074ce4b00855c258bcaa/602ffcc998ace369120dfbc2'
            #print(files)
            r = requests.post(url, files=files,  verify=False)
targetdatealert()
scheduler = BlockingScheduler()
scheduler.add_job(targetdatealert, 'interval', minutes=15)
scheduler.start()
