import vision
import bucket
import base64
import vdb
from datetime import datetime

FORM = [{"label": "any pics?",
                 "name": "pic",
                 "required": "true",
                 "type": "file"}]

def loader(args):
    inp = args.get("input", "")
    out = "Inserisca l'immagine"
    res = {}
    result = False
    url = ''
    if inp and type(inp) is dict and "form" in inp:
      img = inp.get("form", {}).get("pic", "")
      timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
      filename = f"upload/{timestamp}.jpg"
      # Caricamento delle immagini su S3.
      html = upload_image(args, img, filename)
      if html:
         print("Caricamento dell'immagine effettuato su S3.")
         res['html'] = html
      else:
        print("Caricamento dell'immagine su S3 in errore.")
        return html
      
      # Caricamento delle descrizioni su Milvus.
      entity = upload_description(args, img, filename)
      url = entity['url']; out = entity['text']
      result = True
   
    res['form'] = FORM
    res['output'] = out
    res['esito'] = f"result: {str(result)}"
    res['url'] = url
  
    return res

def upload_image(args, img, filename):
    html = ''
    buc = bucket.Bucket(args)
    decoded_img = base64.b64decode(img)
    result = buc.write(filename, decoded_img)
    if result:
        presigned_url = buc.exturl(filename, 60*60)
        html = f'<img src="{presigned_url}">'
    return html  
   
def upload_description(args, decoded_img, url):
   db = vdb.VDB(args)
   vis = vision.Vision(args)
   text = vis.get_description(decoded_img)
   #print('lunghezza testo:', len(text))
   entity = db.insert(text, url)
   return entity
      
        
        
