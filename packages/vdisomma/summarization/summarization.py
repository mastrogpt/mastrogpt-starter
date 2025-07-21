import requests as req
import os
import json
import time

model = "mistral:latest"
def summarization(args, el):
  host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))  
  auth = args.get("AUTH", os.getenv("AUTH"))
  base = f"https://{auth}@{host}/"
  link = f"{base}/api/generate"
  with open("nuvolaris_titles.json", "r", encoding="utf-8") as file:
   dati = json.load(file)
  result = []
  #for el in dati:
  url = el.get('url', '')
  content = el.get('content', '')
  if len(content) > 1500:
      msg = { "model": model, "prompt": f'Riassumi {content}', "stream": False}
      res = req.post(link, json=msg).json()
      out = res.get('response', 'error')
      content = ' '.join(out.split())
  d = {'url': url, 'content': content}
   #return result
  return { "output": d}  
    