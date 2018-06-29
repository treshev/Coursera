import requests

from coursera_house.core.models import Setting


def test_post():
    data = {
        "bedroom_target_temperature": 30,
        "hot_water_target_temperature": 31,
    }

    req = requests.post("http://127.0.0.1:8000/control", data=data)
    print("ALTR POST answer = ", req.status_code, req.content)


def test_502():
    headers = {
        'authorization': "Bearer " + Setting.SMART_HOME_ACCESS_TOKEN,
        'content-type': "application/json",
    }
    try:
        req = requests.get(Setting.SMART_HOME_API_URL + "user.controller", headers=headers)
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    test_post()
