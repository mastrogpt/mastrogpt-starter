#--kind python:default
#--web true
#--param OLLAMA_HOST $OLLAMA_HOST
#--param AUTH $AUTH

import translate
import json

def main(args):
   result = translate.translate(args)
   return result
