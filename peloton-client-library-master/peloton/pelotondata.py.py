import requests
import pandas

s = requests.Session()
payload = {'username_or_email':'jrodens@gmail.com', 'password':'Sanchez26'}
s.post('https://api.onepeloton.com/auth/login', json=payload)


datafromjson = s.get('https://api.onepeloton.com/api/user/<user id>/workouts')

for item in datafromjson:
    print(item)
