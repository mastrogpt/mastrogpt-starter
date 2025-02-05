#--kind python:default
#--web true
import reverse
def main(args):
  return { "body": reverse.reverse(args) }
