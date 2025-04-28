import requests as req
import os

model = "llama3.1:8b"
def translate(args):
  stream: bool = True
  host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))  
  auth = args.get("AUTH", os.getenv("AUTH"))
  base = f"https://{auth}@{host}/"
  url: str = f"{base}/api/generate"
  out: str = f'Ciao, sono {model}. Puoi inserire la frase da tradurre?'
  inp: str = args.get('input', '')
  if inp:
    msg = { "model": model, "prompt": f'Traduci {inp} in Italiano', "stream": stream}
    res = req.post(url, json=msg)
    if not stream:
      answer = res.json()
      out = answer.get('response', 'error')
    else:
      lines: list[str] = [line.decode('utf-8') for line in res.iter_lines()]
      output: str = ''
      for x in lines:
        output += x + ' '
      out = output.strip()  
  return { "output": out}
