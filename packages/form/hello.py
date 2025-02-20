def main(args):
    out = f"Hello, {args.get("input", "world")}"
    return {
        "body": out 
    }
