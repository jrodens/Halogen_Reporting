from jira import JIRA
import openpyxl, pprint
import pandas as pd
import json
import getpass
print('start')

username = input('Enter your user name: ')
password = getpass.getpass(prompt='Enter password: ')
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

newissue=[]
class S(str):
    def __contains__(self, x):
        for i in range(len(self)):
            if self.startswith(x,i): return 1

issue = jira.issue('nycrht-96')
release = [{'name':'release 1'}]
#issue.fields.fixVersion.name.append(u'release 1')
issue.update(fields = {"fixVersions": release})
#issue.update(fixVersions= {'name' : release})
print('Done')
