#--kind python:default
#--web true
#--timeout 300000
#--param OLLAMA_HOST $OLLAMA_HOST
#--param AUTH $AUTH
#--param S3_HOST $S3_HOST
#--param S3_PORT $S3_PORT
#--param S3_ACCESS_KEY $S3_ACCESS_KEY
#--param S3_SECRET_KEY $S3_SECRET_KEY
#--param S3_BUCKET_DATA $S3_BUCKET_DATA
#--param S3_API_URL $S3_API_URL
#--param MILVUS_HOST $MILVUS_HOST
#--param MILVUS_PORT $MILVUS_PORT
#--param MILVUS_DB_NAME $MILVUS_DB_NAME
#--param MILVUS_TOKEN $MILVUS_TOKEN
#--param REDIS_URL $REDIS_URL
#--param REDIS_PREFIX $REDIS_PREFIX

import webrag

def main(args):
  return { "body": webrag.webrag(args)}
