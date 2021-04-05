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

start = time.perf_counter()
'''
The design of this report is to take two data sets, the attributes on the dev board (nycrs) and the views on the analysis board (nycrsa) and joining the two together.
The result is aggergated and sized by quartile for graphing within a pdf
'''
#Get User credentials for JIRA authorization
username = input('Enter your user name: ')
password = getpass.getpass(prompt="Enter Password")
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})
versions = jira.project_versions('IDWH')
for milestone in versions:
    print(milestone)
    print(jira.version(milestone.id))
