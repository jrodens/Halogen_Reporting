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
Application= []
Ticket= []
Status= []
new_row = []
Age = []
Summary = []
Synthesis =[]
Projects_Impacted = []
TDD = []
Labels=[]
Service = []
Component=[]
Linked = []
Criticality = []
now = datetime.datetime.now()
countopen=0
countdev=0
countqa=0
countaccepted=0
Moved = []
Tddmoved = []
#represents the 9 applications part of the cutover apps for filtered view
cutoverapps = ['Broadridge', 'Cougar', 'FID', 'Falcon', 'Nucleus', 'Perform', 'COIL', 'Cash Forecasting Database', 'Equity Quant', 'Hedgehog']

todaysday = datetime.datetime.today().strftime("%A")
'''
if todaysday == 'Monday':
    lastrun = now - datetime.timedelta(3)
elif todaysday == 'Tuesday':
    lastrun = now - datetime.timedelta(1)
elif todaysday == 'Wednesday':
    lastrun = now - datetime.timedelta(2)
elif todaysday == 'Thursday':
    lastrun = now - datetime.timedelta(1)
elif todaysday == 'Friday':
    lastrun = now - datetime.timedelta(2)
elif todaysday == 'Saturday':
    lastrun = now - datetime.timedelta(1)
elif todaysday == 'Sunday':
    lastrun = now - datetime.timedelta(2)
else:
    print('error')
'''
lastrun = now - datetime.timedelta(4)
#print(lastrun)
#prompt user for authorization and authorize user
username = input('Enter your user name: ')
password = getpass.getpass(prompt='Enter your password: ')
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

#collect data from JIRA API
temp = jira.search_issues('project = NYCRS AND "Epic Link" = NYCRS-553 AND issuetype = Task AND component = "Positions Domain"',maxResults=10000)
#temp = pd.DataFrame.from_dict(datafromjson)

#temp.to_excel('O:/apidf.xlsx')
#temp = pd.read_json(datafromjson,typ='series', orient='columns')
#temp=json_normalize(temp['issues'],meta=['fields.key'])
#temp.to_excel('O:/apidf.xlsx')
print(f'Finished in loading datafromjson in {round(time.perf_counter()-start, 2)} seconds')
rightnow = time.perf_counter()
#Class is used to make comparissons against non-string variables such as the object presented here
class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1

# get issues in dataset
for issue in temp:
    #print(f'The issue is : {issue}')
    ticket = issue.key
    #print(f'The ticket is : {ticket}')
    status = S(issue.fields.status.name)
    #synthesis = issue.fields.customfield_17001
#    age = now - datetime.datetime.strptime(temp.fields.created[0:10], '%Y-%m-%d')
    summary = issue.fields.summary


    url = 'https://jira.troweprice.com/rest/api/2/issue/' + ticket + '?expand=changelog'
    issuefromjson= jira.issue(ticket, expand='changelog')
    changelog = issuefromjson.changelog
    #issuefromjson = requests.get(url, auth=(username, password)).content
    moved ="N/A"

    for history in changelog.histories:
        for item in history.items:
            normaldate = datetime.datetime.strptime(history.created[0:10], '%Y-%m-%d')
            #print(normaldate)
            check = normaldate-lastrun
            #print(check)
            if (normaldate >= lastrun):
                #print(f'Ticket {ticket} was moved from {item.fromString} to {item.toString} on {normaldate}')
                #moved = moved + str(f'Moved from {item.fromString} to {item.toString}')
                #print(moved)
                moved = str(f'Moved from {item.fromString} to {item.toString}')
                #print (item.toString) # new value
                #print (item.fromString) # old value

    if issue.fields.customfield_23201 is None:
        pass
    else:


        Ticket.append(ticket)
        Status.append(status)
        #Age.append(age.days)
        Summary.append(summary)


        Labels.append(labels)


        Moved.append(moved)


print(f'Finished in api call in {round(time.perf_counter()-rightnow, 2)} seconds')
rightnow=time.perf_counter()
newdata=pd.DataFrame()
newdata.insert(0,"Ticket", Ticket)
newdata.insert(1,"Status", Status)

#newdata.insert(5,"Criticality", Criticality)
newdata.insert(2,"Status Changed To", Moved)

