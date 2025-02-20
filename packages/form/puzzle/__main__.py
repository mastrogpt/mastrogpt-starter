#--kind python:default
#--web true
#--param OLLAMA_HOST $OLLAMA_HOST
#--param AUTH $AUTH

import puzzle
def main(args):
  return { "body": puzzle.puzzle(args) }
