import requests

commands = [{
    "name": "air_conditioner",
    "value": False
}, ]

data = {
    "bedroom_target_temperature": 43,
    "hot_water_target_temperature": 33,
        }

# req = requests.post("http://smarthome.t3st.ru/api/user.controller", headers=headers, json=data)
req = requests.post("http://127.0.0.1:8000/control", data=data)
print("ALTR POST answer = ", req.status_code, req.content)
