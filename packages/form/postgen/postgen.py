MODEL = "llama3.1:8b"
STREAMING = True

USAGE = """I will generate a post on Apache OpenServerless post for you!"""

FORM = [
  {
    "name": "job",
    "label": "What is your job role?",
    "type": "text",
    "required": "true"
  },
  {
      "name": "why",
      "label": "Why do you recommend Apache OpenServerless?",
      "type": "textarea",
      "required": "true"
  },
  {
    "name": "tone",
    "label": "Which tone the post should have?",
    "required": "true",
    "type": "radio",
    "options": ["Formal", "Informal", "Enthusiastic", "Motivational"]
  }
]


import json, socket, traceback
def stream(args, lines):
  
  if type(lines) is str:
    ls = [{"response":x+" "} for x in lines.split(" ")]
    lines = (json.dumps(x).encode('utf-8') for x in ls)
  
  sock = args.get("STREAM_HOST")
  port = int(args.get("STREAM_PORT"))
  out = ""
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((sock, port))
    try:
      for line in lines:
        print(line, end='')
        dec = json.loads(line.decode("utf-8")).get("response")
        msg = {"output": dec }
        out += dec
        s.sendall(json.dumps(msg).encode("utf-8"))
    except Exception as e:
      traceback.print_exc(e)
      out = str(e)
  return out

import os, requests as req
def chat(args, inp):
  host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
  auth = args.get("AUTH", os.getenv("AUTH"))
  url = f"https://{auth}@{host}/api/generate"
  msg = { "model": MODEL, "prompt": inp, "stream": STREAMING}
  if STREAMING:
    lines = req.post(url, json=msg, stream=True).iter_lines()
    out = stream(args, lines)
  else:
    res = req.post(url, json=msg).json()
    out = res.get("response", "error")
  
  return  out
 
def postgen(args):
  #print(args)

  res = {"streaming": STREAMING}
  inp = args.get("input", "")
  out = USAGE

  #print("TYPE", type(inp))

  if inp == "":
     out = USAGE
     res['form'] = FORM

  elif type(inp) is dict and "form" in inp:
      data = inp["form"]
      for field in data.keys():
        print(data[field])

      inp = f"""Generate a post promoting Apache OpenServerless.
Your job role is {data['job']}.
The reason because you are using Apache OpenServerless is {data['why']}.
The tone of the post should be {data['tone']}.
"""
      out = chat(args, inp)

  elif inp != "":
    out = chat(args, inp)

  res['output'] = out
  print(res)
  return res
