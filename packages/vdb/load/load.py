import vdb

USAGE = f"""Welcome to the Vector DB Loader.
Write text to insert in the DB.
Start with * to do a vector search in the DB.
Start with ! to remove text with a substring.
"""

def load(args):
  collection = args.get("COLLECTION", "default")
  out = f"{USAGE}Current colletion is {collection}"
  inp = str(args.get('input', ""))
  db = vdb.VectorDB(args)
  db.setup()
  
  if inp.startswith("*"):
    if len(inp) == 1:
      out ="please specify a search string"
    else:
      res = db.vector_search(inp[1:])
      if len(res) > 0:
        out = f"Found:\n"
        for i in res:
          out += f"({i[0]:.2f}) {i[1]}\n"
      else:
        out = "Not found"
  elif inp.startswith("!"):
    count = db.remove_by_substring(inp[1:])
    out = f"Deleted {count} records."
  elif inp != '':
    res = db.insert(inp)
    out = "Inserted " 
    out += " ".join([str(x) for x in res.get("ids", [])])

  return {"output": out}
  
