#--kind python:default
#--web true
#--param REDIS_URL $REDIS_URL
#--param REDIS_PREFIX $REDIS_PREFIX
#--kind python:default

import os
import cache

def main(args):
  return { "body": cache.cache(args) }
