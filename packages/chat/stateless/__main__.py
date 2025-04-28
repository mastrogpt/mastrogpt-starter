#--kind python:default
#--web true
#TODO:E2.1
#--...
#--...
#END TODO

import stateless
def main(args):
  return { "body": stateless.stateless(args) }
