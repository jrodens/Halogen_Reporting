#import libraries
import pandas as pd
from jira import JIRA
import getpass
import datetime
import matplotlib.pyplot as plt
from openpyxl.styles import Alignment

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
now = datetime.datetime.now()
countopen=0
countdev=0
countqa=0
countaccepted=0
#represents the 11 applications part of the cutover apps for filtered view
cutoverapps = ['Broadridge','COIL', 'Cash Forecasting Database','Cougar', 'Domino - Cash Notification System: Adhoc', 'Equity Quant', 'FID', 'Falcon', 'Hedgehog', 'Nucleus', 'Perform']
rioapps = ['RIO 2.0', 'RIO-RR']
#prompt user for authorization and authorize user
username = input('Enter your user name: ')
password = getpass.getpass(prompt='Enter your password: ')
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

#collect data from JIRA API
datafromjson = jira.search_issues('project = NYC-IO-Surge-Testing and "Epic Link" = NYCTT-1026 ',maxResults=10000)

#Class is used to make comparissons against non-string variables such as the object presented here
class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1

# get issues in dataset
for issue in datafromjson:
    ticket = issue.key
    status = issue.fields.status
    synthesis = issue.fields.customfield_17001
    tdd = issue.fields.customfield_21501
    age = now - datetime.datetime.strptime(issue.fields.created[0:10], '%Y-%m-%d')
    summary = issue.fields.summary
    projects_impacted = issue.fields.customfield_21202
    labels=issue.fields.labels
    service=issue.fields.customfield_21800
    component = issue.fields.components
    origin = issue
    linked=""
    for link in issue.fields.issuelinks:
        if hasattr(link, "outwardIssue"):
            outwardIssue = link.outwardIssue
            if "NYCIO" in outwardIssue.key:
                linked=jira.issue(outwardIssue.key)
                print(issue)
        elif hasattr(link, "inwardIssue"):
            inwardIssue = link.inwardIssue
            if "NYCIO" in inwardIssue.key:
                linked = jira.issue(inwardIssue.key)
                print(issue)
    issue= origin
    for application in issue.fields.customfield_18406:
        #allows for comparison from the object to a string
        tempapp=S(application)
        tempstatus = S(status)
        tempproject = S(projects_impacted)
        if not issue.fields.components:
            Application.append(tempapp)
            Ticket.append(ticket)
            Status.append(tempstatus)
            Age.append(age.days)
            Summary.append(summary)
            TDD.append(tdd)
            Synthesis.append(synthesis)
            Labels.append(labels)
            Projects_Impacted.append(tempproject)
            Service.append(service)
            Component.append("")
            Linked.append(linked)
        for component in issue.fields.components:
            component =  component.name
            #appends a row for each application in the data frame and attaches requisite inforamtion
            Application.append(tempapp)
            Ticket.append(ticket)
            Status.append(tempstatus)
            Age.append(age.days)
            Summary.append(summary)
            TDD.append(tdd)
            Synthesis.append(synthesis)
            Labels.append(labels)
            Projects_Impacted.append(tempproject)
            Service.append(service)
            Component.append(component)
            Linked.append(linked)
        
#create dataframe with new information to put into Excel Sheet
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
newdata.insert(9, "Dev Team", Component)
newdata.insert(10, "Dev Ticket", Linked)

newdata.to_excel('O:/API Tickets.xlsx', index = False)

new = pd.DataFrame()
other = pd.DataFrame()
accepted = pd.DataFrame()
linked = pd.DataFrame()

new = newdata[(newdata.Status == 'Open')]
other = newdata[(newdata.Status != 'Open') & (newdata.Status != 'Accepted') & (newdata.Status != 'Rejected')]
accepted = newdata[(newdata.Status == 'Accepted')|(newdata.Status == 'Rejected')]
linked = other

new = new.drop('Dev Ticket', axis=1)
other = other.drop('Dev Ticket', axis=1)
accepted = accepted.drop('Dev Ticket', axis=1)

filename ='O:\Investment API Daily Ticket Breakdown -' + str(datetime.datetime.today().strftime('%Y%m%d')) +'.xlsx'
with pd.ExcelWriter(filename) as writer:
    new.to_excel(writer, index=False, sheet_name='New Tickets')
    other.to_excel(writer, index=False, sheet_name='Open Tickets')
    accepted.to_excel(writer, index = False, sheet_name = 'Closed Tickets')
    linked.to_excel(writer, index = False, sheet_name = 'Open Tickets with LInks')
