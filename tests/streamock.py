import socket, threading, time

result = b''
server = None

def args(args={}):
    global server
    if server:
        server.close()
        server = None
    args["STREAM_HOST"] = "127.0.0.1"
    args["STREAM_PORT"] = str(9999+int(time.time()) % 20000)
    return args

def loop():
    global server, result
    client, _ = server.accept()
    result = b''
    while True:
        try:
            data = client.recv(1024)
            if data:
                result += data
            else: 
                break
        except Exception as e:
            print(str(e))
            break

def start(args):
    global server
    stream = (args.get("STREAM_HOST"), int(args.get("STREAM_PORT")))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.settimeout(5)
    server.bind(stream)
    server.listen(5)
    thread = threading.Thread(target=loop)
    thread.start()
    return thread

def stop(thread):
    global result, server
    thread.join()
    server.close()
    return result
