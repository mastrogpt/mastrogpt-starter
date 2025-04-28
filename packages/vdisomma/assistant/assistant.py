#--kind python:default
#--web true
#--param OLLAMA_HOST $OLLAMA_HOST
#--param AUTH $AUTH

import os
import openai
import json
import socket
import traceback

model: str = "llama3.1:8b"
stream : bool = True

def configuration (args):
  # Client configuration.
  host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))  
  api_key = args.get("AUTH", os.getenv("AUTH"))
  base_url = f"https://{api_key}@{host}/v1"
  client = openai.OpenAI(base_url = base_url, api_key=api_key)
  # Socket configuration.
  return client

def stream_creation(args, lines):
  sock = args.get("STREAM_HOST", "localhost")
  port = int(args.get("STREAM_PORT", 3000))
  out: str = ""
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((sock, port))
    try:
      for line in lines:
        cont = line.choices[0].delta.content
        if cont:
          print('content:', cont)
          msg = {"output": cont}
          s.sendall(json.dumps(msg).encode("utf-8"))
          out += str(cont)
  #; print(line, end='')
    except Exception as e:
      traceback.print_exc(e)
      out = str(e)
  return out 

def assistant(args):
  client = configuration(args)
  # Implementazione dell'assistant.
  output: str = "Ciao, sono il tuo assistant. In cosa posso esserle di aiuto?"
  content: str = "Capitale d'Italia" 
  if content:
    message: dict = {"role": "user", "content": content}
    #messages : list[dict] = [message_1, message_2]
    res = client.chat.completions.create(model=model, messages=[message], stream=stream)
    if stream:
      output: str = stream_creation(args, res)
    else:
      output: str = res.choices[0].message.content
  result: dict = {"output": output}
  return result

def main(args):
  output: dict = assistant(args)
  result = { "body": output} 
  return result