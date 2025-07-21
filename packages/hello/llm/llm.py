import os, requests as req
MODEL="llama3.1:8b"

url = None

def llm(args):
  global url
  if  url is None:
    host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
    auth = args.get("OLLAMA_TOKEN", os.getenv("AUTH"))
    url =  f"https://{auth}@{host}/api/generate"
  out = f"Welcome to {MODEL}"
  inp = args.get("input")
  if inp:
    msg = { "model": MODEL, "prompt": inp, "stream": False }
    res = req.post(url, json=msg).json()
    out = res.get("response", "error")
  
  return { "output": out }
