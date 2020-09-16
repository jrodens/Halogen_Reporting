from jira import JIRA
import getpass

import string

username = input('Enter your user name: ')
password = getpass.getpass(prompt='Enter your password: ')
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})

datafromjson = jira.search_issues('project = NYC-RIO-Surge-Halogen and issuetype = Task', maxResults=2000,fields="description")



# Create an empty dictionary
d = dict()


class S(str):
 def __contains__(self, x):
     for i in range(len(self)):
         if self.startswith(x,i): return 1
# Loop through each line of the file
for issue in datafromjson:
    # Remove the leading spaces and newline character
    line = issue.fields.description
    line = S(line)
    line = line.strip()

    # Convert the characters in line to
    # lowercase to avoid case mismatch
    line = line.lower()

    # Remove the punctuation marks from the line
    line = line.translate(line.maketrans("", "", string.punctuation))

    # Split the line into words
    words = line.split(" ")

    # Iterate over each word in line
    for word in words:
        # Check if the word is already in dictionary
        if word in d:
            # Increment count of word by 1
            d[word] = d[word] + 1
        else:
            # Add the word to dictionary with count 1
            d[word] = 1

# Print the contents of dictionary
for key in list(d.keys()):
    print(key, ":", d[key])
