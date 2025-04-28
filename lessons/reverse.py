def main(args):
    inp = args.get("input", "")
    out = "Plese provide some input"
    if inp != "":
        out = inp[::-1]
    return { "body": out}