import socket
import time
import json

def stream(args):
    print("hello")
    inp = args.get("input")
    if host := args.get("STREAM_HOST"):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, int(args.get("STREAM_PORT"))))
                for c in inp:
                    msg = {"output": "Char '%c' ASCII %d\n" %(c, ord(c))} 
                    s.sendall(json.dumps(msg).encode('utf-8'))
                    time.sleep(1)
                s.sendall(b"{}")
        except:
            pass
                
    return {"output": "Returning ASCII char for the input.", "streaming": True}
