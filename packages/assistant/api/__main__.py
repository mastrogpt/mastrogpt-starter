#--kind python:default
#--web true
#--param OLLAMA_HOST $OLLAMA_HOST
#--param AUTH $AUTH
import api
def main(args):
  return { "body": api.api(args) }
