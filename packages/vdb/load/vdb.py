import os, requests as req
from pymilvus import MilvusClient, DataType

MODEL="mxbai-embed-large:latest"
DIMENSION=1024
LIMIT=10

class VectorDB:

  def __init__(self, args):
      uri = f"http://{args.get("MILVUS_HOST", os.getenv("MILVUS_HOST"))}"
      token = args.get("MILVUS_TOKEN", os.getenv("MILVUS_TOKEN"))    
      db_name = args.get("MILVUS_DB_NAME", os.getenv("MILVUS_DB_NAME"))
      print('db:', db_name)
      self.client =  MilvusClient(uri=uri, token=token, db_name=db_name)

      host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
      auth = args.get("OLLAMA_TOKEN", os.getenv("AUTH"))
      self.url = f"https://{auth}@{host}/api/embeddings"

      self.collection = 'job' 
      #self.collection = args.get("COLLECTION", "job")
      print('collection:', self.collection)
      self.setup()

  def setup(self, drop=True):
    if drop:
      self.client.drop_collection(self.collection)
      
    if not self.collection in self.client.list_collections():
      schema = self.client.create_schema()
      schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True, auto_id=True)
      schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=DIMENSION)
      schema.add_field(field_name="embeddings", datatype=DataType.FLOAT_VECTOR, dim=DIMENSION)
      
      index_params = self.client.prepare_index_params()
      index_params.add_index("embeddings", index_type="AUTOINDEX", metric_type="IP")
      self.client.create_collection(collection_name=self.collection, schema=schema, index_params=index_params)

  def embed(self, text):
    msg = { "model": MODEL, "prompt": text, "stream": False }
    res = req.post(self.url, json=msg).json()
    return res.get('embedding', [])

  def insert(self, text):
    vec = self.embed(text)
    return self.client.insert(self.collection, {"text":text, "embeddings": vec})

  def vector_search(self, inp, limit=LIMIT):
    vec = self.embed(inp)
    cur = self.client.search(
      collection_name=self.collection,
      search_params={"metric_type": "IP"},
      anns_field="embeddings", data=[vec],
      output_fields=["text"]
    )
    res = []
    if len(cur[0]) > 0:
      for item in cur[0]:
        dist = item.get('distance', 0)
        text = item.get("entity", {}).get("text", "")
        res.append((dist, text))
    return res

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
