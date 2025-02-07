import os
import redis
import shlex
import json

def to_string(response):
    if response is None:
        return "None"  # For null responses
    elif isinstance(response, bytes):
        return response.decode()  # Decode byte strings
    elif isinstance(response, (list, tuple)):
        return "[" + ", ".join(to_string(item) for item in response) + "]"
    else:
        return str(response)  # For integers, booleans, etc.


rd = None
prefix = "error:"

def cache(args):
  global rd, prefix
  if not rd:
    rd = redis.from_url(args.get("REDIS_URL", os.getenv("REDIS_URL")))
    prefix = args.get("REDIS_PREFIX", os.getenv("REDIS_PREFIX"))
  
  cmd = shlex.split(args.get("input", ""))
  
  res = "Please provide a redis command."
  if len(cmd) > 0:
    try:
      res = rd.execute_command(*cmd)
    except Exception as e:
      res = str(e)
    
  return { "output": to_string(res) }
