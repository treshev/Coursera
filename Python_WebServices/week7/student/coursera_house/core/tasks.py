from __future__ import absolute_import, unicode_literals
from time import sleep
from celery import task
from .models import Setting

import django.core.mail as mail
import requests


@task
def smart_home_manager():
    print("ALTR GET to controller")
    req = get_response_form_the_controller()

    if req and req.status_code == 200:

        device_parameters = get_devices_parameters(req)
        callback_commands = response_handler(device_parameters)

        if callback_commands:
            print("ALTR POST to controller")
            send_callback_commands(callback_commands)

        return device_parameters

    return None


def get_devices_parameters(req):
    device_parameters = {}
    for param in req.json()['data']:
        device_parameters[param["name"]] = param["value"]
    return device_parameters


def get_response_form_the_controller():
    headers = {
        'authorization': "Bearer " + Setting.SMART_HOME_ACCESS_TOKEN,
        'content-type': "application/json",
    }
    try:
        req = requests.get(Setting.SMART_HOME_API_URL + "user.controller", headers=headers)
    except requests.exceptions.ConnectionError:
        return None
    return req


def send_callback_commands(commands: list):
    headers = {
        'authorization': "Bearer " + Setting.SMART_HOME_ACCESS_TOKEN,
        'content-type': "application/json",
    }
    data = {"controllers": commands}

    try:
        req = requests.post(Setting.SMART_HOME_API_URL + "user.controller", headers=headers, json=data)
    except requests.exceptions.ConnectionError:
        return None
    return req


def append_command(name, value, response, callback):
    if response.get(name, None) != value:
        callback.append({"name": name, "value": value})


def response_handler(response: dict):
    callback = []

    settings = Setting.objects.all()

    base_data = {}
    for setting in settings:
        base_data[setting.controller_name] = setting.value

    if response.get("smoke_detector", None) is True:
        append_command('air_conditioner', False, response, callback)
        append_command('bedroom_light', False, response, callback)
        append_command('bathroom_light', False, response, callback)
        append_command('boiler', False, response, callback)
        append_command('washing_machine', "off", response, callback)
    else:
        if response.get("bedroom_temperature", 0) > (
                base_data["bedroom_target_temperature"] + (
                base_data["bedroom_target_temperature"] / 100 * 10)):
            append_command('air_conditioner', True, response, callback)
        elif response.get("bedroom_temperature", 0) < (
                base_data["bedroom_target_temperature"] - (
                base_data["bedroom_target_temperature"] / 100 * 10)):
            append_command('air_conditioner', False, response, callback)

    if response.get("leak_detector", None) is True:
        append_command('cold_water', False, response, callback)
        append_command('hot_water', False, response, callback)
        append_command('boiler', False, response, callback)
        if response.get("smoke_detector", None) is False:
            append_command('washing_machine', "off", response, callback)
        send_email()
    else:
        if response.get("smoke_detector", None) is False and response.get("cold_water", None) is False:
            append_command('boiler', False, response, callback)
            append_command('washing_machine', "off", response, callback)

        if response.get("smoke_detector", None) is False and response.get("boiler_temperature",
                                                                          None) is not None and response.get(
            "boiler_temperature", None) < (
                base_data["hot_water_target_temperature"] - (
                base_data["hot_water_target_temperature"] / 100 * 10)):
            append_command('boiler', True, response, callback)
        elif response.get("smoke_detector", None) is False and response.get("boiler_temperature",
                                                                            None) is not None and response.get(
            "boiler_temperature", 0) > (
                base_data["hot_water_target_temperature"] + (
                base_data["hot_water_target_temperature"] / 100 * 10)):
            append_command('boiler', False, response, callback)

    if response.get("curtains", None) != "slightly_open":
        if response.get("outdoor_light", None) < 50 and response.get("bedroom_light", None) is False:
            append_command('curtains', "open", response, callback)

        if response.get("outdoor_light", None) > 50 or response.get("bedroom_light", None) is True:
            append_command('curtains', "close", response, callback)

    return callback


def send_email():
    mail.send_mail(
        'Обнаружена протечка',
        'Обнаружена протечка, вода перекрыта',
        recipient_list=Setting.MAIL_RECEPIENT,
        fail_silently=False,
    )


def start_timer():
    while True:
        print("timer is working")
        smart_home_manager()
        sleep(5)