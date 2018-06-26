from __future__ import absolute_import, unicode_literals

from time import sleep

import requests
from celery import task

from .models import Setting

'''
Устройства (запись):
air_conditioner – Кондиционер (true – вкл, false – выкл). 
При включении постепенно понижает температуру в спальне, пока она не достигнет 16 градусов и сильнее охладить уже не может.

bedroom_light – Лампа в спальне (true – вкл, false – выкл).
bathroom_light – Лампа в ванной (true – вкл, false – выкл).
curtains – Занавески string (“open” – открыть, “close” – закрыть).
boiler – Бойлер (true – вкл, false – выкл). При включении постепенно повышает температуру воды, пока она не достигнет 90 градусов. Для работы должен быть открыт входной кран холодной воды.
cold_water – Входной кран холодной воды (true – открыть, false – закрыть). Позволяет открыть/перекрыть подачу холодной воды в квартиру
hot_water – Входной кран горячей воды (true – открыть, false – закрыть).
washing_machine – Стиральная машина string (“on” – вкл, “off” – выкл). При включении начинает стирать, потом самостоятельно отключается. Может сломаться и протечь.
'''


@task
def smart_home_manager():
    response = get_response_form_the_controller()
    callback_commands = response_handler(response)
    print("ALTR commands: ", callback_commands)
    if len(callback_commands) > 1:
        print("ALTR commands sent : ", callback_commands)
        send_callback_commands(callback_commands)
    return response

def get_response_form_the_controller():
    headers = {
        'authorization': "Bearer " + Setting.SMART_HOME_ACCESS_TOKEN,
        'content-type': "application/json",
    }
    req = requests.get(Setting.SMART_HOME_API_URL + "user.controller", headers=headers)
    if req.status_code == 200:
        result = {}
        for param in req.json()['data']:
            result[param["name"]] = param["value"]
        return result


def response_handler(response: dict):
    callback = []

    settings = Setting.objects.all()

    base_data = {}
    for setting in settings:
        base_data[setting.controller_name] = setting.value

    if response.get("leak_detector", None) == "True":
        item = {"name": "cold_water",
                "value": False
                }
        callback.append(item)

        item = {"name": "hot_water",
                "value": False
                }
        callback.append(item)
        send_email()

    if response.get("cold_water", None) == "False":
        callback.append({"name": 'boiler', "value": False})
        callback.append({"name": 'washing_machine', "value": "off"})
        # TODO: надо понять как включать машинку если дадут воду

    if response.get("boiler_temperature", None) is not None and response.get("boiler_temperature", None) < (
            base_data["hot_water_target_temperature"] - (
            base_data["hot_water_target_temperature"] / 100 * 10)):
        callback.append({"name": 'boiler', "value": True})
    elif response.get("boiler_temperature", None) is not None and response.get("boiler_temperature", 0) > (
            base_data["hot_water_target_temperature"] + (
            base_data["hot_water_target_temperature"] / 100 * 10)):
        callback.append({"name": 'boiler', "value": False})

    if response.get("curtains", None) != "slightly_open":
        if response.get("outdoor_light", None) < 50 and response.get("bedroom_light", None) == "False":
            callback.append({"name": 'curtains', "value": "open"})

        if response.get("outdoor_light", None) > 50 or response.get("bedroom_light", None) == "True":
            callback.append({"name": 'curtains', "value": "close"})

    if response.get("smoke_detector", None) == "True":
        callback.append({"name": 'air_conditioner', "value": False})
        callback.append({"name": 'bedroom_light', "value": False})
        callback.append({"name": 'bathroom_light', "value": False})
        callback.append({"name": 'boiler', "value": False})
        callback.append({"name": 'washing_machine', "value": "off"})

    if response.get("bedroom_temperature", 0) > (base_data["bedroom_target_temperature"] + (
            base_data["bedroom_target_temperature"] / 100 * 10)):
        callback.append({"name": 'air_conditioner', "value": True})
    elif response.get("bedroom_temperature", 0) < (base_data["bedroom_target_temperature"] - (
            base_data["bedroom_target_temperature"] / 100 * 10)):
        callback.append({"name": 'air_conditioner', "value": False})
    return callback


def send_callback_commands(commands: list):
    headers = {
        'authorization': "Bearer " + Setting.SMART_HOME_ACCESS_TOKEN,
        'content-type': "application/json",
    }
    data = {"controllers": commands}
    req = requests.post(Setting.SMART_HOME_API_URL + "user.controller", headers=headers, json=data)
    print("ALTR POST answer = ", req.json())


def send_email():
    pass


def start_timer():
    while True:
        smart_home_manager()
        sleep(5)
