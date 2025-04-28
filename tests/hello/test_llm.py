import sys 
sys.path.append("packages/hello/llm")
import llm

def test_llm():
    res = llm.llm({})
    assert res["output"].startswith("Welcome to llama")
    args = {"input": "What is the capital of Italy?"}
    res = llm.llm(args).get("output", "")
    assert res.lower().find("rom") != -1
