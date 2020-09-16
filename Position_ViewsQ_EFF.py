#Determine what status each of the linked attributes for a view is in
from jira import JIRA
import getpass
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import time
import concurrent.futures
import json
from pandas.io.json import json_normalize
import requests
import urllib.request
from flatten_json import flatten
start = time.perf_counter()

#Get User credentials for JIRA authorization
username = input('Enter your user name: ')
password = getpass.getpass(prompt="Enter Password")
#jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

#Utilize Jira search function to identify any views on the Analyst board that links to the Halogen View epic
print('Getting issues from JIRA')

mylist=[]
datafromjson = requests.get('https://jira.troweprice.com/rest/api/2/search?jql=project%20=%20NYC-RIO-Surge-Halogen-Analysis%20and%20%22Epic%20Link%22%20=%20NYCRSA-993&maxResults=10', auth=(username, password)).content
#datafromjson2 = requests.get('https://jira.troweprice.com/rest/api/2/search?jql=project%20=%20NYC-RIO-Surge-Halogen%20and%20component%20=%20%22Positions%20Domain%22&maxResults=1000', auth=(username, password)).content
#datafromjson=json_normalize(datafromjson)

datafromjson = pd.read_json(datafromjson, typ='series', orient='columns')
#df = json.loads(datafromjson)
datafromjson=json_normalize(datafromjson['issues'],meta=['fields.issuelinks'])



print("Done!")