'''
#create dataframes for individual tabs
acceptedstories=pd.DataFrame()
QAstories=pd.DataFrame()
Devstories=pd.DataFrame()
Openstories=pd.DataFrame()
Filteredstories=pd.DataFrame()
riotickets=pd.DataFrame()

#filter data for individual tabs
QAstories=newdata[newdata.Status=='QA']
acceptedstories=newdata[newdata.Status=='Accepted']
Devstories=newdata[(newdata.Status=='Dev')|(newdata.Status =='QA Failed')]
Openstories=newdata[(newdata.Status=='Ready For Prioritization')|(newdata.Status =='Open')|(newdata.Status=='Prioritized')]
riotickets=newdata[(newdata['Projects Impacted'] =='RIO 2.0')|(newdata['Projects Impacted']=='RIO-RR')]

#filters out only the applications inscope for cutover
Devstories = Devstories.loc[Devstories['Application'].isin(cutoverapps)]
Filteredstories= newdata.loc[newdata['Application'].isin(cutoverapps)]
QAstories=QAstories.loc[newdata['Application'].isin(cutoverapps)]

#sort for presentation
acceptedstories = acceptedstories.sort_values(by='Application', ascending=True)
Devstories = Devstories.sort_values(by='Application', ascending=True)
QAstories = QAstories.sort_values(by='Application', ascending=True)
Openstories = Openstories.sort_values(by='Application', ascending=True)
newdata=newdata.sort_values(by='Application', ascending=True)
Filteredstories= Filteredstories.sort_values(by='Application', ascending=True)
riotickets=riotickets.sort_values(by='Application', ascending = True)

#sort by application and save to Excel
filename ='O:\Investment API Daily Ticket Metrics -' + str(datetime.datetime.today().strftime('%Y%m%d')) +'.xlsx'
newdata = newdata.sort_values(by='Application', ascending=True)
#newdata.to_excel('O:\API_Ticket_Master_Log.xlsx', index=False)
with pd.ExcelWriter(filename) as writer:
    #writes dataframes to Excel workbook & names worksheets
    Devstories.to_excel(writer, index = False,sheet_name='In Dev (Filtered Apps)')
    QAstories.to_excel(writer, index=False, sheet_name='In QA (Filtered Apps)')
    Filteredstories.to_excel(writer, index=False, sheet_name='All Tickets (Filtered Apps)')
    Openstories.to_excel(writer,index=False,sheet_name='Open Tickets (All Apps)')
    acceptedstories.to_excel(writer, index=False,sheet_name='Accepted (All Apps)')
    newdata.to_excel(writer,index=False, sheet_name='All Tickets (All Apps)') 
    riotickets.to_excel(writer, index=False, sheet_name='RIO Tickets (All Statuses)')
    workbook=writer.book
    worksheet1=writer.sheets['In Dev (Filtered Apps)']
    worksheet2=writer.sheets['In QA (Filtered Apps)']
    worksheet3=writer.sheets['Accepted (All Apps)']
    worksheet4=writer.sheets['Open Tickets (All Apps)']
    worksheet5=writer.sheets['All Tickets (All Apps)']
    worksheet6=writer.sheets['All Tickets (Filtered Apps)']
    worksheet7=writer.sheets['RIO Tickets (All Statuses)']
    #Formatting Excel workbook.  Sets border as well as column width
    formater=workbook.add_format({'border':1})
    formater.set_text_wrap()    
    worksheet1.set_column('A:A',39.43,formater)
    worksheet2.set_column('A:A',39.43,formater)
    worksheet3.set_column('A:A',39.43,formater)
    worksheet4.set_column('A:A',39.43,formater)
    worksheet5.set_column('A:A',39.43,formater)
    worksheet6.set_column('A:A',39.43,formater)
    worksheet7.set_column('A:A',39.43,formater)
    worksheet1.set_column('B:B',8.57,formater)
    worksheet2.set_column('B:B',8.57,formater)
    worksheet3.set_column('B:B',8.57,formater)
    worksheet4.set_column('B:B',8.57,formater)
    worksheet5.set_column('B:B',8.57,formater)
    worksheet6.set_column('B:B',8.57,formater)
    worksheet7.set_column('B:B',8.57,formater)
    worksheet1.set_column('C:C',98.71,formater)
    worksheet2.set_column('C:C',98.71,formater)
    worksheet3.set_column('C:C',98.71,formater)
    worksheet4.set_column('C:C',98.71,formater)
    worksheet5.set_column('C:C',98.71,formater)
    worksheet6.set_column('C:C',98.71,formater)
    worksheet7.set_column('C:C',98.71,formater)
    worksheet1.set_column('D:D',5.14,formater)
    worksheet2.set_column('D:D',5.14,formater)
    worksheet3.set_column('D:D',5.14,formater)
    worksheet4.set_column('D:D',5.14,formater)
    worksheet5.set_column('D:D',5.14,formater)
    worksheet6.set_column('D:D',5.14,formater)
    worksheet7.set_column('D:D',5.14,formater)
    worksheet1.set_column('E:E',3.43,formater)
    worksheet2.set_column('E:E',3.43,formater)
    worksheet3.set_column('E:E',3.43,formater)
    worksheet4.set_column('E:E',3.43,formater)
    worksheet5.set_column('E:E',3.43,formater)
    worksheet6.set_column('E:E',3.43,formater)
    worksheet7.set_column('E:E',3.43,formater)
    worksheet1.set_column('F:F',17.71,formater)
    worksheet2.set_column('F:F',17.71,formater)
    worksheet3.set_column('F:F',17.71,formater)
    worksheet4.set_column('F:F',17.71,formater)
    worksheet5.set_column('F:F',17.71,formater)
    worksheet6.set_column('F:F',17.71,formater)
    worksheet7.set_column('F:F',17.71,formater)
    worksheet1.set_column('G:G',16.29,formater)
    worksheet2.set_column('G:G',16.29,formater)
    worksheet3.set_column('G:G',16.29,formater)
    worksheet4.set_column('G:G',16.29,formater)
    worksheet5.set_column('G:G',16.29,formater)
    worksheet6.set_column('G:G',16.29,formater)
    worksheet7.set_column('G:G',16.29,formater)
    worksheet1.set_column('H:H',55.57,formater)
    worksheet2.set_column('H:H',55.57,formater)
    worksheet3.set_column('H:H',55.57,formater)
    worksheet4.set_column('H:H',55.57,formater)
    worksheet5.set_column('H:H',55.57,formater)
    worksheet6.set_column('H:H',55.57,formater)
    worksheet7.set_column('H:H',55.57,formater)
    worksheet1.set_column('I:I',16.29,formater)
    worksheet2.set_column('I:I',16.29,formater)
    worksheet3.set_column('I:I',16.29,formater)
    worksheet4.set_column('I:I',16.29,formater)
    worksheet5.set_column('I:I',16.29,formater)
    worksheet6.set_column('I:I',16.29,formater)
    worksheet7.set_column('I:I',16.29,formater)
    worksheet1.set_column('J:J',16.29,formater)
    worksheet2.set_column('J:J',16.29,formater)
    worksheet3.set_column('J:J',16.29,formater)
    worksheet4.set_column('J:J',16.29,formater)
    worksheet5.set_column('J:J',16.29,formater)
    worksheet6.set_column('J:J',16.29,formater)
    worksheet7.set_column('J:J',16.29,formater)
    worksheet1.freeze_panes(1,0)
    worksheet2.freeze_panes(1,0)
    worksheet3.freeze_panes(1,0)
    worksheet4.freeze_panes(1,0)
    worksheet5.freeze_panes(1,0)
    worksheet6.freeze_panes(1,0)
    worksheet7.freeze_panes(1,0)
    worksheet1.autofilter('A1:J1000')
    worksheet2.autofilter('A1:J1000')
    worksheet3.autofilter('A1:J1000')
    worksheet4.autofilter('A1:J1000')
    worksheet5.autofilter('A1:J1000')
    worksheet6.autofilter('A1:J1000')
    worksheet7.autofilter('A1:J1000')
    #workbook.conditional_formatting({'border': 1})
'''
print('Done!')
