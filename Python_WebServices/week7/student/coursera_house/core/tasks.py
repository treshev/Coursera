from __future__ import absolute_import, unicode_literals

from time import sleep

import django.core.mail as mail
import requests
from celery import task

from .models import Setting


@task
def smart_home_manager():
    response = get_response_form_the_controller()
    callback_commands = response_handler(response)
    print("ALTR commands: ", callback_commands)
    if len(callback_commands) > 0:
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

    if response.get("smoke_detector", None) is True:
        callback.append({"name": 'air_conditioner', "value": False})
        callback.append({"name": 'bedroom_light', "value": False})
        callback.append({"name": 'bathroom_light', "value": False})
        callback.append({"name": 'boiler', "value": False})
        callback.append({"name": 'washing_machine', "value": "off"})
    else:
        if response.get("bedroom_temperature", 0) > (
                base_data["bedroom_target_temperature"] + (
                base_data["bedroom_target_temperature"] / 100 * 10)):
            callback.append({"name": 'air_conditioner', "value": True})
        elif response.get("bedroom_temperature", 0) < (
                base_data["bedroom_target_temperature"] - (
                base_data["bedroom_target_temperature"] / 100 * 10)):
            callback.append({"name": 'air_conditioner', "value": False})

    if response.get("leak_detector", None) is True:
        callback.append({"name": "cold_water", "value": False})
        callback.append({"name": "hot_water", "value": False})
        callback.append({"name": 'boiler', "value": False})
        callback.append({"name": 'washing_machine', "value": "off"})
        send_email()
    else:
        if response.get("smoke_detector", None) is False and response.get("cold_water", None) is False:
            callback.append({"name": 'boiler', "value": False})
            callback.append({"name": 'washing_machine', "value": "off"})
            # TODO: надо понять как включать машинку если дадут воду

        if response.get("smoke_detector", None) is False and response.get("boiler_temperature",
                                                                          None) is not None and response.get(
            "boiler_temperature", None) < (
                base_data["hot_water_target_temperature"] - (
                base_data["hot_water_target_temperature"] / 100 * 10)):
            callback.append({"name": 'boiler', "value": True})
        elif response.get("smoke_detector", None) is False and response.get("boiler_temperature",
                                                                            None) is not None and response.get(
            "boiler_temperature", 0) > (
                base_data["hot_water_target_temperature"] + (
                base_data["hot_water_target_temperature"] / 100 * 10)):
            callback.append({"name": 'boiler', "value": False})

    if response.get("curtains", None) != "slightly_open":
        if response.get("outdoor_light", None) < 50 and response.get("bedroom_light", None) is False:
            callback.append({"name": 'curtains', "value": "open"})

        if response.get("outdoor_light", None) > 50 or response.get("bedroom_light", None) is True:
            callback.append({"name": 'curtains', "value": "close"})

    return callback


def send_callback_commands(commands: list):
    headers = {
        'authorization': "Bearer " + Setting.SMART_HOME_ACCESS_TOKEN,
        'content-type': "application/json",
    }
    data = {"controllers": commands}
    req = requests.post(Setting.SMART_HOME_API_URL + "user.controller", headers=headers, json=data)
    print("ALTR POST code = ", req.status_code)
    # print("ALTR POST json = ", req.status_code, req.json())


def send_email():
    mail.send_mail(
        'Обнаружена протечка',
        'Обнаружена протечка, вода перекрыта',
        'nemo_samara@mail.ru',
        Setting.MAIL_RECEPIENT,
        fail_silently=False,
    )


def start_timer():
    while True:
        print("timer is working")
        smart_home_manager()
        sleep(5)
