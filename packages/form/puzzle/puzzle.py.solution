import re, os, requests as req
#MODEL = "llama3.1:8b"
MODEL = "phi4:14b"

def chat(args, inp):
  host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
  auth = args.get("AUTH", os.getenv("AUTH"))
  url = f"https://{auth}@{host}/api/generate"
  msg = { "model": MODEL, "prompt": inp, "stream": False}
  res = req.post(url, json=msg).json()
  out = res.get("response", "error")
  return  out
 
def extract_fen(out):
  pattern = r"([rnbqkpRNBQKP1-8]+\/){7}[rnbqkpRNBQKP1-8]+"
  fen = None
  m = re.search(pattern, out, re.MULTILINE)
  if m:
    fen = m.group(0)
  return fen

FORM = [
  {
    "name": "queen",
    "label": "With a queen",
    "type": "checkbox",
  },
  {
    "name": "rook",
    "label": "With a rook",
    "type": "checkbox",
  },
  {
    "name": "knight",
    "label": "With a knight",
    "type": "checkbox",
  },
  {
    "name": "bishop",
    "label": "With a bishop",
    "type": "checkbox",
  }
]

def puzzle(args):
  out = "If you want to see a chess puzzle, type 'puzzle'.\nTo display a fen position, type 'fen <fen string>'."
  res = {}
  inp = args.get("input", "")
  if type(inp) is dict and "form" in inp:
    data = inp["form"]
    for field in data.keys():
      print(field, data[field])

    inp = "Generate a chess puzzle in FEN format"
    if data.get("rook"):
      inp += " with a rook"
    if data.get("bishop"):
      inp += " with a bishop"
    if data.get("queen"):
      inp += " with a queen"
    if data.get("knight"):
      inp += " with a knight"
      
    out = chat(args, inp)
    fen = extract_fen(out)
    if fen:
       print(fen)
       res['chess'] = fen
       out = f"[{inp}]\n{out}"
    else:
      out = "Bad FEN position."
  elif inp == "puzzle":
    res['form'] = FORM
  elif inp.startswith("fen"):
    fen = extract_fen(inp)
    if fen:
       out = "Here you go."
       res['chess'] = fen
  elif inp != "":
    out = chat(args, inp)
    fen = extract_fen(out)
    print(out, fen)
    if fen:
      res['chess'] = fen
      out = "Which kind of puzzle do you want?"

  res["output"] = out
  return res