newdata.to_excel('O:/Halogenitems.xlsx')
'''
#newdata=newdata.loc[newdata['Application'].isin(cutoverapps)]
#newdata.explode('Projects Impacted')
#newdata.insert(10, "Dev Ticket", Linked)


open = newdata[(newdata.Status!='Accepted')&(newdata.Status!='Rejected')]
rejected = newdata[newdata.Status=='Rejected']
accepted = newdata[newdata.Status=='Accepted']
summary = newdata[(newdata.Status!='Rejected')]
#summary=summary.replace(to_replace="Dev", value="Open")
summary=summary.replace(to_replace="Ready For Prioritization", value="Open and Triage")
#summary=summary.replace(to_replace="Blocked", value="Open and Triage")
summary=summary.replace(to_replace="Open", value="Open and Triage")
summary=summary.replace(to_replace="QA Failed", value="QA")
summary=summary.replace(to_replace="Prioritized", value="Open and Triage")
summary=summary.replace(to_replace="In Triage", value="Open and Triage")
summary=summary.replace(to_replace="Needs Information", value="Open and Triage")
#summary= summary.replace(to_replace="Dev", value="Open and Triage")
open=open.sort_values(by=['Application'], ascending=[True])
rejected=rejected.sort_values(by=['Application'], ascending=[True])
accepted=accepted.sort_values(by=['Application'], ascending=[True])
summary = summary.groupby(['Status','Application']).size()
summary = summary.unstack()
summary = summary.fillna(0)
summary = summary.transpose()
openlength = len(open.index) + 1
summlength= len(summary.index) + 1
openlength = str(openlength)
summlength = str(summlength)
#summaryaccepted = accepted.groupby(['Criticality', 'Application']).size()
#summaryopen.join(summaryaccepted)

#filename ='O:\Investment API Daily Ticket Metrics -' + str(datetime.datetime.today().strftime('%Y%m%d')) +'.xlsx'
filename = 'C:\\Users\\' + username + '\\OneDrive - TRowePrice\\API Priority1 Ticket Status-'+ str(datetime.datetime.today().strftime('%Y%m%d')) +'.xlsx'
'''
'''
#print(f'Finished processing data in {round(time.perf_counter()-rightnow, 2)} seconds')
with pd.ExcelWriter(filename) as writer:
    #writes dataframes to Excel workbook & names worksheets
    summary.to_excel(writer,  sheet_name='Summary')
    open.to_excel(writer, index = False,sheet_name='Ticket Detail')
    #accepted.to_excel(writer, index=False, sheet_name='Accepted')
    #rejected.to_excel(writer, index=False, sheet_name='Rejected')
    workbook=writer.book
    worksheet1=writer.sheets['Ticket Detail']
    #worksheet2=writer.sheets['Accepted']
    #worksheet3=writer.sheets['Rejected']
    worksheet4=writer.sheets['Summary']
    #Formatting Excel workbook.  Sets border as well as column width
    formater=workbook.add_format({'border':1})
    formater.set_text_wrap()
    formater.set_bg_color('white')
    worksheet1.set_column('A1:A'+openlength,16,formater)
    worksheet1.set_column('B1:B'+openlength,11.71,formater)
    worksheet1.set_column('C1:C'+openlength,15.29,formater)
    worksheet1.set_column('D1:D'+openlength,11.43,formater)
    worksheet1.set_column('E1:E'+openlength,60.43,formater)
    worksheet1.set_column('F1:F'+openlength,11.14,formater)
    #worksheet2.set_column('F:F',17.71,formater)
    #worksheet3.set_column('F:F',17.71,formater)
    worksheet1.set_column('G1:G'+openlength,10.57,formater)
    #worksheet2.set_column('G:G',16.29,formater)
    #worksheet3.set_column('G:G',16.29,formater)
    #worksheet1.set_column('H:H',55.57,formater)
    #worksheet2.set_column('H:H',55.57,formater)
    #worksheet3.set_column('H:H',55.57,formater)
    #worksheet1.set_column('I:I',16.29,formater)
    #worksheet2.set_column('I:I',16.29,formater)
    #worksheet3.set_column('I:I',16.29,formater)
    #worksheet1.set_column('J:J',16.29,formater)
    #worksheet2.set_column('J:J',16.29,formater)
    #worksheet3.set_column('J:J',16.29,formater)
    #worksheet1.set_column('K:K',16.29,formater)
    #worksheet2.set_column('K:K',16.29,formater)
    #worksheet3.set_column('K:K',16.29,formater)
    worksheet1.freeze_panes(1,0)
    #worksheet2.freeze_panes(1,0)
    #worksheet3.freeze_panes(1,0)
    #worksheet1.autofilter('A1:K1000')
    #worksheet2.autofilter('A1:K1000')
    #worksheet3.autofilter('A1:K1000')
    worksheet4.write(0,5, 'Synthesis', formater)
    worksheet4.set_column('B1:B'+summlength, 10.29, formater)
    worksheet4.set_column('C1:C'+summlength, 10.43,formater)
    #worksheet4.set_column('D:D', 5.57,formater)
print(f'Total time of {round(time.perf_counter()-start, 2)} seconds')
print(f'Your report has been saved in {filename}')
'''
print('Done!')
