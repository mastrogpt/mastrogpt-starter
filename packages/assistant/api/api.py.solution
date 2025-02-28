import chat

def api(args):
  inp = args.get("input", "")
  out = f"Hello from {chat.MODEL}"
  if inp != "":
    ch = chat.Chat(args)
    ch.add(f"user:{inp}")
    out = ch.complete()
  #TODO:E4.1 add streaming True
  return { "output": out, "streaming": True }
  #END TODO
