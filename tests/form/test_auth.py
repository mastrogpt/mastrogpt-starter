import sys
sys.path.append("packages/form/auth")
import os, redis, auth

def test_auth():
    user = "pinocchio"
    rd = redis.from_url(os.getenv("REDIS_URL"))
    key = f"{os.getenv("REDIS_PREFIX")}TOKEN:{user}"
    secret = "123stella"
    rd.set(key, secret)
    
    args = {}
    assert auth.unauthorized(args)

    args = { "token": f"{user}:_"}
    assert auth.unauthorized(args)

    args = { "token": f"{user}:{secret}"}
    assert not auth.unauthorized(args)
  
    
