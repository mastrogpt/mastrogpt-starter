import os
import vdb
import time
import re
import requests as req
from bs4 import BeautifulSoup
from urllib.parse import urljoin

#MODEL = "gemma2:9b"
#MODEL = "mistral:latest"
MODEL = "mistral:latest"
USAGE = f"""Ciao, sono il tuo Webrag. Le opzioni possibili sono:
Digita https:// per indicizzare un sito
Digita una domanda. """

def summarize(args, content):
    host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))  
    auth = args.get("AUTH", os.getenv("AUTH"))
    base = f"https://{auth}@{host}/"
    url = f"{base}/api/generate"
    msg = {"model": MODEL, "prompt": f"Very short summary of {content}", "stream": False}
    try:
        res = req.post(url, json=msg, timeout=10).json()
        content = res.get("response", "error")
    except Exception as e:
        content = str(e)
    return content

def text_extraction(args, url):
    try:
        response = req.get(url, timeout=10)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "footer", "noscript"]):
            tag.decompose()
        content = soup.get_text(separator=' ')
        text = re.sub(r'\s+', ' ', content).strip()
        content = summarize(args, text)
    except Exception as e:
        content = str(e)
    print('content:', content)
    return content

def urls_extraction(url):
    try:
        response = req.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        urls = []
        for link in soup.find_all("a", href=True):
            full_url = urljoin(url, link["href"])
            urls.append(full_url)
    except Exception as e:
        print(str(e))        
    if len(urls) > 10:
        urls = urls[:10]
    return urls    

def webrag(args):
    db = vdb.VDB(args)
    db.setup()
    out = ''
    inp = str(args.get("input", ""))
    if inp == '':
        out = USAGE
    elif inp.startswith('https'):
        start = time.time()
        content = text_extraction(args, inp)
        end = time.time()
        print('durata:', end - start)
        result = db.insert(inp, content)
        if result:
            out = 'Sito caricato con successo'
        else:
            out = 'Errore di caricamento'    
    else:
        searches = db.search(inp)
        texts = [search['content'] for search in searches]
        urls = [search['url'] for search in searches]
        out = '\n'.join(texts)
        url = '\n'.join(urls)
        out += f'\n Per maggiori informazioni potete consultare le seguenti pagine {url}'
    return { "output": out}
