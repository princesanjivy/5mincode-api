import json

import redis


class Memstore:
    def __init__(self):
        self.memstore = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True,
        )

    def set(self, key: str, value):
        json_data = json.dumps(value)
        result = self.memstore.set(key, json_data)
        if not result:
            return {"message": "set operation failed"}

        return {"message": None}

    def get(self, key):
        json_data = self.memstore.get(key)
        if json_data is None:
            return None
        value = json.loads(json_data)
        return value

    def hset(self, name: str, key: str, value):
        json_data = json.dumps(value)
        result = self.memstore.hset(name, key, json_data)
        if not result:
            return {"message": "hset operation failed"}

        return {"message": None}

    def hget(self, name: str, key: str):
        json_data = self.memstore.hget(name, key)
        if json_data is None:
            return None
        value = json.loads(json_data)
        return value

    def close(self):
        self.memstore.close()
