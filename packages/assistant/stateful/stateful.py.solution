import chat

def stateful(args):
  
  inp = args.get("input", "")
  out = f"Hello from {chat.MODEL}"
  res = {}
  
  if inp != "":
    # load the history in the chat
    ch = chat.Chat(args)
    #TODO:E4.2 load the history
    import history
    hi = history.History(args)
    hi.load(ch)
    #END TODO
    # add a message and save it 
    msg = f"user:{inp}"
    ch.add(msg)
    print(ch.messages)
    out = ch.complete()
    # complete, save the assistant and return the id
    #TODO:E4.2 save the message and the state
    # return the id as state field in the response
    hi.save(msg)
    hi.save(f"assistant:{out}")
    res['state'] = hi.id()
    #END TODO

  res['output'] = out
  return res
