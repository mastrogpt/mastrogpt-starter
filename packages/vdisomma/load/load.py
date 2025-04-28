import vdb
import vision
from datetime import datetime

USAGE = f"""Ciao, sono il tuo database vettoriale. Le opzioni possibili sono:
- Scegli "Create" per creare una collection
- Scegli "Insert" per inserire dati.
- Scegli "Search" per cercare una stringa. 
- Scegli "Delete" per cancellare una collection.
- Scegli "List"   per visualizzare la lista di collections presenti. 
"""

def load(args):
    db = vdb.VDB(args)
    state = args.get("state", "")
    inp = args.get("input", "")
    print('inp:', inp)
    print('state')
    out = USAGE
    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    next_state = ""  # Stato da restituire alla prossima iterazione
    result = 'Ok'
    if not state:   
        # Primo messaggio o reset
        out = USAGE
        next_state = "waiting_command"

    elif state == "waiting_command":
        if inp.lower().startswith("create"):
            out = db.setup()
            next_state = ""
        elif inp.lower().startswith("insert"):
            out = "Inserisca il testo da caricare"
            next_state = "waiting_insert_data"
        elif inp.lower().startswith("search"):
            out = "Scriva il testo da cercare:"
            next_state = "waiting_search_data"
        else:
            out = "Comando non riconosciuto. " + USAGE
            next_state = "waiting_command"

    elif state == "waiting_insert_data":
        url = f'upload/{timestamp}.png'
        print('url:', url)
        res = {}
        # Esempio formato input: "testo da salvare/https://link.it"
        try:
            if isinstance(inp, str):
                result = db.insert(inp, url)
                if result:
                    out = f"Inserimento riuscito."
                else:
                    out = "Inserimento fallito."
        except Exception as e:
            out = f"Errore durante l'inserimento: {str(e)}"
            next_state = "waiting_command"

    elif state == "waiting_search_data":
        search_field = inp[:20]
        try:
            results = db.search(search_field)
            if not results:
                out = "Nessun risultato trovato."
            else:
                out = "Risultati trovati:\n"
                for r in results:
                    out += f"{r['text']}\n {r['url']}\n Similarità: {r['dist']:.2f}\n"
        except Exception as e:
            out = f"Errore nella ricerca: {str(e)}"
        next_state = "waiting_command"

    result = {'output': out, 'state': next_state}
    return result
