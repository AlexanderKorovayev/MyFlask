import requests


address = "http://localhost:2000/users?name=Vasya&age=26"


content = {"Content-Type": "text/html",
           "Host": "localhost"}

r = requests.post(url=address, headers=content)
print(r.text)

