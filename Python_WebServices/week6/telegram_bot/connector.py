import datetime
import json
from collections import defaultdict, OrderedDict
import os

import redis

START, ADD_ADDRESS, IS_PHOTO_NEEDED, ADD_PHOTO, IS_LOCATION_NEEDED, ADD_LOCATION, END = range(7)
USER_STATE = defaultdict(lambda: START)
USER_DATA = {}


class Connector:
    def get_user_data(self, chat_id):
        raise NotImplementedError

    def update_user_data(self, chat_id, key, value):
        raise NotImplementedError

    def commit_user_data(self, chat_id):
        raise NotImplementedError

    def delete_user_data(self, chat_id):
        raise NotImplementedError

    def get_state(self, chat_id):
        raise NotImplementedError

    def update_state(self, chat_id, state):
        raise NotImplementedError


class RedisConnector(Connector):
    redis_connection = None

    def get_redis_connection(self):
        if self.redis_connection is None:
            redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379')
            print('ALTR: Redis url is: ', redis_url)
            self.redis_connection = redis.Redis.from_url(redis_url)
            # self.redis_connection = redis.StrictRedis(host='localhost', port=6379, db=0)
        return self.redis_connection

    def get_user_data(self, chat_id):
        r = self.get_redis_connection()
        user_binary_data = r.get(chat_id)
        if user_binary_data:
            user_data = json.loads(user_binary_data)
            ordered_list = OrderedDict(sorted(user_data.items(), reverse=True))
            return ordered_list
        else:
            return None

    def update_user_data(self, chat_id, key, value):
        r = self.get_redis_connection()
        user = r.get(chat_id)
        if not user:
            user_data = {"current": {key: value}}
        else:
            user_data = json.loads(user)
            if isinstance(user_data['current'], str):
                user_data["current"] = {key: value}
            else:
                user_data["current"][key] = value
        print(user_data)
        r.set(chat_id, json.dumps(user_data))

    def commit_user_data(self, chat_id):
        r = self.get_redis_connection()
        user = r.get(chat_id)
        if user:
            user_data = json.loads(user)
            user_data[str(datetime.datetime.now())] = user_data.get('current', None)
            user_data['current'] = ''
            r.set(chat_id, json.dumps(user_data))

    def delete_user_data(self, chat_id):
        r = self.get_redis_connection()
        r.delete(chat_id)

    def get_state(self, chat_id):
        r = self.get_redis_connection()
        user_state_data = r.get("USER_STATE_{}".format(chat_id))
        user_data = int(user_state_data) if user_state_data else None
        return user_data

    def update_state(self, chat_id, state):
        r = self.get_redis_connection()
        r.set("USER_STATE_{}".format(chat_id), state)


class InMemoryConnector(Connector):

    def get_user_data(self, chat_id):
        return USER_DATA.get(chat_id.chat.id, None)

    def update_user_data(self, chat_id, key, value):
        if chat_id not in USER_DATA:
            USER_DATA[chat_id] = {"current": {key: value}}
        else:
            USER_DATA[chat_id]["current"][key] = value

    def commit_user_data(self, chat_id):
        if chat_id in USER_DATA:
            USER_DATA[chat_id][str(datetime.datetime.now())] = USER_DATA[chat_id].get('current', None)
            USER_DATA[chat_id]['current'] = {}

    def delete_user_data(self, chat_id):
        USER_DATA.pop(chat_id, "Empty")

    def get_state(self, chat_id):
        return USER_STATE[chat_id]

    def update_state(self, chat_id, state):
        USER_STATE[chat_id] = state
