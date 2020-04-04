import requests


post_address = 'http://localhost:2000/users?name=Vasya&age=26'

headers = {'Host': 'localhost',
           'Accept': 'text/html'}


r = requests.post(url=post_address,
                  headers=headers)

print(r.reason, r.status_code)
print(r.text)