#--kind python:default
#--web true
#--param OLLAMA_HOST $OLLAMA_HOST
#--param AUTH $AUTH
#END TODO

import stateless
def main(args):
  return { "body": stateless.stateless(args) }
