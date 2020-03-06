import requests


get_address = 'http://localhost:2000/users'

headers = {'Host': 'localhost',
           'Accept': 'text/html'}

r = requests.get(url=get_address,
                 headers=headers)

print(r.reason, r.status_code, r.headers)
print(r.text)
