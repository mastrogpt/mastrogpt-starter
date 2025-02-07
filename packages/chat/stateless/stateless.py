import os, requests as req, json, socket

MODEL="llama3.1:8b"
#MODEL="deepseek-r1:32b"

def url(args):
  #TODO:E2.1
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
        #print(line, end='')     
        #TODO:E2.2 fix this streaming implementation
        # line is a json string and you have to extract only the "response" field
        #msg = {"output": line.decode("utf-8")}
        #out += str(line)

        res = json.loads(line.decode("utf-8"))["response"]
        out += res
        msg = {"output": res}

        #END TODO
        s.sendall(json.dumps(msg).encode("utf-8"))
    except Exception as e:
      traceback.print_exc(e)
      out = f"{str(e)} res:{res} out: {out} msg:{msg}"
  return out

def stateless(args):
  global MODEL
  llm = url(args)
  out = f"Welcome to {MODEL}"
  inp = args.get("input", "")
  #return({"output": f"Arg:{args}", "streaming": False})
  match str(inp).lower():
      case "llama":
        MODEL="llama3.1:8b"
        out = f"Llama version -> {MODEL} Loaded..."
        return { "output": out, "streaming": False}
      case "deepseek":
        MODEL="deepseek-r1:32b"
        out = f"Deepseek version -> {MODEL} Loaded..."
        return { "output": out, "streaming": False}
      case "":
        out = f"Welcome to the chat with {MODEL}, if you want you can type Deepseek or Llama to switch model."
        return { "output": out, "streaming": False}
      case _:
        msg = { "model": MODEL, "prompt": inp, "stream": True }
        lines = req.post(llm, json=msg, stream=True).iter_lines()
        out = stream(args, lines)
        return { "output": out, "streaming": True}
  #if inp != "":
    #TODO:E2.3 
    # add if to switch to llama3.1:8b or deepseek-r1:32b
    # on input 'llmama' or 'deepseek' and change the inp to "who are you"
    #END TODO

    #msg = { "model": MODEL, "prompt": inp, "stream": True }
    #lines = req.post(llm, json=msg, stream=True).iter_lines()
    #out = stream(args, lines)
  return { "output": "Honestly we shouldn't be here but... here we are i guess.", "streaming": False}
