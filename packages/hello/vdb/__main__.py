#--docker ghcr.io/sciabarracom/openserverless-runtimes-python:v3.12.2501130900
#--web true
#--param OLLAMA_HOST $OLLAMA_HOST
#--param OLLAMA_TOKEN $AUTH
#--param MILVUS_HOST $MILVUS_HOST
#--param MILVUS_PORT $MILVUS_PORT
#--param MILVUS_DB_NAME $MILVUS_DB_NAME
#--param MILVUS_TOKEN $MILVUS_TOKEN

import vdb
def main(args):
  return { "body": vdb.vdb(args) }
