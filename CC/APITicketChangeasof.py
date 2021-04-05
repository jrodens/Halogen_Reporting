#import libraries
import pandas as pd
from jira import JIRA
import getpass
import datetime
import matplotlib.pyplot as plt
from openpyxl.styles import Alignment
import time
from pandas.io.json import json_normalize


# https://stackoverflow.com/questions/30155353/accessing-transition-history-via-jira-rest-api
start = time.perf_counter()
#setting up lists for entries
#Date after which tickets should be pulled from
newdate = datetime.datetime(2020, 1, 14)


Ticket= []
Status= []
Moved = []
#represents the 9 applications part of the cutover apps for filtered view

statuslookup = ['Accepted']
todaysday = datetime.datetime.today().strftime("%A")

#prompt user for authorization and authorize user
username = input('Enter your user name: ')
password = getpass.getpass(prompt='Enter your password: ')
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

#collect data from JIRA API
temp = jira.search_issues('project = NYC-IO-Surge-Testing  AND "Epic Link" = NYCTT-1026',maxResults=10000)
print(f'Finished in loading datafromjson in {round(time.perf_counter()-start, 2)} seconds')
rightnow = time.perf_counter()
class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1

# get issues in dataset
for issue in temp:
    ticket = issue.key
    status = S(issue.fields.status.name)
    url = 'https://jira.troweprice.com/rest/api/2/issue/' + ticket + '?expand=changelog'
    issuefromjson= jira.issue(ticket, expand='changelog')
    changelog = issuefromjson.changelog
    moved ="N/A"
    tddmoved = "N/A"
    for history in changelog.histories:
        for item in history.items:
            normaldate = datetime.datetime.strptime(history.created[0:10], '%Y-%m-%d')
            if (item.field == "status") & (normaldate >= newdate):
                print(f'{ticket} was moved to {item.toString} on {normaldate}')
                if S(item.toString) in statuslookup:
                    print(f'Ticket {ticket}')
                    moved = str(f'Moved from {item.fromString} to {item.toString}')
                    Moved.append(moved)
                    Ticket.append(ticket)
                    Status.append(status)


print(f'Finished in api call in {round(time.perf_counter()-rightnow, 2)} seconds')
rightnow=time.perf_counter()
newdata=pd.DataFrame()
newdata.insert(0,"Ticket", Ticket)
newdata.insert(1,"Status", Status)
newdata.insert(2,"Moved", moved)


filename = 'C:\\Users\\' + username + '\\OneDrive - TRowePrice\\API Priority1 Ticket Status-'+ str(datetime.datetime.today().strftime('%Y%m%d')) +'.xlsx'
print(f'Finished processing data in {round(time.perf_counter()-rightnow, 2)} seconds')
with pd.ExcelWriter(filename) as writer:
    #writes dataframes to Excel workbook & names worksheets
    newdata.to_excel(writer, index = False,sheet_name='Ticket Detail')
    workbook=writer.book
    worksheet1=writer.sheets['Ticket Detail']
    formater=workbook.add_format({'border':1})
    formater.set_text_wrap()
    formater.set_bg_color('white')
    worksheet1.freeze_panes(1,0)

print(f'Total time of {round(time.perf_counter()-start, 2)} seconds')
print(f'Your report has been saved in {filename}')
print('Done!')
