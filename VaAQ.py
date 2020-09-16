#Determine what status each of the linked attributes for a view is in
from jira import JIRA
import json
import requests
import getpass
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

#Get User credentials for JIRA authorization
username = input('Enter your user name: ')
password = getpass.getpass(prompt="Enter Password")
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

#Utilize Jira search function to identify any views on the Analyst board that links to the Halogen View epic
datafromjson = jira.search_issues('project = NYC-RIO-Surge-Halogen-Analysis and "Epic Link" = NYCRSA-993', maxResults=1000)

#Class to give a string for comparing strings to string-like variables
class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1
q1 = pd.DataFrame()
q2=pd.DataFrame()
q3= pd.DataFrame()
q4=pd.DataFrame()


Report = []
Attribute=[]
Labels = []
print('Getting issues from JIRA')
#Parse the returned JSON
for issue in datafromjson:
    summ = issue.fields.summary
    currentStatus = issue.fields.status
    currentID = issue.key

    label= issue.fields.labels
    label=S(label)
    #Iterate through each linked item
    for link in issue.fields.issuelinks:
        if hasattr(link, "outwardIssue"):
            outwardIssue = link.outwardIssue
            #Include the NYCRS as a comparison key to ensure we're only returning attributes
            if "NYCRS" in outwardIssue.key and outwardIssue.key[5] != 'A':
                issue = jira.issue(outwardIssue.key)        
        elif hasattr(link, "inwardIssue"):
            inwardIssue = link.inwardIssue
            #Include the NYCRS as a comparison key to ensure we're only returning attributes
            if "NYCRS" in inwardIssue.key and inwardIssue.key[5] != 'A':
                issue = jira.issue(inwardIssue.key)            
    Report.append(summ)
    Attribute.append(issue)
    Labels.append(label)

    #For each view, print the number of open, aceepted, QA, blocked and dev dependencies along with the view name
    #print('{} has {} open items, {} accepted items, {} items in QA, {} blocked and {} in development'.format(summ, openitem, accepted, QA, blocked, dev))

newdata=pd.DataFrame()
newdata.insert(0,"Position View", Report)
newdata.insert(1,"Attribute", Attribute)
newdata.insert(2, "Labels", Labels)

#newdata.to_excel('O:/Position Attribute Data.xlsx')

print('Plotting data')
newdata.set_index('Position View',inplace = True, drop=True)
q1 = newdata[newdata['Labels'].str.contains("Q1")]
q2 = newdata[newdata['Labels'].str.contains("Q2")]
q3 = newdata[newdata['Labels'].str.contains("Q3")]
q4 = newdata[newdata['Labels'].str.contains("Q4")]

q1.to_excel('O:/Q1.xlsx')
q2.to_excel('O:/Q2.xlsx')
q3.to_excel('O:/Q3.xlsx')
q4.to_excel('O:/Q4.xlsx')



print("Done!")
