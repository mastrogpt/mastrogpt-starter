import os, re, requests as req
import json, socket, traceback, time
import vdb
import bucket
import base64

MODELS = {
  "P": "phi4:14b",
  "L": "llama3.1:8b",
  "M": "mistral:latest"
}

USAGE = '''Salve, sono il suo RAG assistant. Le chiedo di inserire la configurazione per il RAG nel formato:
[Model][Size][Collection][Domanda], dove:
i) Model: modello llm per il RAG. Può scegliere tra i seguenti:
    P: "phi4:14b",
    L: "llama3.1:8b",
    M: "mistral:latest"
ii) Size: numero di documenti da estarre.
ii) Collection: la collection da cui cercare.
iv)  Domanda: contesto richiesto '''
MODELS = {
  "P": "phi4:14b",
  "L": "llama3.1:8b",
  "M": "mistral:latest"
}

def parse_query(s):
    pattern = r'^(\[[^\[\]]+\])+$'
    result = dict()
    matching = bool(re.match(pattern, s))
    if matching:
        opt = re.findall(r'\[(.*?)\]', s)
        model = MODELS[str(opt[0])] 
        size = int(opt[1]) 
        collection = str(opt[2]) 
        question = str(opt[3])
        result = {'model': model, 'size': size, 'collection': collection, 'question': question}
    else:
        print('La configurazione inserita non è corretta. Ritenti')    
    return result    

def streamlines(args, lines):
  sock = args.get("STREAM_HOST")
  port = int(args.get("STREAM_PORT") or "0")
  out = ""
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    if sock:
      s.connect((sock, port))
    try:
      for line in lines:
        time.sleep(0.1)
        msg = {"output": line }
        out += line
        if sock:
          s.sendall(json.dumps(msg).encode("utf-8"))
    except Exception as e:
      traceback.print_exc(e)
      out = str(e)
    if sock:
      s.close()
  return out

def stream(args, lines):
  sock = args.get("STREAM_HOST")
  port = int(args.get("STREAM_PORT") or "0")
  out = ""
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    if sock:
      s.connect((sock, port))
    try:
      for line in lines:
        dec = json.loads(line.decode("utf-8")).get("response")
        msg = {"output": dec }
        out += dec
        if sock:
          s.sendall(json.dumps(msg).encode("utf-8"))
    except Exception as e:
      traceback.print_exc(e)
      out = str(e)
    if sock:
      s.close()
  return out

def llm(args, model, prompt):
  host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
  auth = args.get("AUTH", os.getenv("AUTH"))
  url = f"https://{auth}@{host}/api/generate"

  msg = {"model": model, "prompt": prompt, "stream": True}
  lines = req.post(url, json=msg, stream=True).iter_lines()
  result = stream(args, lines) 
  return result

def upload_description(args, opts):
    question = opts.get('question', '')
    prompt = 'Non è stata aggiunta alcuna domanda: non è possibile continuare con la richiesta.'
    if question:
      db = vdb.VDB(args, opts)
      db_search = db.search(question)
      searche_results = sorted(db_search, key = lambda x: x['dist'])
      entities = [x for x in searche_results if x['url']]
      prompt = 'Considera il seguente testo'
      urls = str()
      texts = list()
      urls = list()
      url_s3 = 'Di seguito i nomi delle immagini memorizzate in S3:'
      for entity in entities:
          text = entity.get('text', '')
          if text:
            texts.append(text.strip())
          url = entity.get('url', '')
          if url:
            urls.append(url.strip())
      url_s3 += ';'.join(urls)
      prompt += ' '.join(texts)
    return prompt, url_s3

def rag(args):
  state = args.get('state', '')
  inp = args.get('input', "")
  next_state = state
  out = str()
  url = str()
  if not state:
    out = USAGE
    next_state = 'waiting_state'
  elif state == 'waiting_state':
    opts = parse_query(inp)
    prompt, url = upload_description(args, opts)
    model = opts.get('model', "mistral:latest")
    prompt += 'La risposta deve essere di media lunghezza.'
    out = llm(args, model, prompt)
    out += url
  result = {'output': out, 'state': str(next_state)}
  return result 
