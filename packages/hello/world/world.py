def world(args):
  # TODO: the expected output is "Hello, <name>" - fix the bug
  name = args.get("input", "world")
  return { "output": f"Hi, {name}" }
