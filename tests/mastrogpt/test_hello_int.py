import os, requests as req
def test_demo():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/mastrogpt/hello"
    res = req.get(url).json()
    assert res.get("output") == "Hello, world"
    args = { "input": "Test"}
    res = req.post(url, json=args).json()
    assert res["output"] == "Hello, Test"