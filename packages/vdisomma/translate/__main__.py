#--kind python:default
#--web true
#--param OLLAMA_HOST $OLLAMA_HOST
#--param AUTH $AUTH

import translate
def main(args):
  result: str = translate.translate(args)
  return { "body": result}
