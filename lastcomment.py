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
start = time.perf_counter()

#Get User credentials for JIRA authorization
username = input('Enter your user name: ')
password = getpass.getpass(prompt="Enter Password")
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})
priority = jira.search_issues('filter = 43915 AND issueFunction in hasComments()')
#datafromjson = requests.get('https://jira.troweprice.com/rest/api/2/search?jql=filter%20%3D%2043915%20AND%20issueFunction%20in%20hasComments()', auth=(username, password)).content
#datafromjson = pd.read_json(datafromjson, typ='series', orient='columns')
#datafromjson = json_normalize(datafromjson['issues'])
class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1
nocomments=[]
string = 'key in ('
idw = ['Ford, Andrew', 'Panchal, Arti', 'Rodens, Joshua', 'Hughes, Kim', 'Brown, Stacy', 'Thomas, Joseph', 'Chaudhari, Tarang', 'Morris, Justin']
for issue in priority:
    key = S(issue.key)
    items = jira.issue(key)
   # item.fields.comments
  #  for item in items:
    results = items.fields.comment.maxResults -1
    #print(items.fields.comment.maxResults)
    c = items.fields.comment.comments[results]
    if S(c.author.displayName) not in idw:
        string = string + key + ','
string = string[:-1]
string=string + ')'
print(string)
jira.update_filter(47923, jql=string)
print('done')
        #print(f"author {c.author.displayName}")
