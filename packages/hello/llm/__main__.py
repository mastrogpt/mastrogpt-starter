#--kind python:default
#--web true
#--param OLLAMA_HOST $OLLAMA_HOST
#--param OLLAMA_TOKEN $AUTH
import llm
def main(args):
  return { "body": llm.llm(args) }
