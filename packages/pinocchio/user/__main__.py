#--kind python:default
#--web true
import user
def main(args):
  return { "body": user.user(args) }
