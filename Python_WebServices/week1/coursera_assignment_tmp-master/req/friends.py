import re

import collections
import requests

ACCESS_TOKEN = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'

params = {
    "v": "5.71",
    "access_token": ACCESS_TOKEN
}


def calc_friends_age(friends_list):
    result = []
    for friend in friends_list:
        if "bdate" in friend.keys():
            date = friend["bdate"].split(".")
            # if len(date) > 2:
            if re.match("[0-9]+.[0-9]+.[0-9]+", friend["bdate"]):
                result.append(2018 - int(date[2]))
    result_dict = collections.Counter(result)
    result = list(result_dict.items())
    result.sort(key=lambda x: (x[1], -x[0]), reverse=True)
    return (result)

def get_friends_list(uid):
    if uid.isdigit():
        params["user_id"] = uid
    else:
        params["user_ids"] = uid

    req = requests.get("https://api.vk.com/method/users.get", params=params)

    params["user_id"] = req.json()["response"][0]['id']
    params["fields"] = "bdate"
    birthdayRequest = requests.get("https://api.vk.com/method/friends.get", params=params)
    return birthdayRequest.json()["response"]["items"]

def get_user_info(uid):
    if uid.isdigit():
        params["user_id"] = uid
    else:
        params["user_ids"] = uid

    req = requests.get("https://api.vk.com/method/users.get", params=params)


if __name__ == '__main__':
    friends_list = get_friends_list('id157049879')
    for friend in friends_list:
        print(friend)

    res = calc_friends_age(friends_list)
    print(res)
