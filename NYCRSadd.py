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


datafromjson = jira.search_issues('project = nycrs and issueFunction in linkedissuesof("key=NYCRSA-541")', maxResults=1000)

#Class is used to make comparissons against non-string variables such as the object presented here
class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1


Issue=[]

for issue in datafromjson:
    existingComponents = []
    rlinks = jira.remote_links(issue.key)
    initial_issue = issue.key
    status = S(issue.fields.status)
    for component in issue.fields.components:
        existingComponents.append({"name" : component.name})
    if len(rlinks )==0:
        identifier=0
        pass
    else:
        identifier=1
        requesturl = 'https://jira.troweprice.com/rest/api/latest/issue/' + issue.key + '/remotelink/'
        linkeditem = requests.get(requesturl, auth=(username, password)).content
        linkeditem1 = pd.read_json(linkeditem, typ='frame', orient='columns')
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
    description = issue.fields.description
    labels = issue.fields.labels
    issue_list = {
        'project': {'key': 'NYCRS'},
        'summary': summary,
        'issuetype': {'name':'Task'},
        'description': description
        }
    new_issue=jira.create_issue(fields=issue_list)
    print(new_issue)
    epicissue=[]
    epicissue.append(str(new_issue))
    new_issue.update(fields={"labels":labels})
    new_link = jira.create_issue_link('relates to', new_issue, initial_issue)
    print(new_link)
    if identifier == 1:
        new_remotelink = jira.add_simple_link(new_issue, remote_link)
        print(new_remotelink)
    jira.add_issues_to_epic(epic, epicissue)
    new_issue.update(fields={"components": existingComponents})


print('Done!')
