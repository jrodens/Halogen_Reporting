from jira import JIRA
import pandas as pd
import getpass


username = input("Enter your username: ")
password = getpass.getpass(prompt="Enter Password: ")
jira = JIRA(basic_auth= (username, password), options = {'server':'https://jira.troweprice.com'})

ViewData = jira.search_issues('project = NYC-RIO-Surge-Halogen-Analysis and "Epic Link" = NYCRSA-993', fields= 'summary, status, key, labels, issuelinks',maxResults=1000)
Attributedata = jira.search_issues('project = NYC-RIO-Surge-Halogen and component = "Positions Domain" and issuetype = Task', fields= 'summary, status, key, labels', maxResults=10000)

print('done')

