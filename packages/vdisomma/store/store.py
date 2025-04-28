import bucket
from PIL import Image
import io
import base64

USAGE = f"""Ciao, sono il tuo S3 storage personale. Le opzioni possibili sono:
- Scegli "Read" per leggere un documento.
- Scegli "Insert" per inserire dati.
- Scegli "Search" per cercare una stringa. 
"""
FORM = [{"label": "any pics?",
                 "name": "pic",
                 "required": "true",
                 "type": "file"}]

def store(args):
  buc = bucket.Bucket(args)
  state = args.get("state", "")
  inp = args.get("input", "")
  out = USAGE
  next_state = ""  # Stato da restituire alla prossima iterazione
  result = 'Ok'
  res = {}
  html = ''
  print('inp:', inp)
  print('state:', state)
  print('next_state:', next_state)
  print('out:', out)
  if not state:
      # Primo messaggio o reset
      out = USAGE
      next_state = "waiting_command"
  elif state == "waiting_command":
     if inp.lower().startswith('read'):
        out = "Inserisca il documento da leggere."
        next_state = "waiting_read_file"
     elif inp.lower().startswith('remove'):
        out = "Inserisca il documento da cancellare."
        next_state = 'waiting_remove_file'
     elif inp.lower().startswith('write'):
        out = "Inserisca il testo da salvare ed il documento dove inserirlo nel formato 'file=testo'."
        next_state = 'waiting_write_file'   
     elif inp.lower().startswith('search'):
        out = "Inserisca il documento da cercare."
        next_state = 'waiting_search_file'                 
     else:
        out = "Comando non riconosciuto. " + USAGE
        next_state = "waiting_command"
    
  elif state == "waiting_read_file":
     #img = buc.read(inp)
     #print('img:', img)
     #out = base64.b64encode(img).decode('utf-8')
     out = f'Ecco il file {inp}'
     presigned_url = buc.exturl(inp, 60*60)
     print('htm:', html)
     html = f'<img src="{presigned_url}">'
  elif state == "waiting_remove_file":  
     out = buc.remove(inp)
  elif state == "waiting_write_file":  
     file, text = inp.split('=')
     out = buc.write(file, text)
  elif state == "waiting_search_file": 
     out = buc.find(inp)     

  res['form'] = FORM if state=="waiting_read_file" else None
  res['output'] = out
  res['esito'] = f"result: {str(result)}"
  res['state'] = str(next_state)
  res['html'] = html
  return res
