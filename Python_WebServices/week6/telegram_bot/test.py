import json

import collections
import redis
import os

# r = redis.StrictRedis(host='localhost', port=6379, db=0)
redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379')
r = redis.Redis.from_url(redis_url)
for key in r.scan_iter("*"):
    print("key:", key)
    # r.delete(key)


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
