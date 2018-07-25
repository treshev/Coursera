import json

import collections
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)
for key in r.scan_iter("*"):
    print("key:", key)
    # r.delete(key)


def handle_list_command(places_list):
    if places_list:
        i = 1
        for place in places_list:
            if 'current' not in place:
                item = places_list[place]
                title_text = "<b>{}</b>. {}".format(i, item["address"])
                print(title_text)

                if "file_id" in item.keys():
                    print(item["file_id"])

                if "location" in item.keys():
                    location = item["location"]
                    print(location[0], location[1])
                if i < 10:
                    i += 1
                else:
                    return

    else:
        print("Bla bla")


user_id = '343143713'
user = json.loads(r.get(user_id))
print("user: ", sorted(user.items(), reverse=True))
ordered_list = collections.OrderedDict(sorted(user.items(), reverse=True))
handle_list_command(ordered_list)

# user_state = 'USER_STATE_343143713'
# user = json.loads(r.get(user_state))
# print("User State: ", user)


# r.delete("343143713")
# r.delete("USER_STATE_343143713")
#
# user_data = json.loads(user)
# user_data["current"]["photo"] = "photo1"
#
# r.set(user_id, json.dumps(user_data))
#
# user = r.get(user_id)
# print(user)
#
# user = r.get(user_id)
# user_data = json.loads(user)
# print("User_data: ", user_data)
# user_data[str(datetime.datetime.now())] = user_data.pop('current', None)
# print("User_data after pop: ", user_data)
# r.set(user_id, json.dumps(user_data))
#
# print(r.get(user_id))
#
# r.delete("343143713")
