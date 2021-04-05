#Determine what status each of the linked attributes for a view is in
from jira import JIRA
import json
import requests
import getpass
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import math
import datetime

#Get User credentials for JIRA authorization
username = input('Enter your user name: ')
password = getpass.getpass(prompt="Enter Password")
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

createdate1 = datetime.datetime(2020, 6, 1)
createdate2 = createdate1 + datetime.timedelta(6)
while(createdate1 <= datetime.datetime.today()):
    cd1= createdate1.strftime("%Y-%m-%d")
    cd2= createdate2.strftime("%Y-%m-%d")
    string = 'project = NYC-IO-Surge-Testing AND ("Projects Impacted" is EMPTY OR "Projects Impacted" in ("IDW 1.0 DE", RIO-RR))  AND status was not in (Accepted, Rejected) on '+cd1 +' AND status was in (Accepted, Rejected) on ' +cd2
    string2 = 'project ="NYC-IO-Surge-Testing"  AND ("Projects Impacted" is EMPTY OR "Projects Impacted" in ("IDW 1.0 DE", "IDW Cutover", RIO-RR, "IDW 1.0 Publications", "BAU (Business as Usual)", "SV MoM")) and "Consumer Application (NYCTT)" = Anova AND status was not in (Accepted, Rejected) on '+cd1 +' AND status was in (Accepted, Rejected) on ' +cd2
    #Utilize Jira search function to identify any views on the Analyst board that links to the Halogen View epic
    datafromjson = jira.search_issues(string, maxResults=1000)
    datafromjson2 = jira.search_issues(string2)

    #Parse the returned JSON
    i=0
    j=0
    for issue in datafromjson:
        i=i+1
    for issue in datafromjson2:
        j=j+1
    print(f"DE Resolved {cd1} - {cd2}: {i}")
    #print(f"ANOVA Resolved {cd1} - {cd2}: {j}")
    createdate1 = createdate1 + datetime.timedelta(7)
    createdate2 = createdate2 + datetime.timedelta(7)
print("Done!")
