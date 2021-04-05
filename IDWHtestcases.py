from adaptavist import Adaptavist
import getpass
import pandas as pd
import matplotlib.pyplot as plt


username = input('Enter your user name: ')
password = getpass.getpass(prompt="Enter Password")
sprint = input('Enter the name of the sprint label: ')
atm = Adaptavist('https://jira.troweprice.com', username, password)


project = 'projectKey = "IDWRDV" AND labels IN "' + sprint + '"'

data = atm.get_test_cases(project)

testcases = pd.DataFrame(data)
testcases = testcases['status']
testcases = testcases.groupby(['status']).sum()
testcases.unstack()

color_dict = {'Accepted':'#7030A0','Dev': '#4472C4', 'Prioritized': '#C00000', 'Ready For Prioritization': '#002060', 'Blocked':'#FFC000','In Progress':'#002060','Not Started':'#C00000','QA':'#548235','Rejected':'#808080'}
fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1= testcases.plot(ax=ax1, kind='bar',stacked=True, figsize=(20,10), color=[color_dict.get(x) for x in testcases.columns], label = ["Not Started", "In Progress","Blocked","QA","Accepted"],title='item')
fig.savefig('O:/IDW2TestCases.pdf', orientation='landscape', bbox_inches='tight')
plt.close()
