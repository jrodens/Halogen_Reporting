#import libraries
import pandas as pd
from jira import JIRA
import getpass
import datetime
import matplotlib.pyplot as plt
from openpyxl.styles import Alignment
import time

starttimetoload= time.perf_counter()
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
Factor = []
now = datetime.datetime.now()
countopen=0
countdev=0
countqa=0
countaccepted=0
#represents the 9 applications part of the cutover apps for filtered view
#cutoverapps = ['EU Shortsale', 'Derivatives Management Application (DERMA)', 'Trading Hub', 'Broker Commission Reporting', 'Fair Value Actions', 'TRPSAM (.NET)', 'CRD', 'FODB']

#prompt user for authorization and authorize user
username = input('Enter your user name: ')
password = getpass.getpass(prompt='Enter your password: ')
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

#collect data from JIRA API
datafromjson = jira.search_issues('project = NYC-IO-Surge-Testing and "Application(s) Impacted" is not EMPTY',maxResults=10000)

print(f'Finished in loading datafromjson in {round(time.perf_counter()-starttimetoload, 2)} seconds')
rightnow= time.perf_counter()
#Class is used to make comparissons against non-string variables such as the object presented here
class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1
pri1 = ['Broadridge', 'Cougar', 'FID', 'Falcon', 'Nucleus', 'Perform', 'COIL', 'Cash Forecasting Database', 'Equity Quant']
pri2 = ['EU Shortsale', 'Derivatives Management Application (DERMA)', 'Trading Hub', 'Broker Commission Reporting', 'Fair Value Actions', 'TRPSAM (.NET)', 'CRD', 'FODB']

# get issues in dataset
for issue in datafromjson:
    ticket = issue.key
    status = S(issue.fields.status)
    synthesis = issue.fields.customfield_17001
    tdd = issue.fields.customfield_21501
    age = now - datetime.datetime.strptime(issue.fields.created[0:10], '%Y-%m-%d')
    summary = issue.fields.summary
    projects_impacted = issue.fields.customfield_21202
    labels=issue.fields.labels
    criticality = issue.fields.customfield_19700
    criticality=S(criticality)
    service = issue.fields.customfield_21800
    service = S(service)
    for application in issue.fields.customfield_18406:
        factor = 0
        application=S(application)
        if application in pri1:
            factor = 3
        elif application in pri2:
            factor = 2
        else:
            factor = 1
        Factor.append(factor)
        Application.append(application)
        Ticket.append(ticket)
        Status.append(status)
        Age.append(age.days)
        Summary.append(summary)
        TDD.append(tdd)
        Synthesis.append(synthesis)
        Labels.append(labels)
        Projects_Impacted.append(projects_impacted)
        Service.append(service)
        Criticality.append(criticality)

print(f'Finished in api call in {round(time.perf_counter()-rightnow, 2)} seconds')
rightnow= time.perf_counter()
newdata=pd.DataFrame()
newdata.insert(0,"Application", Application)
newdata.insert(1,"Ticket", Ticket)
newdata.insert(2,"Ticket Summary", Summary)
newdata.insert(3,"Status", Status)
newdata.insert(4, "Age", Age)
newdata.insert(5, "Projects Impacted", Projects_Impacted)
newdata.insert(6,"Target Delivery Date", TDD)
newdata.insert(7, "Synthesis", Synthesis)
newdata.insert(8, "Service", Service)
newdata.insert(9,"Criticality", Criticality)
newdata.insert(10, "Factor", Factor)

#newdata=newdata.loc[newdata['Application'].isin(cutoverapps)]
#newdata.explode('Projects Impacted')
#newdata.insert(10, "Dev Ticket", Linked)


open = newdata[(newdata.Status!='Accepted')&(newdata.Status!='Rejected')]
rejected = newdata[newdata.Status=='Rejected']
accepted = newdata[newdata.Status=='Accepted']
summary = newdata[(newdata.Status!='Rejected')]
application = newdata
summary=summary.replace(to_replace="Dev", value="Open")
summary=summary.replace(to_replace="Ready For Prioritization", value="Open")
summary=summary.replace(to_replace="Blocked", value="Open")
summary=summary.replace(to_replace="QA", value="Open")
summary=summary.replace(to_replace="QA Failed", value="Open")
summary=summary.replace(to_replace="Prioritized", value="Open")
#summary = summary.groupby(['Application', 'Service']).size()
summary = summary.groupby(['Service'])['Factor'].sum()
#summary = summary.unstack()
#summary = summary.fillna(0)
#summary = summary.transpose()
application = application.groupby(['Application', 'Status']).size()
application = application.unstack()
application = application.fillna(0)
#summaryaccepted = accepted.groupby(['Criticality', 'Application']).size()
#summaryopen.join(summaryaccepted)

#filename ='O:\Investment API Daily Ticket Metrics -' + str(datetime.datetime.today().strftime('%Y%m%d')) +'.xlsx'
total = application.join(summary , on='Application',how='outer')
print(f'Finished processing data  in {round(time.perf_counter()-rightnow, 2)} seconds')
filename = 'C:\\Users\\' + username + '\\OneDrive - TRowePrice\\API Tickets-'+ str(datetime.datetime.today().strftime('%Y%m%d')) +'.xlsx'
with pd.ExcelWriter(filename) as writer:
    #writes dataframes to Excel workbook & names worksheets
    total.to_excel(writer,  sheet_name='Service Summary')
    newdata.to_excel(writer, index = False,sheet_name='Detail')
    application.to_excel(writer, sheet_name='Application Summary')
    workbook=writer.book
    worksheet1=writer.sheets['Detail']
    worksheet4=writer.sheets['Service Summary']
    worksheet5=writer.sheets['Application Summary']
    #Formatting Excel workbook.  Sets border as well as column width
    formater=workbook.add_format({'border':1})
    formater.set_text_wrap()
    formater.set_bg_color('white')
    worksheet1.set_column('A:A',39.43,formater)
    worksheet1.set_column('B:B',8.57,formater)
    worksheet1.set_column('C:C',98.71,formater)
    worksheet1.set_column('D:D',5.14,formater)
    worksheet1.set_column('E:E',3.43,formater)
    worksheet1.set_column('F:F',17.71,formater)
    worksheet1.set_column('G:G',16.29,formater)
    worksheet1.set_column('H:H',55.57,formater)
    worksheet1.set_column('I:I',16.29,formater)
    worksheet1.set_column('J:J',16.29,formater)
    worksheet1.set_column('K:K',16.29,formater)
    worksheet1.freeze_panes(1,0)
    worksheet1.autofilter('A1:K1000')
    #worksheet4.write(0,3, 'Count', formater)
    worksheet4.set_column('B:B', 10.29, formater)
    worksheet4.set_column('C:C', 10.43,formater)
    worksheet4.set_column('D:D', 5.57,formater)

print(f'Finished in {round(time.perf_counter()-starttimetoload, 2)} seconds')
print(f'Your pdf has been saved in {filename}')
print('Done!')
