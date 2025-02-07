#--kind python:default
#--web true
#--param S3_HOST $S3_HOST
#--param S3_PORT $S3_PORT
#--param S3_ACCESS_KEY $S3_ACCESS_KEY
#--param S3_SECRET_KEY $S3_SECRET_KEY
#--param S3_BUCKET_DATA $S3_BUCKET_DATA

import store

def main(args):
  return { "body": store.store(args) }
