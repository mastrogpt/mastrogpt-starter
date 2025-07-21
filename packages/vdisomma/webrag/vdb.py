import os
import requests as req
from pymilvus import MilvusClient, DataType

COLLECTION = "test"
#DIMENSION = 1024
DIMENSION = 768
#MODEL = "mxbai-embed-large:latest"
MODEL = "nomic-embed-text:v1.5" #problemi con la dimensione
#MODEL = "mxbai-embed-large:335m" da rivedere


class VDB:
    def __init__(self, args):
        uri = f"http://{args.get('MILVUS_HOST', os.getenv('MILVUS_HOST'))}"
        token = args.get("MILVUS_TOKEN", os.getenv("MILVUS_TOKEN"))    
        db_name = args.get("MILVUS_DB_NAME", os.getenv("MILVUS_DB_NAME"))
        self.client = MilvusClient(uri=uri, token=token, db_name=db_name)

        host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
        auth = args.get("OLLAMA_TOKEN", os.getenv("AUTH"))
        self.url = f"https://{auth}@{host}/api/embeddings"

        self.collection = args.get("COLLECTION", COLLECTION)

    def setup(self):
        client = self.client
        collection = self.collection
        if not client.has_collection(collection):
            schema = client.create_schema()
            schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True, auto_id=True)
            schema.add_field(field_name="url", datatype=DataType.VARCHAR, max_length=512) 
            schema.add_field(field_name="content", datatype=DataType.VARCHAR, max_length=2048) 
            schema.add_field(field_name="embeddings", datatype=DataType.FLOAT_VECTOR, dim=DIMENSION)

            index_params = client.prepare_index_params()
            index_params.add_index("embeddings", index_type="AUTOINDEX", metric_type="IP")
            client.create_collection(collection_name=collection, schema=schema, index_params=index_params)
        
    def embed(self, text):
        url = self.url
        msg = {"model": MODEL, "prompt": text, "stream": False}
        res = req.post(url, json=msg).json()
        return res.get('embedding', [])

    def insert(self, url, text):
        client = self.client
        collection = self.collection
        result = client.has_collection(collection)
        if result: 
            vec = self.embed(text)
            entity = {}
            try:
                entity = {"url": url, 'content': text, "embeddings": vec}
                result = client.insert(self.collection, entity)
                if result:
                    print('Caricamento effettuato su Milvus')
            except Exception as e:
                print(f'Errore di caricamento: {e}')
            return result        

    def search(self, text):
        client = self.client
        collection = self.collection
        # Genera embedding della query
        embed = self.embed(text)
        data = [embed]
        # Parametri per la ricerca
        params = {"metric_type": "IP"}  # IP = Inner Product
        anns_field = "embeddings"       # campo che contiene l’embedding del contenuto
        output_fields = ["url", "content"]
        # Search in Milvus
        results = client.search(collection_name=collection, data=data, anns_field=anns_field,
                                search_param=params, limit= 1, output_fields=output_fields)[0]
        search_result = []
        for item in results:
            entity = item.get("entity", {})
            search_result.append({"dist": item.get("score", 0), "url": entity.get("url", ""), "content": entity.get("content", "")})
        return search_result

    def remove_by_substring(self, inp):
        cur = self.client.query_iterator(collection_name=self.collection, 
                batchSize=2, output_fields=["text"])
        res = cur.next()
        ids = []
        while len(res) > 0:
            for ent in res:
                if ent.get('text', "").find(inp) != -1:
                    ids.append(ent.get('id'))
            res = cur.next()
        if len(ids) >0:
            res = self.client.delete(collection_name=self.collection, ids=ids)
            return res['delete_count']
        return 0

    def delete(self):
        client = self.client
        collection = self.collection
        result = client.has_collection(collection) 
        if result:
            client.drop_collection(collection)

    
