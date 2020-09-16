import json
import requests
import getpass
import pandas as pd
from pandas.io.json import json_normalize


#username = input('Enter your user name: ')
#password = getpass.getpass(prompt="Enter password: ")

#datafromjson = requests.get('https://jira.troweprice.com/rest/api/2/search?jql=project%20%3D%20NYC-RIO-Surge-Halogen-Analysis%20and%20%22Epic%20Link%22%20%3D%20NYCRSA-993&maxResults=1000&fields=summary,issuelinks,labels', auth=(username,password)).content
#datafromjson = json.loads('response.json')
datafromjson = pd.read_json('response.json', typ='series', orient = 'columns')
datafromjson = json_normalize(datafromjson['issues'])
datafromjson.explode('fields.issuelinks')
#datafromjson = json_normalize(datafromjson['key'], record_path=['fields.issuelinks'], sep="_")
#datafromjson = datafromjson.explode('fields.labels')
#datafromjson = pd.read_json('response.json', typ='frame', orient = 'series')
datafromjson.to_excel('O:/df2.xlsx')
#datafromjson=json.load(datafromjson)
#datafromjson=json_normalize(datafromjson)
#datafromjson = json_normalize(datafromjson['issues'],meta=['fields.status.name'])
#datafromjson.to_excel('O:/df2.xlsx')
print('done')
