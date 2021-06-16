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
datafromjson = jira.search_issues('project ="Halogen User Testing"  AND issuetype = "View" and "Program (HUT)" = "Data Entitlement"', maxResults=1000)
datafromjson2 = jira.search_issues('project = "Halogen User Testing" AND issuetype = "Defect"', maxResults=1000)

#Class to give a string for comparing strings to string-like variables
class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1
views = pd.DataFrame()
defects = pd.DataFrame()
newdata = pd.DataFrame()
View = []
CurrentStatus = []
CurrentID = []
Program =  []
Group = []
Defectid = []
Defectname = []
Criticality = []
Link = []
DefectStatus=[]
Type = []
print('Getting issues from JIRA')
#Parse the returned JSON
for issue in datafromjson:
    for link in issue.fields.issuelinks:
        if hasattr(link, "outwardIssue"):
            outwardIssue = link.outwardIssue
            if "HUT" in outwardIssue.key:
                Link.append(outwardIssue.key)
                View.append(issue.fields.summary)
                CurrentStatus.append(issue.fields.status)
                CurrentID.append(issue.key)
                Program.append(issue.fields.customfield_25205)
                Group.append(issue.fields.customfield_25000)
        elif hasattr(link, "inwardIssue"):
            inwardIssue = link.inwardIssue
            if "HUT" in inwardIssue.key:
                Link.append(inwardIssue.key)
                View.append(issue.fields.summary)
                CurrentStatus.append(issue.fields.status)
                CurrentID.append(issue.key)
                Program.append(issue.fields.customfield_25205)
                Group.append(issue.fields.customfield_25000)
views.insert(0, "View ID", CurrentID)
views.insert(1, "View Name", View)
views.insert(2, "Program", Program)
views.insert(3, "Status", CurrentStatus)
views.insert(4, "Group", Group)
views.insert(4, "Link", Link)
for issue in datafromjson2:
    Defectid.append(issue.key)
    Defectname.append(issue.fields.summary)
    Criticality.append(issue.fields.customfield_23700)
    DefectStatus.append(issue.fields.status)
    Type.append(issue.fields.customfield_22302)
defects.insert(0, "Defect ID", Defectid)
defects.insert(1, "Name", Defectname)
defects.insert(2, "Criticality", Criticality)
defects.insert(3, "Defect Status", DefectStatus)
defects.insert(4, "Type", Type)
defects.to_excel('C:\\Users\\' + username + '\\OneDrive - TRowePrice\\defects.xlsx', index=False)
views.to_excel('C:\\Users\\' + username + '\\OneDrive - TRowePrice\\views.xlsx', index=False)
newdata = pd.merge(views,defects,how = 'right', left_on='Link', right_on='Defect ID')
#snewdata = newdata.drop(['Link'])
newdata = newdata.sort_values(by=['View ID'])
output = 'C:\\Users\\' + username + '\\OneDrive - TRowePrice\\Halogen_Data.xlsx'
newdata.to_excel(output, index=False)


print("Done!")
