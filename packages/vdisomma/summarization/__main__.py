#--kind python:default
#--web true
#--param OLLAMA_HOST $OLLAMA_HOST
#--param AUTH $AUTH

import summarization

model = "mistral:latest"

# Entry point OpenWhisk-style
def main(args):
    return { "body": summarization.summarization(args) }

