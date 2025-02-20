def reverse(args):
  inp = args.get("input","")
  out = "Perfavore scrivi un input"
  if inp != "":
    out = inp[::-1]
  return { "output": out }
