import redis
import uuid
import os
from urllib.parse import urlparse, urlunparse

class History:
    
    def __init__(self, args):
        prefix = args.get("REDIS_PREFIX", os.getenv("REDIS_PREFIX"))
        redis_url = args.get("REDIS_URL", os.getenv("REDIS_URL"))
        self.cache = redis.from_url(redis_url)
        self.queue = args.get("state")
        if self.queue is None:
            self.queue = prefix+"assistant:"+str(uuid.uuid4())
            
    def id(self):
        return self.queue

    def save(self, msg):
        self.cache.rpush(self.queue, msg)
        self.cache.expire(self.queue, 86400)
        return self.queue
        
    def load(self, ch):
        for item in self.cache.lrange(self.queue, 0, -1):
            ch.add(item.decode('utf-8'))
    

            
