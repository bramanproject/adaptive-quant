# utils/cache.py

import time


class Cache:

    def __init__(self):

        self.storage = {}

    def get(self, key):

        if key not in self.storage:
            return None

        value, expire = self.storage[key]

        if expire < time.time():

            del self.storage[key]

            return None

        return value

    def set(self, key, value, ttl=300):

        self.storage[key] = (

            value,

            time.time() + ttl

        )

    def clear(self):

        self.storage.clear()
