#--kind python:default
#--web true
#--param REDIS_URL $REDIS_URL
#--param REDIS_PREFIX $REDIS_PREFIX
#--param OLLAMA_HOST $OLLAMA_HOST
#--param AUTH $AUTH

import stateful
def main(args):
  return { "body": stateful.stateful(args) }
