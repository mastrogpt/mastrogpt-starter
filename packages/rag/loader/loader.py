import vdb

USAGE = f"""Welcome to the Vector DB Loader.
Write text to insert in the DB. 
Use `@[<coll>]` to select a collection and show the collections.
Use `*<string>` to vector search the <string>  in the DB.
Use `#<limit>`  to change the limit of searches.
Use `!<substr>` to remove text with `<substr>` in collection.
Use `!![<collection>]` to remove `<collection>` (default current) and switch to default.
"""

def loader(args):
  #print(args)
  # get state: <collection>[:<limit>]
  collection = "default"
  limit = 30
  sp = args.get("state", "").split(":")
  if len(sp) > 0 and len(sp[0]) > 0:
    collection = sp[0]
  if len(sp) > 1:
    try:
      limit = int(sp[1])
    except: pass
  print(collection, limit)
  out = f"{USAGE}Current collection is {collection} with limit {limit}"
  db = vdb.VectorDB(args, collection)
  inp = str(args.get('input', ""))
  # select collection
  if inp.startswith("@"):
    out = ""
    if len(inp) > 1:
      collection = inp[1:]
      out = f"Switched to {collection}.\n"
    out += db.setup(collection)
  # set size of search
  elif inp.startswith("#"):
    try: 
      limit = int(inp[1:])
    except: pass
    out = f"Search limit is now {limit}.\n"
  # run a query
  elif inp.startswith("*"):
    search = inp[1:]
    if search == "":
      search = " "
    res = db.vector_search(search, limit=limit)
    if len(res) > 0:
      out = f"Found:\n"
      for i in res:
        out += f"({i[0]:.2f}) {i[1]}\n"
    else:
      out = "Not found"
  # remove a collection
  elif inp.startswith("!!"):
    if len(inp) > 2:
      collection = inp[2:].strip()
    out = db.destroy(collection)
    collection = "default"
  # remove content
  elif inp.startswith("!"):
    count = db.remove_by_substring(inp[1:])
    out = f"Deleted {count} records."    
  elif inp != '':
    out = "Inserted "
    lines = [inp]
    if args.get("options","") == "splitlines":
      lines = inp.split("\n")
    for line in lines:
      if line == '': continue
      res = db.insert(line)
      out += "\n".join([str(x) for x in res.get("ids", [])])
      out += "\n"
  return {"output": out, "state": f"{collection}:{limit}"}
  
