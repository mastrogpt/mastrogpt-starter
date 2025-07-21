import os
import requests as req
from pymilvus import MilvusClient, DataType

COLLECTION = "job"
DIMENSION = 1024
MODEL = "mxbai-embed-large:latest"

class VDB:
    def __init__(self, args, opts):
        print('args:', args)
        uri = f"http://{args.get('MILVUS_HOST', os.getenv('MILVUS_HOST'))}"
        token = args.get("MILVUS_TOKEN", os.getenv("MILVUS_TOKEN"))    
        db_name = args.get("MILVUS_DB_NAME", os.getenv("MILVUS_DB_NAME"))
        print('db:', db_name)
        self.client = MilvusClient(uri=uri, token=token, db_name=db_name)

        host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
        auth = args.get("OLLAMA_TOKEN", os.getenv("AUTH"))
        self.url = f"https://{auth}@{host}/api/embeddings"

        self.collection = opts.get('Collection', 'job')
        self.model = opts.get('Model', "llama3.1:8b")
        self.size = opts.get('Size', 2)

    def setup(self):
        client = self.client
        collection = self.collection
        
        schema = client.create_schema()
        schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True, auto_id=True)
        schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=DIMENSION)  # max_length al posto di dim
        schema.add_field(field_name="embeddings", datatype=DataType.FLOAT_VECTOR, dim=DIMENSION)
        schema.add_field(field_name="url", datatype=DataType.VARCHAR, max_length=DIMENSION)  # VARCHAR usa max_length, non dim

        index_params = client.prepare_index_params()
        index_params.add_index("embeddings", index_type="AUTOINDEX", metric_type="IP")
        client.create_collection(collection_name=collection, schema=schema, index_params=index_params)
       
    def embed(self, text):
        url = self.url
        msg = {"model": MODEL, "prompt": text, "stream": False}
        res = req.post(url, json=msg).json()
        result = res.get('embedding', []) 
        return result

    def insert(self, text, url):
        client = self.client
        collection = self.collection
        print('collection_insert:', collection)
        collections = client.list_collections()
        if collection not in collections:
            self.setup()
        result = client.has_collection(collection)
        if result: 
            vec = self.embed(text)
            entity = {}
            try:
                entity = {"text": text, "embeddings": vec, "url": url}
                print('entity:', entity)
                result = client.insert(self.collection, entity)
                if result:
                    print('Caricamento effettuato su Milvus')
            except Exception as e:
                print(f'Errore di caricamento: {e}')    
        return entity

    def search(self, text):
        client = self.client
        collection = self.collection
        size = self.size
        print('collection:', collection)
        collections = client.list_collections()
        if collection not in collections:
            self.setup()
        result = client.has_collection(collection)
        if result:     
            embed = self.embed(text)
            collection_name = self.collection
            data = [embed]
            params = {"metric_type": "IP"}  
            anns_field = "embeddings"
            output_fields = ["text", "url"]

        res = client.search(
            collection_name=collection_name,
            data=data,
            anns_field=anns_field,
            search_param=params,
            limit=size,
            output_fields=output_fields)[0]

        search_result = []
        print('res:', res)
        for item in res:
            dist = item.get('score', 0) or item.get('distance', 0)
            entity = item.get("entity", {})
            search_result.append({
                "dist": dist,
                "text": entity.get("text", ""),
                "url": entity.get("url", "")
            })
        return search_result

    def remove_by_substring(self, inp):
        collection = self.collection
        cur = self.client.query_iterator(collection_name=collection, batchSize=2, output_fields=["text"])
        res = cur.next()
        ids = []
        while len(res) > 0:
            for ent in res:
                if ent.get('text', "").find(inp) != -1:
                    ids.append(ent.get('id'))
            res = cur.next()
        if len(ids) >0:
            res = self.client.delete(collection_name=collection, ids=ids)
            return res['delete_count']
        return 0
    

