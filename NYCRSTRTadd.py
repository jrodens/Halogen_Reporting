#import libraries
import pandas as pd
from jira import JIRA
import getpass
import datetime
import matplotlib.pyplot as plt
from openpyxl.styles import Alignment
import requests
from pandas.io.json import json_normalize
import json
import pprint

#setting up lists for entries

now = datetime.datetime.now()

#prompt user for authorization and authorize user
username = input('Enter your user name: ')
password = getpass.getpass(prompt='Enter your password: ')
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

#collect data from JIRA API
#datafromjson2 = requests.get('https://jira.troweprice.com/rest/api/2/search?jql=project%20%3D%20"IDW%20RIO%20Data%20Validation"%20and%20"Summary"%20~%20"Document%20Req"&maxResults=2000', auth=(username,password)).content
#datafromjson2 = pd.read_json(datafromjson2, typ='series', orient='columns')
#datafromjson2=json_normalize(datafromjson2['issues'],meta=['issue.key'])



datafromjson = jira.search_issues('project = "IDW RIO Data Validation" and "Summary" ~ "Document Req"',maxResults=1)
'''
3datafromjson = requests.get('https://jira.troweprice.com/rest/api/2/search?jql=project=%20"IDW%20RIO%20Data%20Validation"%20and%20summary%20~%20"document%20req"&maxResults=2000', auth=(username, password)).content

datafromjson = pd.read_json(datafromjson, typ='series', orient='columns')
datafromjson.to_excel('O:/rdtickets1.xlsx')
datafromjson=json_normalize(datafromjson['issues'],meta=['fields.summary'])
datafromjson.to_excel('O:/rdvtickets.xlsx')
'''

#Class is used to make comparissons against non-string variables such as the object presented here
class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1

Link_url = []
Link_title = []
Issue=[]



for issue in datafromjson:
    rlinks = jira.remote_links(issue.key)
    initial_issue = issue.key
    status = S(issue.fields.status)
    if len(rlinks )==0:
        identifier=0
        pass
    else:
        identifier=1
        requesturl = 'https://jira.troweprice.com/rest/api/latest/issue/' + issue.key + '/remotelink/'
        linkeditem = requests.get(requesturl, auth=(username, password)).content

        #print(linkeditem.url)
        linkeditem1 = pd.read_json(linkeditem, typ='frame', orient='columns')
       # linkeditem.to_excel('O:/linkeditem.xlsx')
        linkeditem2 = json_normalize(linkeditem1.loc[0,'object'], meta=['url'])
        linkeditem3=json_normalize(linkeditem1.loc[0,'object'], meta=['title'])
        print(linkeditem2.url[0])
        Link_url.append(linkeditem2.url[0])
        print(linkeditem3.title[0])
        Link_title.append(linkeditem3.title[0])
        Issue.append(issue.key)
        remote_link = {
                    'url':linkeditem2.url[0],
                    'title':linkeditem3.title[0]
        }

    epic = S(issue.fields.customfield_10506)
    epic = str(epic)
    summary = issue.fields.summary
    summary = summary.replace('[Document Req]','[Development]')
    description = issue.fields.description
    labels = issue.fields.labels


    issue_list = {
        'project': {'key': 'IDWRDV'},
        'summary': summary,
        'issuetype': {'name':'Task'},
        'description': description
        }
    new_issue=jira.create_issue(fields=issue_list)
    print(new_issue)

#    initial_issue.update(fields={"labels":"Copied"}
    epicissue=[]
    epicissue.append(str(new_issue))
    new_issue.update(fields={"labels":labels})
    new_link = jira.create_issue_link('relates to', new_issue, initial_issue)
    print(new_link)
    if identifier == 1:
        new_remotelink = jira.add_simple_link(new_issue, remote_link)
        print(new_remotelink)
    if "Accepted" in status:
        jira.transition_issue(new_issue, 321)
    jira.add_issues_to_epic(epic, epicissue)



''''
datafromjson2=datafromjson2.drop(['expand','id','self'], axis=1)
q1=pd.DataFrame()
q1.insert(0, "Issue", Issue)
q1.insert(1, "Link_Url", Link_url)
q1.insert(2, "Link_title", Link_title)
newdata=pd.merge(q1,datafromjson2,how='right', left_on='Issue', right_on='key')
newdata.to_excel('O:/newdata.xlsx')
newdata1=newdata.to_json(orient='index')
#jira.add_remote_link(issue, issue2)


    #ticket = issue.key



#df = pd.read_excel('o:/ForUpload.xlsx')

for index, row in df.iterrows():
    summ= df.iloc[index,0]
    points=0
    points= df.iloc[index,4]
    points = int(points)
    desc = df.iloc[index,3]
    component=df.iloc[index,1]

    issue_list = {
    'project': {'key': 'IDWRDV'},
    'summary': summ,
    'issuetype': {'name': 'Story'},
    'description': desc,
    'customfield_10502': points,
    }

    new_issue = jira.create_issue(fields=issue_list)
    print(new_issue)

    new_link = jira.create_issue_link('relates to', new_issue, block)
    print('Issue {} is related to {}'.format(new_issue,block))
    '''
print('Done!')
