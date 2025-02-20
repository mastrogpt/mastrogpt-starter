#--web true

import time
def count_to_zero(n):
  while n > 0:
    yield f"{n}...\n"
    n -= 1
    time.sleep(1)
  yield "Go!\n"
  
import json, socket, traceback
def stream(args, lines):
  sock = args.get("STREAM_HOST")
  port = int(args.get("STREAM_PORT"))
  out = ""
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((sock, port))
    try:
      for line in lines:
        msg = {"output": line}
        s.sendall(json.dumps(msg).encode("utf-8"))
        out += str(line) #; print(line, end='')
    except Exception as e:
      traceback.print_exc(e)
      out = str(e)
  return out

def main(args): 
  inp = args.get("input", "")
  out = f"Input a number > 0 to countdown"
  if inp != "":
    try: n = int(inp)
    except: n = 0
    lines = count_to_zero(n)
    out = stream(args, lines)
        
  return { "body": { "output": out, "streaming": True } }
