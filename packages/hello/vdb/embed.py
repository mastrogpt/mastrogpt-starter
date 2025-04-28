import os, requests as req
MODEL="mxbai-embed-large:latest"
DIMENSION=1024

def url(args):
    host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
    auth = args.get("OLLAMA_TOKEN", os.getenv("AUTH"))
    url = f"https://{auth}@{host}/api/embeddings"
    return url

def embed(url, inp):    
  msg = { "model": MODEL, "prompt": inp, "stream": False }
  res = req.post(url, json=msg).json()
  out = res.get('embedding', [])
  return out
