import os, requests as req

def test_cache_int():
    url = os.getenv("OPSDEV_HOST") + "/api/my/hello/cache"
    res = req.get(url).json()
    assert res.get("output") == "Please provide a redis command."
    res = req.post(url, json={"input": "ECHO 'hello world'"}).json()
    assert res.get("output") == "hello world"
    res = req.post(url, json={"input": "error"}).json()
    assert res.get("output") == "unknown command 'error', with args beginning with: "

