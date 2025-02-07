import os, requests as req
def test_llm_int():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/hello/llm"
    res = req.get(url).json()
    assert res["output"].startswith("Welcome to llama")
    args = {"input": "what is the capital of Italy?"}
    res =req.post(url, json=args).json().get("output", "")
    assert res.lower().find("rom") != -1
