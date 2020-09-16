#import libraries
import pandas as pd
from jira import JIRA
import getpass


#prompt user for authorization and authorize user
username = input('Enter your user name: ')
password = getpass.getpass(prompt='Enter your password: ')
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

#Extract from Excel file name of on-boarders & user id to assign stories to
onboarders = pd.DataFrame()
onboarders = pd.read_excel(filename)

#Grab the template of stories
datafromjson = jira.search_issues('project = NYCIO and "Epic Link" = NYCIO-3093',maxResults=50)

#Class is used to make comparissons against non-string variables such as the object presented here
class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1

Link_url = []
Link_title = []
Issue=[]

#Goes through each individual in Excel list, establishes epic and then copies stories linked to that epic

assignee = 'TRPHR02'
for issue in datafromjson:
    summary = issue.fields.summary
    description = issue.fields.description
    acceptance = S(issue.fields.customfield_16901)
    issue_list = {
        'project': {'key': 'NYCIO'},
        'summary': summary,
        'issuetype': {'name':'Story'},
        'description': description,
        'customfield_16901': acceptance,
        'assignee': {'name': assignee}
        }
    new_issue=jira.create_issue(fields=issue_list)
    print(f'Story {new_issue} has been created')
    jql = str('project = NYCIO and sprint in openSprints() and summary ~ "' + summary + '"')
    issuesassociated = jira.search_issues(jql)
    for issue in issuesassociated:
        block = issue.key
        new_link = jira.create_issue_link('relates to', new_issue, block)
        print(new_link)


print('Done!')
