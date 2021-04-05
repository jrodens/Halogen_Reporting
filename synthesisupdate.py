#Determine what status each of the linked attributes for a view is in
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
start = time.perf_counter()

#Get User credentials for JIRA authorization
username = input('Enter your user name: ')
password = getpass.getpass(prompt="Enter Password")
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})
priority = jira.search_issues('filter = 43915 and status in ("Ready For Prioritization", Dev, Blocked, "Needs More Information", "Prioritized") and Synthesis is not EMPTY')
#datafromjson = requests.get('https://jira.troweprice.com/rest/api/2/search?jql=filter%20%3D%2043915%20AND%20issueFunction%20in%20hasComments()', auth=(username, password)).content
#datafromjson = pd.read_json(datafromjson, typ='series', orient='columns')
#datafromjson = json_normalize(datafromjson['issues'])
class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1
earliest = datetime.datetime.today()-BDay(6)
newlist=[]
string = 'key in ('
Key=[]
for issue in priority:
    key = S(issue.key)
    Key.append(key)
    issuefromjson = jira.issue(key, expand='changelog')
    synthesis = issue.fields.customfield_17001[0:6]
    changelog = issuefromjson.changelog
    for history in changelog.histories:
        for item in history.items:
            if (item.field == "Synthesis"):
                date2 = datetime.datetime.strptime(history.created[0:10], '%Y-%m-%d')
                if date2 > earliest:
                    newlist.append(key)
'''
   # synthesis=string(synthesis)
    for i in idw:
        #print(f'{i}:{synthesis}')
        if i in synthesis:
            newlist.append(key)
        else:
            pass
'''
final_list = [i for i in newlist + Key if i not in Key or i not in newlist]
print(final_list)

    #newlist = [x for x in idw if synthesis in x]
for ticket in final_list:
    string = string + ticket + ','
string = string[:-1]
string=string + ')'
print(string)
jira.update_filter(48000, jql=string)
print('done')
        #print(f"author {c.author.displayName}")
