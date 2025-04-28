import os, requests as req, json, socket

MODEL="llama3.1:8b"
#MODEL="deepseek-r1:32b"

def url(args):
  #TODO:E2.1
  host = ...
  auth = ...
  #END TODO
  base = f"https://{auth}@{host}"
  return f"{base}/api/generate"

import json, socket, traceback
def stream(args, lines):
  sock = args.get("STREAM_HOST")
  port = int(args.get("STREAM_PORT"))
  out = ""
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((sock, port))
    try:
      for line in lines:
        #print(line, end='')     
        #TODO:E2.2 fix this streaming implementation
        # line is a json string and you have to extract only the "response" field
        msg = {"output": line.decode("utf-8")}
        out += str(line)
        #END TODO
        s.sendall(json.dumps(msg).encode("utf-8"))
    except Exception as e:
      traceback.print_exc(e)
      out = str(e)
  return out

def stateless(args):
  global MODEL
  llm = url(args)
  out = f"Welcome to {MODEL}"
  inp = args.get("input", "")
  if inp != "":
    #TODO:E2.3 
    # add if to switch to llama3.1:8b or deepseek-r1:32b
    # on input 'llmama' or 'deepseek' and change the inp to "who are you"
    #END TODO
    msg = { "model": MODEL, "prompt": inp, "stream": True }
    lines = req.post(llm, json=msg, stream=True).iter_lines()
    out = stream(args, lines)
  return { "output": out, "streaming": True}
