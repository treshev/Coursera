import redis
import json
import datetime

r = redis.StrictRedis(host='localhost', port=6379, db=0)
for key in r.scan():
    print(key)

user_id = '343143713'
user = r.get(user_id)
print(user)

user_state = 'USER_STATE_343143713'
user = r.get(user_state)
print(user)

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