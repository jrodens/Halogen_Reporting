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

starttimetoload= time.perf_counter()
#Utilize Jira search function to identify any views on the Analyst board that links to the Halogen View epic
datafromjson = jira.search_issues('project = NYC-IO-Surge-Testing and status != "Accepted" and status != "Rejected"', maxResults=2000)
finishtimetoload= time.perf_counter()
print(f'Finished in loading datafromjson in {round(finishtimetoload-starttimetoload, 2)} seconds')
now = time.perf_counter()
print(f'Finished in loading datafromjson2 in {round(now-finishtimetoload, 2)} seconds')
print(f'Finished in loading data in {round(now-starttimetoload, 2)} seconds')


#Class to give a string for comparing strings to string-like variables
class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1

newdata=pd.DataFrame()
Labels = []
Summary = []
Service = []
Item=[]
Status=[]
#Parse the returned JSON
for issue in datafromjson:
    summ = issue.fields.summary
    Status.append(S(issue.fields.status))
    currentID = issue.key
    service = S(issue.fields.customfield_21800)
    Service.append(service)


newdata.insert(0,"Service",Service)
newdata.insert(1,"Status",Status)


#data cleans: drop not needed fields and align statuses

newdata=newdata.replace(to_replace="Prioritized", value="Not Started")
newdata=newdata.replace(to_replace="Open", value="Not Started")
newdata=newdata.replace(to_replace="Ready For Prioritization", value= "Not Started")
newdata=newdata.replace(to_replace="Dev", value="In Development")
newdata=newdata.replace(to_replace="In Triage", value="Not Started")
newdata=newdata.replace(to_replace="QA Failed", value="QA")
newdata = newdata[(newdata.Service!='None')]
newdata.to_excel('O:/TicketsbyService.xlsx')
newdata = newdata.groupby(['Service','Status']).size()

color_dict = {'Accepted':'#7030A0','Blocked':'#FFC000','In Development':'#002060','Not Started':'#C00000','QA':'#548235','Rejected':'#808080'}
output = 'C:\\Users\\' + username + '\\OneDrive - TRowePrice\\Consumer Tickets by Service -'+ str(datetime.datetime.today().strftime('%Y%m%d')) +'.pdf'
pdf = PdfPages(output)
fig1 = plt.figure()

with PdfPages(output) as pdf:
    ax1=fig1.add_subplot(111)
    newdata=newdata.unstack()
    newdata.plot(ax=ax1,kind='bar',stacked=True, figsize=(20,10),color=[color_dict.get(x) for x in newdata.columns], title="Consumer Tickets by Service")

    pdf.savefig(fig1, orientation='landscape', bbox_inches="tight")

print(f'Total time: {round(time.perf_counter()-start, 2)} seconds')
print(f'Your pdf has been saved in {output}')
print("Done!")
