
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
from PIL import Image, ImageFont, ImageDraw
import textwrap
from apscheduler.schedulers.blocking import BlockingScheduler
import ast

projects = (("IDW 1.0", "NYCIO", '390', 'NYC-IO-Surge'), ("Hadron", "IDWH", '900', 'IDW 2.0 - Hadron - Meson'), ("Halogen Analysis", "NYCRSA", '512', 'NYC-RIO-Surge-Halogen-Analysis'), ("Halogen Development", "NYCRS",'490', 'NYC-RIO-Surge-Halogen-Board'))

username = input('Enter your user name: ')
password = getpass.getpass(prompt="Enter Password")
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1


#removed_from_sprint = pd.DataFrame()
#added_to_sprint = pd.DataFrame()
'''
def SprintReview(data1):

        wrong_points = jira.search_issues('project = ' + projects[1] + 'AND sprint in openSprints() and ("Story Points" is EMPTY or "Story Points" not in  (1,2,3,5,8)')
        added_to_sprint = jira.search_issues('project = ' + projects[1] + 'AND sprint in openSprints()')
        for issue in added_to_sprint:
            currentID = issue.key
            added_details = jira.issue(currentID, expand='changelog')
            changelog = added_details.changelog
            for history in added_details.histories:
                for item in history.items:
                    if (item.field == "Sprint" and item.to == data1['id'] and datetime.datetime.strptime(history.created[0:10], '%Y-%m-%d') > datetime.datetime.strptime(sprint['startDate'][0:10], '%Y-%m-%d')):
                        print(item)
                    elif (item.field == "Sprint" and item.from == data1['id'] and datetime.datetime.strptime(history.created[0:10], '%Y-%m-%d') > datetime.datetime.strptime(sprint['startDate'][0:10], '%Y-%m-%d')):
                        print(item)
'''
#def GetSprint():
    #Finds the open sprint on each board
for index, project in enumerate(projects):
    Removed = pd.DataFrame()
    Added = pd.DataFrame()
    Wrong = pd.DataFrame()
    id = []
    component = []
    epic = []
    milestone = []
    assignee = []
    epic = []
    status = []
    getsprint = jira.sprints(project[2])
    wrong_points = jira.search_issues('project = ' + project[1] + ' AND sprint in openSprints() and ("Story Points" is EMPTY or "Story Points" not in  (1,2,3,5,8))')
    #print('project = ' + project[1] + ' AND sprint in openSprints()')
    for sprint in getsprint:
        url = 'https://jira.troweprice.com/rest/agile/1.0/sprint/' + str(sprint.id)
        data1 = requests.get(url, auth=(username,password)).content
        data1 = data1.decode("utf-8")
        data1 = ast.literal_eval(data1)
        if data1['state'] == 'active':
            data = data1
            break
    #added_to_sprint = jira.search_issues('project = ' + project[1] + ' AND sprint in openSprints()')
    #print(added_to_sprint)
    string = "project = " + project[1] + " and issueFunction in removedAfterSprintStart('" + project[3] + "', '" + data['name'] + "')"
    string2 = "project = " + project[1] + " and issueFunction in addedAfterSprintStart('" + project[3] + "', '" + data['name'] + "')"
    removed_from_sprint = jira.search_issues(string)
    added_to_sprint = jira.search_issues(string2)
    for issue in removed_from_sprint:
        id.append(issue.key)
        epic.append(issue.fields.customfield_10506)
        assignee.append(issue.fields.assignee.displayName)
        status.append(issue.fields.status.name)
    #q1.insert(0,"Story",Item)
    Removed.insert(0, "ID", id)
    Removed.insert(1, "Epic", epic)
    Removed.insert(2, "Assignee", assignee)
    Removed.insert(3, "Status", status)
    for issue in added_to_sprint:
        id.append(issue.key)
        epic.append(issue.fields.customfield_10506)
        assignee.append(issue.fields.assignee.displayName)
        status.append(issue.fields.status.name)
    Added.insert(0, "ID", id)
    Added.insert(1, "Epic", epic)
    Added.insert(2, "Assignee", assignee)
    Added.insert(3, "Status", status)
Halogen_Added = Added[Added['ID'].str.contains("NYCRS")]
Hadron_Added = Added[Added['ID'].str.contains("IDWH")]
IDW_Added = Added[Added['ID'].str.contains("NYCIO")]
Halogen_Removed = Removed[Removed['ID'].str.contains("NYCRS")]
Hadron_Removed = Removed[Removed['ID'].str.contains("IDWH")]
IDW_Removed = Removed[Removed['ID'].str.contains("NYCIO")]
'''
    if project[1]== "NYCIO":
        for issue in removed_from_sprint:
            id.append(issue.key)
            epic.append(issue.fields.customfield_10506)
            assignee.append(issue.fields.assignee.displayName)
            status.append(issue.fields.status.name)
        #q1.insert(0,"Story",Item)
        Removed.insert(0, "ID", id)
        Removed.insert(1, "Epic", epic)
        Removed.insert(2, "Assignee", assignee)
        Removed.insert(3, "Status", status)
        for issue in added_to_sprint:
            id.append(issue.key)
            epic.append(issue.fields.customfield_10506)
            assignee.append(issue.fields.assignee.displayName)
            status.append(issue.fields.status.name)
        Added.insert(0, "ID", id)
        Added.insert(1, "Epic", epic)
        Added.insert(2, "Assignee", assignee)
        Added.insert(3, "Status", status)
        fig, ax =plt.subplots(figsize=(12,4))
        ax.axis('tight')
        ax.axis('off')
        the_table = ax.table(cellText=Added.values, colLabels=Added.columns, loc='center')
        pp = PdfPages("O:/Added.pdf")
        pp.savefig(fig, bbox_inches='tight')
        pp.close()
        '''
'''
    if project[1]== "IDWH":
        for issue in removed_from _sprint:
    if project[1] =="NYCRS" or project[1]== "NYCRSA":
        for issue in removed_from _sprint:

    for issue in added_to_sprint:
        currentID = issue.key
        added_details = jira.issue(currentID, expand='changelog')
        changelog = added_details.changelog
        for history in changelog.histories:
            for item in history.items:
                if (item.field == "Sprint" and item.to == data1['id'] and datetime.datetime.strptime((history.created[0:10], '%Y-%m-%d') > datetime.datetime.strptime(sprint['startDate'][0:10], '%Y-%m-%d'))):
                    print(item)
                if ((item.field == "Sprint") and (item.fromString == data1['name']) and (datetime.datetime.strptime(history.created[0:10], '%Y-%m-%d') > datetime.datetime.strptime(sprint['startDate'][0:10], '%Y-%m-%d'))):
                    print(item)
    '''
#GetSprint()
