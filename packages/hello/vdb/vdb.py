import os, pymilvus
from pymilvus import MilvusClient, Function, FunctionType, DataType
import embed

COLLECTION="test"
LIMIT=5

vdb_db = None

def vdb_init(args):
    global vdb_db
    if vdb_db is None:
      uri = f"http://{args.get("MILVUS_HOST", os.getenv("MILVUS_HOST"))}"
      token = args.get("MILVUS_TOKEN", os.getenv("MILVUS_TOKEN"))    
      db_name = args.get("MILVUS_DB_NAME", os.getenv("MILVUS_DB_NAME"))
      vdb_db = MilvusClient(uri=uri, token=token, db_name=db_name)
    
    if "drop_collection" in args:
      vdb_db.drop_collection(args.get("drop_collection"))
      
    if not COLLECTION in vdb_db.list_collections():
      schema = vdb_db.create_schema()
      schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True, auto_id=True)
      schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=embed.DIMENSION)
      schema.add_field(field_name="embeddings", datatype=DataType.FLOAT_VECTOR, dim=embed.DIMENSION)
      
      #bm25_function = Function(name="text_bm25_emb", input_field_names=["text"], output_field_names=["sparse"], function_type=FunctionType.BM25)
      #schema.add_function(bm25_function)
      
      index_params = vdb_db.prepare_index_params()
      index_params.add_index("embeddings", index_type="AUTOINDEX", metric_type="IP")
      #index_params.add_index(field_name="sparse", index_type="AUTOINDEX",  metric_type="BM25")
      vdb_db.create_collection(collection_name=COLLECTION, schema=schema, index_params=index_params)

    return vdb_db

def vdb(args):
  llm = embed.url(args)
  db = vdb_init(args)
  
  inp = args.get('input', "")
  out = f"Start with '*' to search in collection '{COLLECTION}'.\nStart with '!' to search and remove.\nThe text you type will be inserted for search.\nLimit for search and remove is {LIMIT}"
  search_params = { 'params': {'drop_ratio_search': 0.2} }

  if inp.startswith("*"):
      if len(inp) >1:
        vec = embed.embed(llm, inp[1:])
        res = db.search(collection_name=COLLECTION, search_params={"metric_type":"IP"}, limit=LIMIT,
                  anns_field="embeddings", data=[vec],  output_fields=["text"] )
        if len(res[0]) > 0:
          out = "Found (ordered by IP distance):\n"
          for item in res[0]:
            text = item.get("entity", {}).get("text", "")
            dist = item.get('distance', 0)
            out += f"- ({dist:.2f}) {text}\n"
        else:
          out = "Not found"
      else:
        out = "Please specify a not empty search string."
  elif inp.startswith("!"):
      if len(inp) >1:
        inp = inp[1:]
        ids = []
        qit = db.query_iterator(collection_name=COLLECTION, batchSize=2, output_fields=["text"])
        res = qit.next()
        out ="Deleting:\n"
        while len(res) > 0:
          for ent in res:
            text = ent.get('text') 
            if text.find(inp) != -1:
               ids.append(ent.get('id'))
               out += f"- {text}\n"
          res = qit.next()
        res = db.delete(collection_name=COLLECTION, ids=ids)
        out += f"Deleted: {res['delete_count']}\n"      
      else:
        out = "Please specify a not empty delete substring."
  elif len(inp) >0:
    vec = embed.embed(llm, inp)
    r = db.insert(COLLECTION, [{"text": inp, "embeddings": vec}])
    out = f"OK: {r}" if r.get("insert_count", 0) == 1 else f"ERROR: {r}"
  
  return { "output":  out }

