#Determine what status each of the linked attributes for a view is in
from jira import JIRA
import json
import requests
import getpass
import pandas as pd
import matplotlib.pyplot as plt

#Get User credentials for JIRA authorization
username = input('Enter your user name: ')
password = getpass.getpass(prompt="Enter Password")
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

#Utilize Jira search function to identify any views on the Analyst board that links to the Halogen View epic
datafromjson = jira.search_issues('project = NYC-RIO-Surge-Halogen and component = "Positions Domain" and status != Rejected', fields = "key, issuelinks",maxResults=10000)

#Class to give a string for comparing strings to string-like variables
class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1
missing=[]
print('Getting issues from JIRA')
#Parse the returned JSON
for issue in datafromjson:
    currentID = issue.key
    #Iterate through each linked item
    for link in issue.fields.issuelinks:
        print("issuelinks: ",issue.fields.issuelinks)
        if hasattr(link, "outwardIssue"):
            outwardIssue = link.outwardIssue
            outwardIssue = S(outwardIssue)
            print(outwardIssue)
            #Include the NYCRS as a comparison key to ensure we're only returning attributes
            if "NYCRSA" in outwardIssue :
                pass
        elif hasattr(link, "inwardIssue"):
            inwardIssue = link.inwardIssue
            inwardIssue = S(inwardIssue)
            #Include the NYCRS as a comparison key to ensure we're only returning attributes
            print(inwardIssue)
            if "NYCRSA" in inwardIssue:
                pass
        else:
            missing.append(currentID)
newdata=pd.DataFrame()
newdata.insert(0,"Attributes not linked to views", missing)
newdata.to_excel('O:/Position Attribute Data.xlsx', index=False)
print("Done!")
