from __future__ import absolute_import, unicode_literals
from celery import task
from celery import shared_task
import requests

from .models import Setting

@task
def smart_home_manager():
    print('ALTR 111')
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
    pass

@shared_task
def add(x, y):
    return x + y
