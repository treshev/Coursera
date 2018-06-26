import requests

commands = [{
    "name": "air_conditioner",
    "value": False
}, ]

headers = {
    'authorization': "Bearer cd5547b376b51438221dcdc905b426cfd463d8735a5ab1509c137ceb2f66132a",
    'content-type': "application/json",
}

data = {"controllers": commands}

print("ALTR DATA = ", data)
req = requests.post("http://smarthome.t3st.ru/api/user.controller", headers=headers, json=data)
print("ALTR POST answer = ", req.status_code, req.json())
