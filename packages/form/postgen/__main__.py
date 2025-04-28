#--param OLLAMA_HOST $OLLAMA_HOST
#--param AUTH $AUTH
#--kind python:default
#--web true

import postgen
def main(args):
  return { "body": postgen.postgen(args) }
