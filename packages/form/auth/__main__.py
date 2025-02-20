#--kind python:default
#--web true
#--param REDIS_URL $REDIS_URL
#--param REDIS_PREFIX $REDIS_PREFIX

import auth
def main(args):
  return { "body": auth.auth(args) }
