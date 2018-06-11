import requests
from requests.auth import HTTPBasicAuth

response1 = requests.post("http://79.137.175.13/submissions/1/", auth=('alladin', 'opensesame'))
print(response1.json())

response2 = requests.put("http://79.137.175.13/submissions/super/duper/secret/", auth=('galchonok', 'ktotama'))
print(response2.json())