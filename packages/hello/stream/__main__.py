#--kind python:default
#--web true
import stream
def main(args):
  return { "body": stream.stream(args) }
