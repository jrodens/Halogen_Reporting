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
print("starting search")
#datafromjson = jira.search_issues('project ="NYC-RIO-Surge-Halogen" AND issuetype = Task AND status = Accepted and key > "NYCRS-1400"', maxResults=800)


#Class to give a string for comparing strings to string-like variables
class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1

print('Getting issues from JIRA')
#Parse the returned JSON

d1=[]
d2=[]
df = pd.read_excel('O:/Completedattributes.xlsx')
frame = pd.DataFrame()
for index,row in df.iterrows():
    currentID = df.iloc[index,0]
    issuefromjson = jira.issue(currentID, expand='changelog')
    changelog = issuefromjson.changelog
    #createdate = datetime.datetime.strptime(issuefromjson.fields.created[0:10], '%Y-%m-%d')
    for history in changelog.histories:
        for item in history.items:
            dated = datetime.datetime.strptime(history.created[0:10], '%Y-%m-%d')
            if (item.field == "status") & ((S(item.toString) == "Accepted")):
                print(f'{currentID}  :  {dated}')
                d1.append(currentID)
                d2.append(dated)

frame.insert(0,"ID", d1)
frame.insert(1,"Accepted On", d2)
frame.to_excel('O:/AttributesbyAcceptDateExcel.xlsx', index=False)
print(f"Done!")
