import requests

from coursera_house.core.models import Setting
from requests.exceptions import ConnectionError


# commands = [{
#     "name": "air_conditioner",
#     "value": False
# }, ]
#
# data = {
#     "bedroom_target_temperature": 43,
#     "hot_water_target_temperature": 33,
#         }
#
# # req = requests.post("http://smarthome.t3st.ru/api/user.controller", headers=headers, json=data)
# req = requests.post("http://127.0.0.1:8000/control", data=data)
# print("ALTR POST answer = ", req.status_code, req.content)

headers = {
    'authorization': "Bearer " + Setting.SMART_HOME_ACCESS_TOKEN,
    'content-type': "application/json",
}
# try:
#     req = requests.get(Setting.SMART_HOME_API_URL + "user.controller", headers=headers)
# except Exception as ex:
#     print(ex)

try:
    req = requests.get("http://www.google2.com")
except ConnectionError as e:    # This is the correct syntax
   print(e)
   r = "No response"

