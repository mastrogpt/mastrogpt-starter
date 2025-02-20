import os, requests as req, json, socket

MODEL="llama3.1:8b"
#MODEL="deepseek-r1:32b"

def url(args):
  host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
  auth = args.get("AUTH", os.getenv("AUTH"))
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
        dec = json.loads(line.decode("utf-8")).get("response", "error")
        dec = dec.replace("<think>","[think]")
        dec = dec.replace("/<think>","[/think]")
        msg = {"output": dec}
        out += dec
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
    if inp == "llama":
      MODEL = "llama3.1:8b"
      inp = "Who am i"
    elif inp == "deepseek":
      MODEL ="deepseek-r1:32b"
      inp = "Who am i"
    msg = { "model": MODEL, "prompt": inp, "stream": True }
    lines = req.post(llm, json=msg, stream=True).iter_lines()
    out = stream(args, lines)
  return { "output": out, "streaming": True}
